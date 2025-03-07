"""
FCC Tool - FCC Amateur Radio License Database Management Tool
============================================================

Author: Tiran Dagan (Backstop Radio)
Contact: tiran@tirandagan.com
License: MIT License

Copyright (c) 2025 Tiran Dagan

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Description:
-----------
This script provides a unified command-line interface for managing and querying the FCC Amateur Radio
License database. It combines database management and query functionality in a single tool.

Features:
--------
1. Database Management:
   - Download and update the FCC database from the official source
   - Compact the database to reduce file size
   - Optimize the database by removing unused tables and columns
   - Rebuild indexes to improve search performance

2. Database Queries:
   - Look up amateur radio call signs
   - Search for records by name (case-insensitive wildcard search)
   - Search for records by state
   - Combine name and state filters for more specific searches
   - Display detailed or summarized information

Functions:
---------
- signal_handler(sig, frame): Handles interrupt signals during long-running operations
- main(): Main function that parses command-line arguments and executes the appropriate action

Usage:
-----
The tool uses modules from the 'modules' directory:
- config: Configuration settings
- database: Database operations (FCCDatabase class)
- updater: Database update functionality
- logger: Logging configuration
- filesystemtools: File system operations

Command Line Options:
-------------------
Database Management:
  --update                : Check for and download updates to the FCC database
  --force-download        : Force download even if data is up to date
  --skip-download         : Skip download and use existing data files
  --check-update          : Check if an update is available without downloading
  --keep-files            : Keep downloaded and extracted files after processing
  --quiet                 : Suppress INFO log messages (only show WARNING and above)
  --compact               : Compact the database to reduce file size
  --optimize              : Remove unused tables and compact the database
  --rebuild-indexes       : Rebuild database indexes to improve search performance

Queries:
  --callsign CALLSIGN     : Look up a specific amateur radio call sign
  --name NAME             : Search for records by name (case-insensitive wildcard search)
  --state STATE           : Filter records by two-letter state code (e.g., CA, NY, TX)
  --verbose               : Display all fields for each record

Examples:
--------
python fcc_tool.py --update
python fcc_tool.py --callsign W1AW
python fcc_tool.py --name "Smith"
python fcc_tool.py --state CA
python fcc_tool.py --name "Smith" --state TX
python fcc_tool.py --compact
python fcc_tool.py --optimize
"""

import argparse
import signal
import logging
import sys
import os
from modules import config, fcc_code_defs
from modules import updater, logger
from modules.database import FCCDatabase
from modules.filesystemtools import ensure_directory

# Version information
__version__ = "1.6.0"
APP_NAME = "FCC Tool"

# Utility functions

def display_header():
    """
    Display a nice framed header with program name, copyright, and version information.
    """
    terminal_width = 80
    try:
        # Try to get the terminal width on supported platforms
        if sys.platform != "win32":
            import shutil
            terminal_width = shutil.get_terminal_size().columns
        else:
            # On Windows, try to use os.get_terminal_size
            terminal_width = os.get_terminal_size().columns
    except (ImportError, AttributeError, OSError):
        # Fall back to default width if we can't get the terminal width
        pass
    
    # Ensure minimum width
    terminal_width = max(terminal_width, 60)
    
    # Create the header content
    header_lines = [
        f"{APP_NAME} v{__version__}",
        f"Copyright © 2025 Tiran Dagan (Backstop Radio)",
        "All rights reserved."
    ]
    
    # Calculate the box width (content + padding)
    content_width = max(len(line) for line in header_lines)
    box_width = min(content_width + 4, terminal_width)
    
    # Create the box
    horizontal_line = "+" + "-" * (box_width - 2) + "+"
    empty_line = "|" + " " * (box_width - 2) + "|"
    
    # Print the header
    print(horizontal_line)
    print(empty_line)
    for line in header_lines:
        padding = (box_width - 2 - len(line)) // 2
        print("|" + " " * padding + line + " " * (box_width - 2 - padding - len(line)) + "|")
    print(empty_line)
    print(horizontal_line)
    print()

def signal_handler(sig, frame):
    """
    Handle interrupt signals (Ctrl+C) during long-running operations.
    
    Args:
        sig: Signal number
        frame: Current stack frame
    """
    print("\nProcess interrupted. Press ESC again to exit or any other key to continue.")
    key = input()
    if key.lower() == 'esc':
        print("Exiting. The data might be corrupt.")
        logging.warning("Process interrupted by user. Exiting. The data might be corrupt.")
        sys.exit(0)
    else:
        print("Resuming process.")

def main():
    """
    Main function that parses command-line arguments and executes the appropriate action.
    """
    # Display the header
    display_header()
    
    # Set up signal handler for Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)
    
    # Set up logging
    logger.setup_logging(verbose=False)
    
    # Create argument parser
    parser = argparse.ArgumentParser(
        description="FCC Tool - FCC Amateur Radio License Database Management Tool",
        epilog="For more information, see the README.md file."
    )
    
    # Create argument groups for better organization
    db_group = parser.add_argument_group('Database Management')
    query_group = parser.add_argument_group('Queries')
    
    # Database Management options
    db_group.add_argument('--update', action='store_true', 
                         help='Check for and download updates to the FCC database')
    db_group.add_argument('--force-download', action='store_true', 
                         help='Force download even if data is up to date')
    db_group.add_argument('--skip-download', action='store_true', 
                         help='Skip download and use existing data files')
    db_group.add_argument('--check-update', action='store_true', 
                         help='Check if an update is available without downloading')
    db_group.add_argument('--keep-files', action='store_true', 
                         help='Keep downloaded and extracted files after processing')
    db_group.add_argument('--quiet', action='store_true', 
                         help='Suppress INFO log messages (only show WARNING and above)')
    db_group.add_argument('--compact', action='store_true', 
                         help='Compact the database to reduce file size')
    db_group.add_argument('--optimize', action='store_true', 
                         help='Remove unused tables and compact the database')
    db_group.add_argument('--rebuild-indexes', action='store_true', 
                         help='Rebuild database indexes to improve search performance')
    
    # Query options
    query_group.add_argument('--callsign', metavar='CALLSIGN', 
                            help='Look up a specific amateur radio call sign')
    query_group.add_argument('--name', metavar='NAME', 
                            help='Search for records by name (case-insensitive wildcard search)')
    query_group.add_argument('--state', metavar='STATE', 
                            help='Filter records by two-letter state code (e.g., CA, NY, TX)')
    query_group.add_argument('--verbose', action='store_true', 
                            help='Display all fields for each record')
    
    # Parse arguments
    args = parser.parse_args()
    
    # Get database path from config
    db_path = config.Config.DB_PATH
    
    # Create database object
    db = FCCDatabase(db_path)
    
    # Ensure data directory exists
    ensure_directory('data')
    
    # If quiet mode is enabled, set log level to WARNING
    if args.quiet:
        logger.set_log_level(logging.WARNING)
    
    # Handle database management options
    
    # Check for update
    if args.check_update:
        update_available = updater.check_for_update()
        if update_available:
            print("A new version of the FCC data is available.")
        else:
            print("The FCC data is up to date.")
        return
    
    # Update database
    if args.update:
        print("Checking for updates to the FCC database...")
        
        # Add debugging information for update issues
        metadata_file = os.path.join(config.Config.DATA_PATH, "fcc_metadata.json")
        print(f"Metadata file exists: {os.path.exists(metadata_file)}")
        print(f"Database exists: {db.database_exists()}")
        print(f"Force download: {args.force_download}")
        
        try:
            updater.update_data(
                skip_download=args.skip_download,
                keep_files=args.keep_files,
                force_download=args.force_download,
                quiet=args.quiet
            )
        except Exception as e:
            logging.error(f"Error during update process: {e}")
            print(f"Error: {e}")
        return
    
    # Rebuild indexes
    if args.rebuild_indexes:
        print("Rebuilding database indexes...")
        if not db.database_exists():
            print("Error: Database does not exist. Please run with --update first.")
            return
        db.rebuild_indexes()
        return
    
    # Optimize database
    if args.optimize:
        print("Optimizing database...")
        if not db.database_exists():
            print("Error: Database does not exist. Please run with --update first.")
            return
        db.optimize_database()
        return
    
    # Compact database
    if args.compact:
        print("Compacting database...")
        if not db.database_exists():
            print("Error: Database does not exist. Please run with --update first.")
            return
        db.compact_database()
        return
    
    # Check if database exists before performing queries
    if not db.database_exists() and (args.callsign or args.name or args.state):
        print("Error: Database does not exist. Please run with --update first.")
        return
    
    # Handle query options
    
    # Search by name and state
    if args.name and args.state:
        records = db.search_records_by_name_and_state(args.name, args.state)
        if records:
            print(f"Found {len(records)} records matching name: {args.name} in state: {args.state.upper()}")
            for record in records:
                if args.verbose:
                    db.display_verbose_record(record)
                else:
                    FCCDatabase.display_record(record)
        else:
            print(f"No records found matching name: {args.name} in state: {args.state.upper()}")
        return
    
    # Search by name only
    if args.name:
        records = db.search_records_by_name(args.name)
        if records:
            print(f"Found {len(records)} records matching name: {args.name} (case-insensitive)")
            for record in records:
                if args.verbose:
                    db.display_verbose_record(record)
                else:
                    FCCDatabase.display_record(record)
        else:
            print(f"No records found matching name: {args.name} (case-insensitive)")
        return
    
    # Search by state only
    if args.state:
        records = db.search_records_by_state(args.state)
        if records:
            print(f"Found {len(records)} records in state: {args.state.upper()}")
            for record in records:
                if args.verbose:
                    db.display_verbose_record(record)
                else:
                    FCCDatabase.display_record(record)
        else:
            print(f"No records found in state: {args.state.upper()}")
        return
    
    # Look up call sign
    if args.callsign:
        call_sign = args.callsign.upper()  # Convert the call sign to uppercase
        record = db.get_record_by_call_sign(call_sign)
        
        if record:
            if args.verbose:
                db.display_verbose_record(record)
            else:
                # Add call sign to the record for display
                record['call_sign'] = call_sign
                FCCDatabase.display_record(record)
        else:
            print(f"No record found for call sign: {call_sign}")
        return
    
    # If we get here, no valid options were provided
    if not any([args.callsign, args.name, args.state, args.update, args.check_update, 
                args.compact, args.optimize, args.rebuild_indexes]):
        parser.print_help()
        print("\nError: No valid options provided. Please specify at least one option.")
        return

if __name__ == "__main__":
    main()
