"""
FCC Config Module - Configuration Settings for FCC Database Tools
================================================================

Author: Tiran Dagan (Backstop Radio)
Contact: tiran@tirandagan.com
License: MIT License

Description:
-----------
This module provides configuration settings for the FCC database tools.
It defines paths, URLs, and other settings used throughout the application.

Classes:
-------
Config: Main configuration class with static attributes

    Attributes:
    ----------
    - BASE_DIR: Base directory of the application
    - DATA_PATH: Path to the data directory
    - ZIP_FILE_PATH: Path to the downloaded zip file
    - EXTRACT_PATH: Path to the directory for extracted files
    - DB_PATH: Path to the SQLite database file
    - ZIP_FILE_URL: URL for downloading the FCC database file
    - USE_MULTITHREADING: Whether to use multithreading for data loading
    - TABLES_TO_PROCESS: List of tables to process during data loading

Usage:
-----
Import the Config class and access its attributes:

    from modules.config import Config
    
    # Access database path
    db_path = Config.DB_PATH
    
    # Access download URL
    url = Config.ZIP_FILE_URL
    
    # Access data directory
    data_dir = Config.DATA_PATH

Customization:
------------
To customize the configuration, modify the attributes in this file.
For example, to change the database path or the tables to process.
"""

import os

class Config:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_PATH = os.path.join(BASE_DIR, "data")
    ZIP_FILE_PATH = os.path.join(DATA_PATH, "l_amat.zip")
    EXTRACT_PATH = os.path.join(DATA_PATH, "extracted")
    DB_PATH = os.path.join(DATA_PATH, "fcc_data.db")
    ZIP_FILE_URL = 'https://data.fcc.gov/download/pub/uls/complete/l_amat.zip'  # URL for the file
    USE_MULTITHREADING = False
    
    # For just the tables needed for the FCC Tool, uncomment the following line and comment the one above it
    TABLES_TO_PROCESS = ["AM","EN","HD"]
    # For a full download into the database of all FCC files, uncomment the following line and comment the one above it
    # TABLES_TO_PROCESS = ["AM", "CO", "EN", "HD", "HS", "LA", "SC", "SF"]