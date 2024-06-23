import json
import logging
import requests
import constants as cs


# Incomplete
def post_identification(observation_id: str):

    # Data for the identification
    data = {
        'identification': {
            'observation_id': observation_id,
            'taxon_id': SPECIES_ID
        }
    }

    try:
        response = requests.post(ID_URL, headers=headers, data=json.dumps(data))
        response.raise_for_status()  # Raise an error for bad status codes
        print(f"Successfully posted identification for observation {observation_id}.")
    except requests.RequestException as e:
        print(f"Error posting identification: {e}")

def get_observation_annotations(observation_id: str):
    try:
        response = requests.get(cs.OBSERVATION_URL, headers=cs.HEADERS)
        response.raise_for_status()  # Raise an error for bad status codes
        data = response.json()

        if 'results' in data and len(data['results']) > 0:
            observation = data['results'][0]
            annotations = observation.get('annotations', [])
            print(f"Annotations for observation {observation_id}:")
            for annotation in annotations:
                print(f" - Attribute ID: {annotation['controlled_attribute_id']}, "
                      f"Value ID: {annotation['controlled_value_id']}, "
                      f"Vote Score: {annotation['vote_score']}, "
                      f"Field name: {annotation['controlled_attribute']['label']}, "
                      f"Value name: {annotation['controlled_value']['label']}")
        else:
            print(f"No annotations found for observation {observation_id}.")
    except requests.RequestException as e:
        print(f"Error fetching annotations for observation {observation_id}: {e}")

def add_annotations(observation_id: str, annotation_string: str) -> None:
    annotations = create_annotation_data(annotation_string)
    for annotation in annotations:
        data = {
            'resource_type': 'Observation',
            'resource_id': int(observation_id),
            'controlled_attribute_id': annotation['type'],
            'controlled_value_id': annotation['value']
        }

        try:
            response = requests.post(cs.ANNOTATION_URL, headers=cs.HEADERS, data=json.dumps(data))
            response.raise_for_status()  # Raise an error for bad status codes
            print(f"Successfully added annotation {annotation} to observation {observation_id}.")
            logging.info(f"Successfully added annotation {annotation} to observation {observation_id}.")
        except requests.RequestException as e:
            print(f"Error adding annotation {annotation} to observation {observation_id}: {e}")
            logging.error(f"Error adding annotation {annotation} to observation {observation_id}: {e}")

def get_observation_photo(observation_id: str):
    try:
        response = requests.get(cs.OBSERVATION_URL + f'/{observation_id}', headers=cs.HEADERS)
        response.raise_for_status()  # Raise an error for bad status codes
        data = response.json()['results'][0]['photos']
        for x in data:
            print(x)
            print('\n\n')
    except requests.RequestException as e:
        print(f"Error fetching annotations for observation {observation_id}: {e}")

# Call the function to post the identification
#post_identification()
#get_observation_annotations(observation_id)
#add_annotations("221694191", "aoaf")
get_observation_photo("221694191")