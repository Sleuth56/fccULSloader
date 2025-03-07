"""
FCC ULS Downloader and Loader
Author: Tiran Dagan
Contact: tiran@tirandagan.com

Description: Unit tests for extractor module.
"""

import unittest
import os
from modules.extractor import extract_zip

class TestExtractor(unittest.TestCase):
    def setUp(self):
        self.zip_path = "test_l_amat.zip"
        self.extract_path = "test_extracted"
        os.makedirs(self.extract_path, exist_ok=True)

        # Create a test zip file
        with open("test_file.txt", "w") as f:
            f.write("This is a test file.")
        with zipfile.ZipFile(self.zip_path, 'w') as zip_ref:
            zip_ref.write("test_file.txt")

    def tearDown(self):
        if os.path.exists(self.zip_path):
            os.remove(self.zip_path)
        if os.path.exists("test_file.txt"):
            os.remove("test_file.txt")
        if os.path.exists(self.extract_path):
            for file in os.listdir(self.extract_path):
                os.remove(os.path.join(self.extract_path, file))
            os.rmdir(self.extract_path)

    def test_extract_zip(self):
        extract_zip(self.zip_path, self.extract_path)
        extracted_files = os.listdir(self.extract_path)
        self.assertIn("test_file.txt", extracted_files)

if __name__ == "__main__":
    unittest.main()
