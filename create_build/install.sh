#!/bin/bash
echo "FCC Tool Installer"

# Check for Python installation
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed or not in PATH."
    echo "Please install Python 3.7 or higher."
    exit 1
fi

# Install required packages quietly
echo "Installing dependencies..."
pip3 install -q -r requirements.txt pyinstaller
if [ $? -ne 0 ]; then
    echo "Error: Failed to install dependencies."
    exit 1
fi

# Clean build artifacts but preserve dist folder
rm -rf build/ *.spec &> /dev/null

echo "Building executable..."
python3 create_build/build_executable.py --platform linux --quiet &> /dev/null
if [ $? -ne 0 ]; then
    echo "Error: Failed to build executable."
    exit 1
fi

# Clean up silently but preserve dist folder
echo "Cleaning up build artifacts..."
rm -rf build/ *.spec &> /dev/null
find . -name "__pycache__" -type d -exec rm -rf {} + &> /dev/null
find . -name "*.pyc" -delete &> /dev/null
rm -f fcc-tool-*.pkg fcc-tool-*.manifest warn-fcc-tool-*.txt &> /dev/null

# Double-check that build folder is gone (sometimes it's recreated)
sleep 1
rm -rf build/ &> /dev/null

# Get version from build_executable.py directly
VERSION=$(python3 create_build/build_executable.py --get-version)

echo "Build completed successfully."
echo "Executable: dist/fcc-tool-linux/fcc-tool-${VERSION}" 