import requests
import time
import schedule
import logging
import constants as cs

# Define the species ID for Pontia protodice (or get it dynamically)
SPECIES_ID = cs.species_ids["Pontia protodice"]  # Pontia protodice

# URL for iNaturalist observations endpoint
API_URL = "https://api.inaturalist.org/v1/observations"

# Track the last observation date to avoid duplicate alerts
last_observation_date = None

# Configure logging
logging.basicConfig(filename='inat_observations.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def check_new_observations():
    global last_observation_date
    
    params = {
        'taxon_id': SPECIES_ID,
        'order_by': 'observed_on',
        'order': 'desc',
        'per_page': 1
    }

    try:
        response = requests.get(API_URL, params=params)
        response.raise_for_status()  # Raise an error for bad status codes
        data = response.json()

        if data['total_results'] > 0:
            latest_observation = data['results'][0]
            observation_date = latest_observation['observed_on']

            if observation_date != last_observation_date:
                last_observation_date = observation_date
                print(f"New observation of Pontia protodice found!")
                print(f"Date: {observation_date}")
                print(f"Location: {latest_observation['place_guess']}")
                print(f"Image: {latest_observation['photos'][0]['url']}")
                logging.info(f"New observation: {latest_observation}")

    except requests.RequestException as e:
        logging.error(f"Error fetching data: {e}")

# Schedule the script to run every 15 minutes
schedule.every(1).minutes.do(check_new_observations)

# Run the scheduler
while True:
    schedule.run_pending()
    time.sleep(1)
