import os
import subprocess
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def check_for_updates():
    try:
        os.chdir('/home/pi/Documents/MatrixAPI')

        subprocess.run(['git', 'fetch'], check=True)

        local_hash = subprocess.check_output(['git', 'rev-parse', 'HEAD']).strip()
        remote_hash = subprocess.check_output(['git', 'rev-parse', '@{u}']).strip()

        if local_hash != remote_hash:
            logging.info("New changes detected. Pulling updates...")
            subprocess.run(['git', 'pull'], check=True)

            # Restart the API
            restart_api()
        else:
            logging.info("No changes detected.")

    except Exception as e:
        logging.error(f"Error checking for updates: {e}")

def restart_api():
    try:
        # Restart the API
        logging.info("Restarting the API...")
        subprocess.run(['sudo', 'systemctl', 'restart', 'matrix-api.service'], check=True)
        logging.info("API restarted successfully.")
    except Exception as e:
        logging.error(f"Error restarting the API: {e}")

if __name__ == "__main__":
    check_for_updates()