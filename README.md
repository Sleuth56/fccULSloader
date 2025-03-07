# FCC Tool

A comprehensive utility for managing and querying FCC amateur radio license database files, creating a local SQLite copy of the entire FCC ULS database for offline use.

## Table of Contents

- [Overview](#overview)
- [Author and License](#author-and-license)
- [Features](#features)
  - [Database Management](#database-management)
    - [Downloading and Updating](#downloading-and-updating)
    - [Maintenance and Optimization](#maintenance-and-optimization)
  - [Query Capabilities](#query-capabilities)
    - [Call Sign Lookup](#call-sign-lookup)
    - [Name Search](#name-search)
    - [State Filtering](#state-filtering)
    - [Combined Searches](#combined-searches)
- [Installation](#installation)
- [Usage](#usage)
  - [Command Line Options](#command-line-options)
  - [Examples](#examples)
- [Configuration](#configuration)
- [Technical Details](#technical-details)
  - [Directory Structure](#directory-structure)
  - [Database Schema](#database-schema)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

## Overview

FCC Tool is a command-line application that creates and maintains a complete local SQLite copy of the FCC Amateur Radio License database. This allows you to develop applications that can look up any callsign, entity, or license name without requiring internet connectivity. The tool provides functionality to download and update the database from the [FCC's Universal Licensing System (ULS)](https://www.fcc.gov/wireless/universal-licensing-system), look up amateur radio call signs, search for licensees by name or state, and maintain the database for optimal performance.

The offline nature of this tool makes it particularly valuable for amateur radio operators in the field, emergency communications scenarios, or any situation where internet access may be limited or unavailable.

## Author and License

**Author:** Tiran Dagan (Backstop Radio)  
**Contact:** tiran@tirandagan.com  
**License:** MIT License

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

## Features

### Database Management

#### Downloading and Updating

FCC Tool can automatically download and update the FCC amateur radio license database from the [FCC's ULS database downloads page](https://www.fcc.gov/uls/transactions/daily-weekly). The tool checks for updates by comparing the last modified date of the remote file with your local copy, ensuring you only download new data when it's available.

Key features:

- **Automatic update detection**: Checks if a new version is available before downloading
- **Efficient data processing**: Downloads, extracts, and loads data into an SQLite database
- **Index creation**: Automatically creates optimized indexes for fast searching
- **Cleanup**: Removes temporary files after processing to save disk space

#### Maintenance and Optimization

The tool provides several options for maintaining and optimizing the database:

- **Compaction**: Reclaims unused space in the database file
- **Optimization**: Removes unused tables and columns to reduce database size
- **Index rebuilding**: Rebuilds database indexes to improve search performance

### Query Capabilities

#### Call Sign Lookup

The primary function of FCC Tool is to look up FCC license information by call sign. This retrieves all available information for a specific amateur radio call sign from the database.

#### Name Search

You can search for FCC license records by name using a case-insensitive wildcard search that matches names in any position. This is useful for finding all licenses associated with a particular person or organization.

#### State Filtering

The tool allows you to search for records by state using the two-letter state code. This is helpful for finding all licensees in a specific geographic area.

#### Combined Searches

You can combine name and state filters to perform more targeted searches, such as finding all licensees with a specific name in a particular state.

## Installation

### Option 1: Using the Executable (Recommended)

FCC Tool is available as a standalone executable for Windows, Linux, and macOS. This is the easiest way to get started.

#### Windows

1. **Download the latest release** from the [Releases page](https://github.com/tirandagan/fccULSloader/releases).
2. **Extract the ZIP file** to a location of your choice.
3. **Run the executable** (`fcc-tool.exe`) from the extracted folder.

#### Linux

1. **Download the latest release** from the [Releases page](https://github.com/tirandagan/fccULSloader/releases).
2. **Extract the tarball**:
   ```
   tar -xzf fcc-tool-linux.tar.gz
   ```
3. **Make the executable file executable**:
   ```
   chmod +x fcc-tool-linux/fcc-tool/fcc-tool
   ```
4. **Run the executable**:
   ```
   ./fcc-tool-linux/fcc-tool/fcc-tool
   ```

#### macOS

1. **Download the latest release** from the [Releases page](https://github.com/tirandagan/fccULSloader/releases).
2. **Extract the ZIP file** to a location of your choice.
3. **Run the application** by double-clicking the `fcc-tool` app in the extracted folder.

### Option 2: Building from Source

If you prefer to build the executable from source, follow these steps:

#### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

#### Windows

1. **Clone the repository**:
   ```
   git clone https://github.com/tirandagan/fccULSloader.git
   cd fccULSloader
   ```

2. **Run the installer script**:
   ```
   install.bat
   ```

3. **Run the executable**:
   ```
   dist\fcc-tool-windows\fcc-tool\fcc-tool.exe
   ```

#### Linux

1. **Clone the repository**:
   ```
   git clone https://github.com/tirandagan/fccULSloader.git
   cd fccULSloader
   ```

2. **Run the installer script**:
   ```
   ./install.sh
   ```

3. **Run the executable**:
   ```
   ./dist/fcc-tool-linux/fcc-tool/fcc-tool
   ```

#### macOS

1. **Clone the repository**:
   ```
   git clone https://github.com/tirandagan/fccULSloader.git
   cd fccULSloader
   ```

2. **Run the installer script**:
   ```
   ./install_macos.sh
   ```

3. **Run the executable**:
   ```
   open ./dist/fcc-tool-macos/fcc-tool/fcc-tool.app
   ```

### Option 3: Running from Python Source

You can also run the application directly from the Python source code:

1. **Clone the repository**:
   ```
   git clone https://github.com/tirandagan/fccULSloader.git
   cd fccULSloader
   ```

2. **Install dependencies**:
   ```
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```
   python fcc_tool.py
   ```

## Project Structure

The project is organized as follows:

```
fcc-tool/
├── src/                  # Source code directory
│   ├── fcc_tool.py       # Main application script
│   ├── modules/          # Application modules
│   └── tests/            # Test files
├── dist/                 # Distribution directory (created during build)
│   ├── fcc-tool-windows/ # Windows executable
│   ├── fcc-tool-linux/   # Linux executable
│   └── fcc-tool-macos/   # macOS executable
├── resources/            # Application resources
├── build_executable.py   # Script to build executables
├── install.bat           # Windows installation script
├── install.sh            # Linux installation script
├── install_macos.sh      # macOS installation script
├── README.md             # This documentation
└── requirements.txt      # Python dependencies
```

## Usage

### Command Line Options

FCC Tool provides a comprehensive set of command-line options for database management and querying:

#### Database Management Options

| Option | Description |
|--------|-------------|
| `--update` | Check for and download updates to the FCC database |
| `--force-download` | Force download even if data is up to date |
| `--skip-download` | Skip download and use existing data files |
| `--check-update` | Check if an update is available without downloading |
| `--keep-files` | Keep downloaded and extracted files after processing |
| `--quiet` | Suppress INFO log messages (only show WARNING and above) |
| `--compact` | Compact the database to reduce file size |
| `--optimize` | Remove unused tables and compact the database |
| `--rebuild-indexes` | Rebuild database indexes to improve search performance |

#### Query Options

| Option | Description |
|--------|-------------|
| `--callsign CALLSIGN` | Look up a specific amateur radio call sign |
| `--name NAME` | Search for records by name (case-insensitive wildcard search) |
| `--state STATE` | Filter records by two-letter state code (e.g., CA, NY, TX) |
| `--verbose` | Display all fields for each record |

### Examples

#### Database Management

Update the database with the latest data from the FCC:
```
python fcc_tool.py --update
```

Force a new download regardless of whether the data is up to date:
```
python fcc_tool.py --force-download
```

Check if an update is available without downloading:
```
python fcc_tool.py --check-update
```

Optimize the database to reduce its size:
```
python fcc_tool.py --optimize
```

Rebuild indexes to improve search performance:
```
python fcc_tool.py --rebuild-indexes
```

#### Queries

Look up a specific call sign:
```
python fcc_tool.py --callsign W1AW
```

Search for records by name:
```
python fcc_tool.py --name "Smith"
```

Search for records in a specific state:
```
python fcc_tool.py --state CA
```

Combine name and state search:
```
python fcc_tool.py --name "Smith" --state TX
```

Display detailed information for search results:
```
python fcc_tool.py --name "Smith" --verbose
```

## Configuration

The database path and other configuration settings are defined in the `modules/config.py` file. You can modify these settings to customize the tool's behavior:

- `DB_PATH`: Path to the SQLite database file
- `DATA_PATH`: Directory for storing data files
- `ZIP_FILE_URL`: URL for downloading the FCC database
- `TABLES_TO_PROCESS`: List of tables to process during data loading

## Technical Details

### Directory Structure

The application is organized into the following structure:

```
fcc-tool/
├── fcc_tool.py           # Main application script
├── README.md             # This documentation
├── requirements.txt      # Python dependencies
├── FCC_DATABASE_DOC.md   # Detailed database documentation
├── data/                 # Data directory (created automatically)
│   ├── fcc_data.db       # SQLite database
│   └── fcc_metadata.json # Metadata about the last download
├── logs/                 # Log directory (created automatically)
│   └── fcc_tool.log      # Application log file
└── modules/              # Application modules
    ├── config.py         # Configuration settings
    ├── database.py       # Database operations
    ├── downloader.py     # File downloading
    ├── extractor.py      # File extraction
    ├── fcc_code_defs.py  # FCC code definitions
    ├── filesystemtools.py # File system operations
    ├── loader.py         # Data loading
    ├── logger.py         # Logging configuration
    ├── schemas.py        # Database schemas
    └── updater.py        # Update process management
```

### Database Schema

The FCC database contains multiple tables with information about amateur radio licenses. The primary tables used by FCC Tool are:

- `HD`: License header information (call sign, license status, etc.)
- `EN`: Entity information (name, address, etc.)
- `AM`: Amateur license information (operator class, etc.)
- `HS`: License history information
- `CO`: Comments associated with licenses
- `LA`: License attachments
- `SC`: Special conditions
- `SF`: Special free form conditions

For detailed information about the FCC database structure, tables, fields, and their meanings, please refer to the [FCC Database Documentation](FCC_DATABASE_DOC.md) included in this repository.

The FCC data is sourced from the [FCC's ULS database downloads page](https://www.fcc.gov/uls/transactions/daily-weekly), specifically the Amateur Radio Service database file (`l_amat.zip`).

## Troubleshooting

### Common Issues

- **Database not found**: Run `python fcc_tool.py --update` to download and create the database.
- **Slow searches**: Run `python fcc_tool.py --rebuild-indexes` to optimize search performance.
- **Large database size**: Run `python fcc_tool.py --optimize` to reduce the database size.
- **Download errors**: Check your internet connection and try again with `python fcc_tool.py --force-download`.

### Logs

The application logs are stored in the `logs/fcc_tool.log` file. If you encounter issues, check this file for detailed error messages and debugging information.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request or open an Issue on GitHub.

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request
