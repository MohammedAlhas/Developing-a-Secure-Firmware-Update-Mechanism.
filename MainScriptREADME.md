# Firmware Update Manager (update_terminal_ui.py)

## Overview

The **Firmware Update Manager (update_terminal_ui.py)** is a Python script designed to facilitate the management of firmware updates for devices. It allows users to authenticate, check for firmware updates, download firmware, verify the integrity of the downloaded firmware, and apply updates based on user roles. The script is structured to ensure secure operations while maintaining a user-friendly interface.

## Features

- **User Authentication**: Supports role-based access control with three user roles:
  - Admin: Can apply firmware updates.
  - Standard User: Can download and verify firmware but cannot apply updates.
  - Viewer: Has view-only access.
  
- **Firmware Management**:
  - Check for available firmware updates.
  - Download firmware from a secure server.
  - Verify firmware using digital signatures.
  - Apply firmware updates securely.

- **Logging**: All actions and events are logged for tracking and debugging purposes.

## Requirements

- Python 3.x
- Required libraries:
  - requests
  - PyYAML

**You can install the required libraries using pip**

```bash
pip install requests pyyaml
```
### Configuration
The script requires a config.yaml file for configuration. Here is an example of the expected structure:

```yaml
firmware:
  firmware_file: "firmware.bin"  # Name of the firmware file
  signature_file: "firmware.sig"   # Name of the signature file
  url: "https://example.com/firmware/"  # Base URL for firmware downloads
  log_file: "firmware_update.log"  # Log file name

server:
  cert_file: "server_cert.pem"  # Path to the server certificate for SSL verification
```

**Example config.yaml File**
```yaml
firmware:
  firmware_file: "firmware.bin"
  signature_file: "firmware.sig"
  url: "https://example.com/firmware/"
  log_file: "firmware_update.log"

server:
  cert_file: "server_cert.pem"
```
Usage
Run the Script: Execute the script from the command line.

```bash
python firmware_update_manager.py
```

### Authenticate: Enter your username and password. The credentials can be one of the following:

**Admin**: admin, **password**: password123

**Standard User**: user, **password**: userpass

**Viewer**: viewer, **password**: viewpass

Select an Option: Choose from the menu to check for updates, download firmware, verify firmware, apply firmware, execute all actions, or exit.

### Functions Explained 
**authenticate**: Authenticates the user based on predefined credentials. 

**check_for_updates**: Checks for new firmware updates from the configured server.

**download_firmware(firmware)**: Downloads the specified firmware from the server.

**verify_firmware(firmware)**: Verifies the downloaded firmware using OpenSSL to check its digital signature.

**apply_firmware(firmware)**: Applies the firmware update to the device (simulated in this script).

**display_menu**: Displays the main menu for user options.

**ask_to_continue**: Prompts the user to continue with the next action or exit.

### Logging
The script logs all actions and errors to the specified log file (default: firmware_update.log). You can check this file for details about operations and any potential issues.

### Security Considerations
Ensure that your server certificate is correctly configured to avoid SSL verification issues.
Change the default passwords in the authenticate() function for production use.

### Contributing
Contributions are welcome! If you have suggestions or improvements, please open an issue or submit a pull request.

### License
This project is licensed under the MIT License - see the LICENSE file for details.
