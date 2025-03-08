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

### Changed
- Improved error handling and user feedback during database operations
- Enhanced documentation with detailed examples for the new features
- Cleaned up console output during index creation and removal for a more professional appearance

### Fixed
- Various minor bug fixes and performance improvements
- Fixed argument processing issue when using `--active-only` with `--force-download`
- Fixed issue where using `--force-download` without `--update` didn't trigger any action

## [1.6.0] - 2025-02-15

### Added
- Initial public release of FCC Tool
- Comprehensive database management features
- Query capabilities for amateur radio call signs
- Search functionality by name and state
- Detailed documentation and examples 