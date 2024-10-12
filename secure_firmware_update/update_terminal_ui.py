import os
import requests
import subprocess
from getpass import getpass
import logging
from datetime import datetime
import yaml

# Load configuration from config.yaml
with open('config.yaml', 'r') as config_file:
    config = yaml.safe_load(config_file)

# Configure logging
log_file = config['firmware'].get('log_file', 'firmware_update.log')
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(message)s')

# Function to authenticate user
def authenticate():
    username = input("Enter username: ")
    password = getpass("Enter password: ")

    # Simple role-based authentication
    if username == "admin" and password == "password123":
        logging.info("Admin authentication successful")
        return "admin"
    elif username == "user" and password == "userpass":
        logging.info("Standard user authentication successful")
        return "standard_user"
    elif username == "viewer" and password == "viewpass":
        logging.info("Viewer authentication successful")
        return "viewer"
    else:
        logging.warning("Authentication failed for user: %s", username)
        print("Authentication failed.")
        return None

# Check for new firmware updates
def check_for_updates():
    print("Checking for updates...")
    logging.info("Checking for firmware updates.")
    
    # Simulate checking server for updates
    firmware = config['firmware']['firmware_file']  # Use firmware name from config
    logging.info(f"New firmware available: {firmware}")
    return firmware

# Download the firmware from server
def download_firmware(firmware):
    url = config['firmware']['url'] + firmware  # Use URL from config
    print(f"Downloading firmware: {firmware}...")
    
    try:
        # Provide path to the certificate for verification
        response = requests.get(url, verify=config['server']['cert_file'])  # Use cert file from config
        response.raise_for_status()
        
        with open(firmware, 'wb') as file:
            file.write(response.content)
        
        logging.info("Firmware %s downloaded successfully.", firmware)
        print("Firmware downloaded successfully.")
        return True
    except requests.exceptions.RequestException as e:
        logging.error("Error downloading firmware from %s: %s", url, e)
        print(f"Error downloading firmware: {e}")
        return False

# Verify the firmware using OpenSSL
def verify_firmware(firmware):
    print(f"Verifying firmware: {firmware}...")
    logging.info("Verifying firmware: %s", firmware)
    
    # Command to verify the firmware's signature using OpenSSL
    verify_cmd = f"openssl dgst -sha256 -verify public_key.pem -signature {config['firmware']['signature_file']} {firmware}"
    
    try:
        result = subprocess.run(verify_cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            logging.info("Firmware verification successful: %s", firmware)
            print("Firmware verified successfully.")
            return True
        else:
            logging.error("Firmware verification failed: %s", result.stderr.decode())
            print(f"Firmware verification failed: {result.stderr.decode()}")
            return False
    except Exception as e:
        logging.error("Error verifying firmware: %s", e)
        print(f"Error verifying firmware: {e}")
        return False

# Apply the firmware update
def apply_firmware(firmware):
    print(f"Applying firmware: {firmware}...")
    logging.info("Applying firmware: %s", firmware)
    
    # Simulate applying firmware (In reality, you would have system-specific commands here)
    print("Firmware update applied successfully.")
    logging.info("Firmware update applied successfully.")

# Function to display the menu
def display_menu():
    print("\nWelcome to the Firmware Update Manager!")
    print("This tool allows you to check for updates, download, verify, and apply firmware.")
    print("1. Check for updates")
    print("2. Download firmware")
    print("3. Verify firmware")
    print("4. Apply firmware")
    print("5. Execute all actions")
    print("6. Exit")
    choice = input("Select an option: ")
    return choice

# Function to ask if the user wants to continue with the next step
def ask_to_continue():
    while True:
        proceed = input("Would you like to proceed with the next option? (yes/no): ").strip().lower()
        if proceed in ['yes', 'y']:
            return True
        elif proceed in ['no', 'n']:
            return False
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")

# Main update process
def update_process():
    role = authenticate()
    if role:
        logging.info("User role: %s", role)  # Log the user's role
        if role in ['admin', 'standard_user', 'viewer']:
            firmware = None
            while True:
                choice = display_menu()
                
                if choice == '1':
                    firmware = check_for_updates()
                    if firmware:
                        print(f"New firmware available: {firmware}")
                    else:
                        print("No new firmware available.")
                    if not ask_to_continue():
                        break
                elif choice == '2':
                    if firmware is None:
                        firmware = check_for_updates()
                    if firmware and download_firmware(firmware):
                        print("Download complete.")
                    if not ask_to_continue():
                        break
                elif choice == '3':
                    firmware = config['firmware']['firmware_file']
                    if verify_firmware(firmware):
                        print("Firmware verified successfully.")
                    if not ask_to_continue():
                        break
                elif choice == '4':
                    firmware = config['firmware']['firmware_file']
                    if role == 'admin':
                        if verify_firmware(firmware):
                            apply_firmware(firmware)
                            break  # Exit after applying firmware
                    else:
                        print("Only admins can apply firmware.")
                    if not ask_to_continue():
                        break
                elif choice == '5':
                    firmware = check_for_updates()
                    if firmware:
                        if download_firmware(firmware):
                            if role == 'admin':
                                if verify_firmware(firmware):
                                    apply_firmware(firmware)
                                    break  # Exit after applying firmware
                                else:
                                    print("Firmware verification failed.")
                            else:
                                print("Download complete. Only admins can apply firmware.")
                    if not ask_to_continue():
                        break
                elif choice == '6':
                    print("Exiting the Firmware Update Manager.")
                    break
                else:
                    print("Invalid option, please try again.")

        else:
            logging.info("User %s has view-only access.", role)
            print("You have view-only access.")
    else:
        logging.error("Authentication failed. Exiting.")
        print("Authentication failed. Exiting.")

# Entry point of the script
if __name__ == "__main__":
    update_process()
