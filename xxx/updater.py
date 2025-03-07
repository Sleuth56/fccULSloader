""" 
FCC Updater Module - FCC Amateur Radio License Database Update Management
========================================================================

Author: Tiran Dagan (Backstop Radio)
Contact: tiran@tirandagan.com
License: MIT License

Description:
-----------
This module manages the process of updating the FCC Amateur Radio License database.
It handles checking for updates, downloading new data, extracting files, and loading
data into the SQLite database.

Functions:
---------
Metadata Management:
- save_download_metadata(last_modified_time): Save metadata about the download
- get_last_download_metadata(): Get metadata about the last download

Update Process:
- check_for_update(): Check if a new version of the data is available
- update_data(skip_download, keep_files, force_download, quiet): Update the database

Usage:
-----
1. Check if an update is available:
   update_available = updater.check_for_update()

2. Update the database:
   updater.update_data(
       skip_download=False,  # Whether to skip the download step
       keep_files=False,     # Whether to keep temporary files
       force_download=False, # Whether to force download regardless of update status
       quiet=False           # Whether to suppress INFO log messages
   )

Dependencies:
------------
- requests: For HTTP requests to check and download updates
- modules.downloader: For downloading the data file
- modules.extractor: For extracting the downloaded zip file
- modules.loader: For loading data into the database
- modules.config: For configuration settings
- modules.logger: For logging
- modules.database: For database operations
- modules.filesystemtools: For file system operations
"""

import logging
import os
import requests
import json
import time
from datetime import datetime
from email.utils import parsedate_to_datetime
from modules import downloader, extractor, loader, config, logger
from modules.database import FCCDatabase
from modules.filesystemtools import ensure_directory, cleanup_temp_files, file_exists

# Path to the metadata file that stores information about the last download
METADATA_FILE = os.path.join(config.Config.DATA_PATH, "fcc_metadata.json")

def save_download_metadata(last_modified_time):
    """
    Save metadata about the download to a JSON file.
    
    Args:
        last_modified_time (float): Timestamp of the last modified time of the remote file
    """
    metadata = {
        'last_download_timestamp': time.time(),
        'last_modified_timestamp': last_modified_time,
        'download_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'source_url': config.Config.ZIP_FILE_URL
    }
    
    # Ensure data directory exists
    ensure_directory('data')
    
    try:
        with open(METADATA_FILE, 'w') as f:
            json.dump(metadata, f, indent=4)
        logging.info(f"Saved download metadata to {METADATA_FILE}")
    except Exception as e:
        logging.error(f"Error saving metadata: {e}")

def get_last_download_metadata():
    """
    Get metadata about the last download from the JSON file.
    
    Returns:
        dict: Metadata about the last download, or None if the file doesn't exist
    """
    if not file_exists(METADATA_FILE):
        return None
    
    try:
        with open(METADATA_FILE, 'r') as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"Error reading metadata file: {e}")
        return None

def check_for_update():
    """
    Check if a new version of the data file is available by comparing the last modified
    time of the remote file with the last download time stored in the metadata file.
    
    Returns:
        bool: True if an update is available, False otherwise
    """
    logging.info("Checking for updates...")
    try:
        # Get the last modified time of the remote file
        response = requests.head(config.Config.ZIP_FILE_URL)
        response.raise_for_status()
        remote_last_modified = response.headers.get('Last-Modified')
        
        if not remote_last_modified:
            logging.warning("Could not determine the last modified date of the remote file.")
            return True
        
        remote_last_modified_time = parsedate_to_datetime(remote_last_modified).timestamp()
        
        # Get the last download metadata
        metadata = get_last_download_metadata()
        
        if metadata is None:
            logging.info("No previous download metadata found. Downloading new file.")
            return True
        
        last_modified_timestamp = metadata.get('last_modified_timestamp')
        
        if last_modified_timestamp is None:
            logging.info("No last modified timestamp in metadata. Downloading new file.")
            return True
        
        # Compare the timestamps
        if remote_last_modified_time > last_modified_timestamp:
            logging.info("A new version of the data file is available.")
            return True
        else:
            logging.info("The data file is up to date.")
            return False
            
    except requests.RequestException as e:
        logging.error(f"Error checking for updates: {e}")
        return False

def update_data(skip_download=False, keep_files=False, force_download=False, quiet=False):
    """
    Update the FCC data by downloading, extracting, and loading it into the database.
    
    Args:
        skip_download (bool): Whether to skip the download step
        keep_files (bool): Whether to keep the downloaded and extracted files after loading
        force_download (bool): Whether to force download even if no update is available
        quiet (bool): Whether to suppress INFO log messages (only show WARNING and above)
    """
    # Set up logging with appropriate level
    logger.setup_logging(verbose=False)
    
    # If quiet mode is enabled, set log level to WARNING
    if quiet:
        logger.set_log_level(logging.WARNING)
    
    logging.info("Starting the FCC ULS data downloader and loader.")
    db = FCCDatabase(config.Config.DB_PATH)
    
    if not skip_download:
        # When force_download is True, we download regardless of update status
        if force_download or check_for_update():
            if force_download:
                logging.info("Forcing download regardless of update status.")
            else:
                logging.info("Downloading the latest data file.")
                
            # Get the last modified time of the remote file before downloading
            try:
                response = requests.head(config.Config.ZIP_FILE_URL)
                response.raise_for_status()
                remote_last_modified = response.headers.get('Last-Modified')
                remote_last_modified_time = parsedate_to_datetime(remote_last_modified).timestamp() if remote_last_modified else time.time()
            except requests.RequestException as e:
                logging.error(f"Error getting last modified time: {e}")
                remote_last_modified_time = time.time()
            
            # Ensure data directory exists
            ensure_directory('data')
            
            # Download the file
            downloader.download_file(url=config.Config.ZIP_FILE_URL, dest_path=config.Config.ZIP_FILE_PATH)
            
            # Save metadata about the download
            save_download_metadata(remote_last_modified_time)
            
            # Create extraction directory before extracting
            ensure_directory('extraction')
            
            logging.info("Extracting data file.")
            extractor.extract_data(config.Config.ZIP_FILE_PATH, config.Config.EXTRACT_PATH)
        else:
            logging.info("Skipping download as no new update is available.")
    else:
        logging.info("Skipping download step as requested.")
    
    # Check if extraction directory exists and has files
    if not os.path.exists(config.Config.EXTRACT_PATH):
        logging.error("Extraction directory does not exist. Cannot proceed with loading data.")
        print("Error: Extraction directory does not exist. Cannot proceed with loading data.")
        print("This is likely because the extraction directory was not created during download.")
        print("Try running with --force-download to ensure a fresh download and extraction.")
        return
    
    # Check if extraction directory is empty
    if not os.listdir(config.Config.EXTRACT_PATH):
        logging.error("Extraction directory is empty. Cannot proceed with loading data.")
        print("Error: Extraction directory is empty. Cannot proceed with loading data.")
        print("This is likely because the extraction process failed or was interrupted.")
        print("Try running with --force-download to ensure a fresh download and extraction.")
        return
    
    tables_to_process = config.Config.TABLES_TO_PROCESS
    
    logging.info("Creating database tables.")
    db.create_tables(tables_to_process)
    db.disable_indexes(tables_to_process)
    
    logging.info(f"Loading data into the database for tables: {tables_to_process}.")
    loader.load_all_data(db, config.Config.EXTRACT_PATH, config.Config.USE_MULTITHREADING, tables_to_process)
    
    logging.info("Applying indexes.")
    db.enable_indexes(tables_to_process)
    
    # Clean up temporary files after successful database loading if keep_files is False
    if not keep_files:
        cleanup_temp_files()
        logging.info("Temporary files cleaned up.")
    else:
        logging.info("Keeping temporary files as requested.")
    
    logging.info("Process completed successfully.")
    print("FCC data loading completed successfully.")