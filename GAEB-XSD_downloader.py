import os
import hashlib
import requests
import zipfile
from bs4 import BeautifulSoup
import shutil

# URL of the webpage you want to access
url = 'https://www.gaeb.de/de/service/downloads/gaeb-datenaustausch/'

# Path to the current script
script_path = os.path.dirname(os.path.realpath(__file__))

# Path to save the files
path = os.path.join(script_path, 'download')

# Path to save the xsd files
xsd_path = os.path.join(script_path, 'GAEB-XSD_schema_files')

# Create directories if they do not exist
os.makedirs(path, exist_ok=True)
os.makedirs(xsd_path, exist_ok=True)

# Function to download and save a file
def download_file(href, path):
    # Full path to save the file
    filename = os.path.basename(href)
    full_path = os.path.join(path, filename)

    # Only download the file if it does not exist
    if not os.path.exists(full_path):
        # Download the file
        response = requests.get(href)

        # Ensure the request was successful
        if response.status_code == 200:
            # Save the file
            with open(full_path, 'wb') as file:
                file.write(response.content)

            print(f"File {filename} has been downloaded and saved.")

            # If it's a zip file, extract it
            if href.endswith('.zip'):
                with zipfile.ZipFile(full_path, 'r') as zip_ref:
                    zip_ref.extractall(path)
                    print(f"File {filename} has been extracted.")

# Function to move a file
def move_file(old_file_path, new_file_path):
    old_file_hash = hashlib.md5(open(old_file_path, 'rb').read()).hexdigest()

    # If file already exists, check the hash
    if os.path.exists(new_file_path):
        new_file_hash = hashlib.md5(open(new_file_path, 'rb').read()).hexdigest()

        # If hashes are the same, do not move the file
        if old_file_hash == new_file_hash:
            return

    # Move the file
    shutil.move(old_file_path, new_file_path)
    print(f"File {os.path.basename(old_file_path)} has been moved to the 'GAEB-XSD_schema'")

# Get the webpage
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Find all links on the webpage
for link in soup.find_all('a'):
    href = link.get('href')
    
    # Check if link is to a .zip or .xsd file
    if href.endswith('.zip') or href.endswith('.xsd'):
        download_file(href, path)

# Move all xsd files to GAEB-XSD_schema_files
for root, dirs, files in os.walk(path):
    for file in files:
        if file.endswith('.xsd'):
            old_file_path = os.path.join(root, file)
            new_file_path = os.path.join(xsd_path, file)
            move_file(old_file_path, new_file_path)

# Delete all non-zip files and empty directories in the 'download' directory
for root, dirs, files in os.walk(path, topdown=False):
    for file in files:
        if not file.endswith('.zip'):
            file_path = os.path.join(root, file)
            os.remove(file_path)
            print(f"File {file} has been deleted.")
    for dir in dirs:
        dir_path = os.path.join(root, dir)
        if not os.listdir(dir_path):
            os.rmdir(dir_path)
            print(f"Directory {dir} has been deleted.")
