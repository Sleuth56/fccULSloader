# Changelog

All notable changes to the FCC Tool project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.7.0] - 2025-03-08

### Added
- New `--active-only` command-line option to filter out inactive license records
  - When used with `--update`, only active records are loaded into the database
  - When used alone, it removes inactive records from an existing database
  - Shows a sample of call signs to be deleted and requires confirmation
  - Displays detailed feedback about the deletion process
- Safety features for the `--active-only` option:
  - Confirmation prompts before deleting records
  - Display of the number of inactive records that will be deleted
  - Sample of call signs that will be removed
- Special handling when `--active-only` is used with `--force-download`:
  - Database is completely rebuilt with only active records
  - Skips the check for inactive records in the existing database
- Enhanced `--verbose` option to display related records from all available tables

### Changed
- Improved error handling and user feedback during database operations
- Enhanced documentation with detailed examples for the new features
- Cleaned up console output during index creation and removal for a more professional appearance
- Moved requirements.txt to the src folder for better project organization
- Improved display of coded fields to show full text descriptions (e.g., "operator_class: Amateur Extra (E)" instead of just "operator_class: E")
- Completely redesigned verbose output format:
  - Organized fields into logical groups (license, operator, personal, contact, etc.)
  - Combined related fields on the same line (name components, address details)
  - Used shorthand labels for better space efficiency (UID, ULS#, etc.)
  - Eliminated duplication in related records
  - Used table names as section headers with descriptive titles (e.g., "Entity/Licensee (EN) RECORDS")
  - Displayed multiple related records in a compact tabular format
  - Improved field ordering for better readability (e.g., Attention field above address)
  - Omitted redundant call sign information from related records
  - Grouped related records by their primary HD record for better organization
- Simplified application header to a single line with underline for a cleaner look

### Fixed
- Various minor bug fixes and performance improvements
- Fixed argument processing issue when using `--active-only` with `--force-download`
- Fixed issue where using `--force-download` without `--update` didn't trigger any action
- Fixed Linux executable naming to follow the format "fcc-tool-linux-[version]"

## [1.6.0] - 2025-02-15

### Added
- Initial public release of FCC Tool
- Comprehensive database management features
- Query capabilities for amateur radio call signs
- Search functionality by name and state
- Detailed documentation and examples 