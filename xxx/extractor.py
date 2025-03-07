"""
FCC ULS Downloader and Loader
Author: Tiran Dagan
Contact: tiran@tirandagan.com

Description: Module to handle extracting data from the downloaded zip file.
"""

import os
import zipfile
import logging
import shutil

def extract_data(zip_file_path, extract_to_path):
    """
    Extract the zip file to the specified directory.

    :param zip_file_path: Path to the zip file.
    :param extract_to_path: Directory to extract the files to.
    """
    if not os.path.exists(zip_file_path):
        logging.error(f"Zip file {zip_file_path} does not exist.")
        return

    # If the extraction directory exists, remove it to ensure a clean extraction
    if os.path.exists(extract_to_path):
        try:
            shutil.rmtree(extract_to_path)
            logging.info(f"Removed existing extraction directory: {extract_to_path}")
        except OSError as e:
            logging.error(f"Error removing existing extraction directory: {e}")
            print(f"Warning: Could not remove existing extraction directory: {e}")

    # Create a fresh extraction directory
    try:
        os.makedirs(extract_to_path, exist_ok=True)
    except OSError as e:
        logging.error(f"Error creating extraction directory: {e}")
        print(f"Error: Could not create extraction directory: {e}")
        return

    try:
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            print(f"Extracting {os.path.basename(zip_file_path)}...")
            zip_ref.extractall(extract_to_path)
            logging.info(f"Extracted {zip_file_path} to {extract_to_path}")
            print(f"Extraction completed successfully.")
    except zipfile.BadZipFile as e:
        logging.error(f"Failed to extract {zip_file_path}: {e}")
        print(f"Error: Failed to extract zip file: {e}")
