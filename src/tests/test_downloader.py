"""
FCC ULS Downloader and Loader
Author: Tiran Dagan
Contact: tiran@tirandagan.com

Description: Unit tests for downloader module.
"""

import unittest
import os
from modules.downloader import download_file
from modules.config import Config

class TestDownloader(unittest.TestCase):
    def setUp(self):
        self.url = Config.URL
        self.zip_path = "test_l_amat.zip"

    def tearDown(self):
        if os.path.exists(self.zip_path):
            os.remove(self.zip_path)

    def test_download_file(self):
        result = download_file(self.url, self.zip_path)
        self.assertTrue(result)
        self.assertTrue(os.path.exists(self.zip_path))
        self.assertGreater(os.path.getsize(self.zip_path), 0)

if __name__ == "__main__":
    unittest.main()
