"""
FCC ULS Downloader and Loader
Author: Tiran Dagan
Contact: tiran@tirandagan.com

Description: Module to handle downloading the ZIP file.
"""

import requests
import logging
import time
import os
from modules.progress import create_download_progress_bar

def download_file(url, dest_path, retries=3):
    """
    Download a file from the given URL to the destination path with a progress bar.
    
    Args:
        url (str): The URL to download from.
        dest_path (str): The path to save the file to.
        retries (int): Number of retry attempts if download fails.
        
    Returns:
        bool: True if download was successful, False otherwise.
    """
    attempt = 0
    while attempt < retries:
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            
            # Make a HEAD request first to get the file size
            response_head = requests.head(url)
            total_size_in_bytes = int(response_head.headers.get('content-length', 0))
            
            # Stream the download with progress bar
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            # Initialize custom progress bar
            progress_bar = create_download_progress_bar(
                total_size=total_size_in_bytes,
                desc="Downloading FCC data"
            )
            
            with open(dest_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:  # filter out keep-alive new chunks
                        file.write(chunk)
                        progress_bar.update(len(chunk))
            
            progress_bar.close()
            logging.info(f"File downloaded successfully: {dest_path}")
            return True
            
        except requests.RequestException as e:
            attempt += 1
            logging.error(f"Download attempt {attempt} failed: {e}")
            print(f"Download attempt {attempt} failed: {e}")
            if attempt < retries:
                wait_time = 5
                print(f"Retrying in {wait_time} seconds...")
                time.sleep(wait_time)  # Wait before retrying
    
    logging.error(f"Failed to download file after {retries} attempts.")
    return False

def _generate_bar(self, width=10):
    """Generate a progress bar string"""
    if self.total and self.total > 0:
        percent = self.n / self.total
        filled_length = int(width * percent)
        bar = '█' * filled_length + ' ' * (width - filled_length)
        return bar
    return ' ' * width
