import os
import json
import discord
import logging
import constants as cs
import requests
from discord.ext import commands
from dotenv import load_dotenv

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='-',intents=intents)

# Set up logging config
logging.basicConfig(filename='quicknat.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# TODO: add functionality for multiple EOPs as well as plant annotations
def create_annotation_data(shortform: str) -> list[str]:
    annotations = []
    if len(shortform) == 4: # Standard Life - EOP - Stage - Sex
        if shortform[0] in cs.ANNOTATION_LIFE:
            annotations.append({'type': 17, 'value': cs.ANNOTATION_LIFE[shortform[0]]})
        if shortform[1] in cs.ANNOTATION_EOP:
            annotations.append({'type': 22, 'value': cs.ANNOTATION_EOP[shortform[1]]})
        if shortform[2] in cs.ANNOTATION_STAGE:
            annotations.append({'type': 1, 'value': cs.ANNOTATION_STAGE[shortform[2]]})
        if shortform[3] in cs.ANNOTATION_SEX:
            annotations.append({'type': 9, 'value': cs.ANNOTATION_SEX[shortform[3]]})
    return annotations


@bot.command(aliases=['view'])
async def see(ctx, observation_id: str) -> None:
    # TODO: add author notes to logging
    logging.info(f"View command accessed with parameters observation_id: {observation_id}.")
    try:
        response = requests.get(cs.OBSERVATION_URL + f'/{observation_id}', headers=cs.HEADERS)
        response.raise_for_status()  # Raise an error for bad status codes

        data = response.json()['results'][0]
        logging.info(f"Full data package for observation {observation_id}: {data}")

        image_url = data['photos'][0]['url'].replace("square", "original")
        annotations = data.get('annotations', [])
        annotation_str = ""
        for anno in annotations:
            annotation_str += f"{anno['controlled_attribute']['label']}: {anno['controlled_value']['label']}\n"


        embed = discord.Embed(title=f"Observation {observation_id}: {data['taxon']['name']}", color=discord.Color.blue(), description=annotation_str)
        embed.add_field(name = "Grade", value = data['quality_grade'], inline = False)
        embed.add_field(name = "Time observed", value = data['time_observed_at'], inline = False)
        embed.set_image(url=image_url)

        await ctx.send(embed=embed)

    except requests.RequestException as e:
        await ctx.send(f"Error fetching annotations for observation {observation_id}: {e}")


@bot.command(aliases=['pa', 'fp', 'postall'])
async def fullpost(ctx, observation_id: str, taxon: str, annotations: str = None) -> None:
    # Step 1: Post Identification
    if taxon in cs.SPECIES_IDS:
        # Data headers for the identification
        data = {
        'identification': {
            'observation_id': int(observation_id),
            'taxon_id': cs.SPECIES_IDS[taxon]
            }
        }

        try:
            response = requests.post(cs.ID_URL, headers=cs.HEADERS, data=json.dumps(data))
            response.raise_for_status()  # Raise an error for bad status codes
            await ctx.send(f"Successfully posted identification for observation {observation_id}.")
        except requests.RequestException as e:
            await ctx.send(f"Error posting identification: {e}")
    else:
        await ctx.send("ID phase skipped.")

    # Step 2: Post Annotations
    annotation_list = create_annotation_data(annotations)
    for annotation in annotation_list:
        data = {
            'resource_type': 'Observation',
            'resource_id': int(observation_id),
            'controlled_attribute_id': annotation['type'],
            'controlled_value_id': annotation['value']
        }

        try:
            response = requests.post(cs.ANNOTATION_URL, headers=cs.HEADERS, data=json.dumps(data))
            response.raise_for_status()  # Raise an error for bad status codes
            await ctx.send(f"Successfully added annotation {annotation} to observation {observation_id}.")
            logging.info(f"Successfully added annotation {annotation} to observation {observation_id}.")
        except requests.RequestException as e:
            await ctx.send(f"Error adding annotation {annotation} to observation {observation_id}: {e}")
            logging.error(f"Error adding annotation {annotation} to observation {observation_id}: {e}")


if __name__ == '__main__':
    load_dotenv()
    bot_token = os.getenv("BOT_TOKEN")
    bot.run(cs.TOKEN)
