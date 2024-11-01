import os
import hashlib
import requests
import zipfile
from bs4 import BeautifulSoup
import shutil
import tempfile

# URL of the webpage you want to access
URL = 'https://www.gaeb.de/de/service/downloads/gaeb-datenaustausch/'

# Paths to save files
SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))
DOWNLOAD_PATH = os.path.join(tempfile.gettempdir(), 'temp_download')
XSD_PATH = os.path.join(SCRIPT_PATH, 'GAEB-XSD_schema_files')

# Create directories if they do not exist
os.makedirs(DOWNLOAD_PATH, exist_ok=True)
os.makedirs(XSD_PATH, exist_ok=True)

# Function to download and save a file
def download_file(href, path):
    filename = os.path.basename(href)
    full_path = os.path.join(path, filename)

    # Only download the file if it does not exist
    if not os.path.exists(full_path):
        response = requests.get(href)
        if response.status_code == 200:
            with open(full_path, 'wb') as file:
                file.write(response.content)
            print(f"File {filename} has been downloaded and saved.")

            # Extract if it's a zip file
            if filename.endswith('.zip'):
                with zipfile.ZipFile(full_path, 'r') as zip_ref:
                    zip_ref.extractall(path)
                    print(f"File {filename} has been extracted.")

# Function to move a file if it doesn't already exist with the same hash
def move_file(old_file_path, new_file_path):
    if not os.path.exists(new_file_path) or hashlib.md5(open(old_file_path, 'rb').read()).hexdigest() != hashlib.md5(open(new_file_path, 'rb').read()).hexdigest():
        shutil.move(old_file_path, new_file_path)
        print(f"File {os.path.basename(old_file_path)} has been moved to the 'GAEB-XSD_schema_files'.")

# Function to process the download and extraction
def process_gaeb_xsd_download():
    # Get the webpage and parse it
    response = requests.get(URL)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find and process all .zip and .xsd links
        for link in soup.find_all('a', href=True):
            href = link['href']
            if href.endswith(('.zip', '.xsd')):
                download_file(href, DOWNLOAD_PATH)

        # Move all .xsd files to XSD_PATH
        for root, _, files in os.walk(DOWNLOAD_PATH):
            for file in files:
                if file.endswith('.xsd'):
                    move_file(os.path.join(root, file), os.path.join(XSD_PATH, file))

        # Delete all non-zip files and empty directories in the 'temp_download' directory
        for root, dirs, files in os.walk(DOWNLOAD_PATH, topdown=False):
            for file in files:
                if not file.endswith('.zip'):
                    os.remove(os.path.join(root, file))
                    print(f"File {file} has been deleted.")
            for dir in dirs:
                dir_path = os.path.join(root, dir)
                if not os.listdir(dir_path):
                    os.rmdir(dir_path)
                    print(f"Directory {dir} has been deleted.")

        # Delete the 'temp_download' directory itself
        if os.path.exists(DOWNLOAD_PATH):
            shutil.rmtree(DOWNLOAD_PATH)
            print(f"Directory 'temp_download' has been deleted.")

# Allow the script to be used as a module or standalone script
if __name__ == "__main__":
    process_gaeb_xsd_download()
