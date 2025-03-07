"""
FCC ULS Downloader and Loader
Author: Tiran Dagan
Contact: tiran@tirandagan.com

Description: Unit tests for logger module.
"""

import unittest
import logging
from modules.logger import configure_logging

class TestLogger(unittest.TestCase):
    def test_configure_logging(self):
        configure_logging(verbose=True)
        logger = logging.getLogger()
        self.assertEqual(logger.level, logging.DEBUG)

        configure_logging(verbose=False)
        logger = logging.getLogger()
        self.assertEqual(logger.level, logging.INFO)

if __name__ == "__main__":
    unittest.main()
