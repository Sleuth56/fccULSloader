# FCC Tool

A comprehensive utility for managing and querying FCC amateur radio license database files, creating a local SQLite copy of the entire FCC ULS database for offline use. Includes both a command-line interface and a modern web interface.

## Table of Contents 📑

- [Overview](#overview)
- [Author and License](#author-and-license)
- [Features](#features)
  - [Web Interface](#web-interface)
  - [Database Management](#database-management)
  - [Query Capabilities](#query-capabilities)
- [Installation](#installation)
- [Usage](#usage)
  - [Web Interface](#using-the-web-interface)
  - [Command Line Options](#command-line-options)
  - [Examples](#examples)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Database Documentation](#database-documentation)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [Changelog](#changelog)

## Overview

FCC Tool is a command-line and web application that creates and maintains a complete local SQLite copy of the FCC Amateur Radio License database. This allows you to develop applications that can look up any callsign, entity, or license name without requiring internet connectivity. The tool provides functionality to download and update the database from the [FCC's Universal Licensing System (ULS)](https://www.fcc.gov/wireless/universal-licensing-system), look up amateur radio call signs, search for licensees by name or state, and maintain the database for optimal performance.

The offline nature of this tool makes it particularly valuable for amateur radio operators in the field, emergency communications scenarios, or any situation where internet access may be limited or unavailable.


[↑ Back to Table of Contents](#table-of-contents-)

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

[↑ Back to Table of Contents](#table-of-contents-)

## Features

### Web Interface
**[[Features](#features) > Web Interface]**

FCC Tool includes a modern, responsive web interface (`fcc_tool_web.py`) that provides an elegant way to search and view FCC amateur radio license data:

#### Search Interface
- **Clean, Modern Design**: A beautiful, intuitive search interface
- **Multiple Search Options**: 
  - Callsign lookup (e.g., W1AW)
  - Name search (partial or full)
  - State filtering with searchable dropdown
- **Keyboard Shortcuts**: Quick navigation using Alt + C/N/S
- **Search Tips**: Built-in help and search suggestions
- **Recent Searches**: Track and quickly access your recent searches

![Main Search Interface](docs/screenshots/main_search.jpg)
*Clean, modern search interface with keyboard shortcuts and search tips*

#### Search Results
- **Flexible Views**: 
  - Table view for compact listing
  - Card view for detailed information
- **Advanced Filtering**:
  - License status (Active/Inactive)
  - License class (Extra, General, Technician)
  - Sort by various fields
- **Pagination**: Browse through large result sets
- **Quick Actions**: Direct access to detailed profiles

![Search Results](docs/screenshots/search_results.jpg)
*Search results with advanced filtering and sorting options*

#### Profile View
- **Detailed Information**: Comprehensive license details
- **Interactive Map**: View licensee location
- **Personal Information**: Entity details and contact info
- **License Details**: Status, class, dates, and more
- **Dark Mode**: Toggle between light and dark themes
- **Responsive Design**: Works on desktop and mobile

![Profile View](docs/screenshots/profile_view.jpg)
*Detailed profile view with interactive map and comprehensive license information*

The web interface is built with:
- Flask for the backend
- Bootstrap 5 for responsive design
- Leaflet.js for interactive maps
- Modern CSS with animations and transitions
- Session management for recent searches
- Real-time search filtering

[↑ Back to Table of Contents](#table-of-contents-)

### Database Management
**[[Features](#features) > Database Management]**

FCC Tool can automatically download and update the FCC amateur radio license database from the [FCC's ULS database downloads page](https://www.fcc.gov/uls/transactions/daily-weekly). The tool checks for updates by comparing the last modified date of the remote file with your local copy, ensuring you only download new data when it's available.

Key features:

- **Automatic update detection**: Checks if a new version is available before downloading
- **Efficient data processing**: Downloads, extracts, and loads data into an SQLite database
- **Optimized data loading**: Uses temporary tables and bulk operations for fast data loading
- **Index creation**: Automatically creates optimized indexes for fast searching
- **Cleanup**: Removes temporary files after processing to save disk space

The tool also provides several options for maintaining and optimizing the database:

- **Compaction**: Reclaims unused space in the database file
- **Optimization**: Removes unused tables and columns to reduce database size
- **Index rebuilding**: Rebuilds database indexes to improve search performance

[↑ Back to Table of Contents](#table-of-contents-)

### Query Capabilities
**[[Features](#features) > Query Capabilities]**

#### Call Sign Lookup

The primary function of FCC Tool is to look up FCC license information by call sign. This retrieves all available information for a specific amateur radio call sign from the database.

#### Name Search

You can search for FCC license records by name using a case-insensitive wildcard search that matches names in any position. This is useful for finding all licenses associated with a particular person or organization.

#### State Filtering

The tool allows you to search for records by state using the two-letter state code. This is helpful for finding all licensees in a specific geographic area.

#### Combined Searches

You can combine name and state filters to perform more targeted searches, such as finding all licensees with a specific name in a particular state.

[↑ Back to Table of Contents](#table-of-contents-)

## Installation

FCC Tool can be run directly from Python source or as a standalone executable. For detailed instructions on building and running the application, see the [Build Documentation](create_build/README.md).

### Quick Start

#### Running from Python Source

```bash
# Install dependencies
pip install -r requirements.txt

# Run the CLI application
python fcc_tool.py --help

# Run the web interface
python fcc_tool_web.py
```

The web interface requires additional Python packages:
- Flask
- Flask-Session
- Leaflet.js (included via CDN)

These are all included in requirements.txt.

#### Using Pre-built Executables

Download the latest release from the [Releases page](https://github.com/tirandagan/fccULSloader/releases) for your platform (Windows, Linux, or macOS).

[↑ Back to Table of Contents](#table-of-contents-)

## Usage

### Using the Web Interface
**[[Usage](#usage) > Web Interface]**

To start the web interface:

```bash
python src/fcc_tool_web.py
```

This will start a Flask web server on port 5000. You can then access the web interface by opening a web browser and navigating to:

```
http://localhost:5000
```

The web interface provides:

1. **Search Options**:
   - Search by callsign (e.g., W1AW)
   - Search by name (partial or full)
   - Filter by state
   
2. **Advanced Filtering**:
   - License status (Active/Inactive)
   - License class (Extra, General, Technician)
   - Sort results by various fields
   
3. **Keyboard Shortcuts**:
   - Alt + C: Focus callsign field
   - Alt + N: Focus name field
   - Alt + S: Focus state field
   - Ctrl + T: Toggle dark/light theme

4. **View Options**:
   - Table view for compact listing
   - Card view for detailed information
   - Interactive map view for location data

### Command Line Options
**[[Usage](#usage) > Command Line Options]**

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
| `--active-only` | Only keep active license records (license_status="A") in the database. Requires confirmation before deleting records |

#### Query Options

| Option | Description |
|--------|-------------|
| `--callsign CALLSIGN` | Look up a specific amateur radio call sign |
| `--name NAME` | Search for records by name (case-insensitive wildcard search) |
| `--state STATE` | Filter records by two-letter state code (e.g., CA, NY, TX) |
| `--verbose` | Display all fields for each record, including related records from other tables |

[↑ Back to Table of Contents](#table-of-contents-)

### Examples
**[[Usage](#usage) > Examples]**

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

Update the database and only keep active license records:
```
python fcc_tool.py --update --active-only
```

Force a complete database rebuild with only active license records:
```
python fcc_tool.py --force-download --active-only
```

Filter an existing database to only keep active license records:
```
python fcc_tool.py --active-only
```

When using the `--active-only` option, the tool will:
1. Display the number of inactive records that will be deleted
2. Show a sample of call signs that will be removed
3. Ask for confirmation before proceeding with the deletion

This safety feature ensures you don't accidentally delete records you might need.

When using `--active-only` with `--force-download`, the database will be completely rebuilt with only active records, skipping the check for inactive records in the existing database.

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

[↑ Back to Table of Contents](#table-of-contents-)

## Project Structure

The project is organized as follows:

```
fcc-tool/
├── src/                  # Source code directory
│   ├── fcc_tool.py       # Main CLI application script
│   ├── fcc_tool_web.py   # Web interface application
│   ├── flask_session/    # Flask session storage
│   │   ├── css/         # Stylesheets
│   │   ├── js/          # JavaScript files
│   │   └── img/         # Images and icons
│   ├── modules/          # Application modules
│   └── tests/           # Test files
├── create_build/         # Build scripts and tools
│   ├── build_executable.py  # Main build script
│   ├── simple_build.py   # Simplified build script
│   ├── install.bat       # Windows installation script
│   ├── install.sh        # Linux installation script
│   └── install_macos.sh  # macOS installation script
├── dist/                 # Distribution directory (created during build)
│   ├── fcc-tool-windows/ # Windows executable
│   ├── fcc-tool-linux/   # Linux executable
│   └── fcc-tool-macos/   # macOS executable
├── resources/            # Application resources
├── README.md             # This documentation
├── FCC_DATABASE_DOC.md   # Detailed database documentation
├── run.bat               # Windows run script
├── run.sh                # Linux/macOS run script
└── requirements.txt      # Python dependencies
```

When running the application, additional directories are created:

```
fcc-tool/
├── data/                 # Data directory (created automatically)
│   ├── fcc_data.db       # SQLite database
│   └── fcc_metadata.json # Metadata about the last download
└── logs/                 # Log directory (created automatically)
    └── fcc_tool.log      # Application log file
```

[↑ Back to Table of Contents](#table-of-contents-)

## Configuration

The database path and other configuration settings are defined in the `modules/config.py` file. You can modify these settings to customize the tool's behavior:

- `DB_PATH`: Path to the SQLite database file
- `DATA_PATH`: Directory for storing data files
- `ZIP_FILE_URL`: URL for downloading the FCC database
- `TABLES_TO_PROCESS`: List of tables to process during data loading

[↑ Back to Table of Contents](#table-of-contents-)

## Database Documentation

The FCC database contains multiple tables with information about amateur radio licenses. The primary tables used by FCC Tool are:

- `HD`: License header information (call sign, license status, etc.)
- `EN`: Entity information (name, address, etc.)
- `AM`: Amateur license information (operator class, etc.)
- `HS`: License history information
- `CO`: Comments associated with licenses
- `LA`: License attachments
- `SC`: Special conditions
- `SF`: Special free form conditions

> I created a detailed information about the FCC database structure, tables, fields, and their meanings, see the [FCC Database Documentation](FCC_DATABASE_DOC.md).

The FCC data is sourced from the [FCC's ULS database downloads page](https://www.fcc.gov/uls/transactions/daily-weekly), specifically the Amateur Radio Service database file (`l_amat.zip`).

**[📄 View Complete FCC Database Documentation](FCC_DATABASE_DOC.md)**

[↑ Back to Table of Contents](#table-of-contents-)

## Troubleshooting

### Common Issues

- **Database not found**: Run `python fcc_tool.py --update` to download and create the database.
- **Slow searches**: Run `python fcc_tool.py --rebuild-indexes` to optimize search performance.
- **Large database size**: Run `python fcc_tool.py --optimize` to reduce the database size.
- **Download errors**: Check your internet connection and try again with `python fcc_tool.py --force-download`.

### Logs

The application logs are stored in the `logs/fcc_tool.log` file. If you encounter issues, check this file for detailed error messages and debugging information.

[↑ Back to Table of Contents](#table-of-contents-)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request or open an Issue on GitHub.

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request

[↑ Back to Table of Contents](#table-of-contents-)

## Changelog

For a detailed list of changes between versions, please see the [CHANGELOG.md](CHANGELOG.md) file.

The current version is 1.7.0, which adds the `--active-only` feature to filter out inactive license records.

[↑ Back to Table of Contents](#table-of-contents-)