import schedule
import time
import requests
import logging
import yaml

# Load configuration from config.yaml
with open('config.yaml', 'r') as config_file:
    config = yaml.safe_load(config_file)

# Configure logging
log_file = config['firmware'].get('log_file', 'firmware_update.log')
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(message)s')

def check_for_updates():
    logging.info("Checking for firmware updates automatically.")
    url = config['firmware']['url'] + config['firmware']['firmware_file']  # Use URL from config
    try:
        response = requests.head(url)
        if response.status_code == 200:
            logging.info("New firmware available.")
            print("New firmware available.")
        else:
            logging.info("No updates available.")
            print("No updates available.")
    except requests.exceptions.RequestException as e:
        logging.error("Error checking for updates: %s", e)

def job():
    check_for_updates()

# Schedule to run daily at 10:00 AM
schedule.every().day.at("10:00").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
