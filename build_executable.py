#!/usr/bin/env python3
"""
Build script for creating standalone executables of FCC Tool for multiple platforms
"""

import os
import shutil
import subprocess
import sys
import platform
import argparse

# Define paths
DIST_DIR = "dist"
BUILD_DIR = "build"
SOURCE_DIR = "src"

# Platform-specific settings
PLATFORMS = {
    "windows": {
        "executable_dir": os.path.join(DIST_DIR, "fcc-tool-windows"),
        "icon": os.path.join("resources", "fcc-tool.ico"),
        "separator": ";",
        "extension": ".exe"
    },
    "linux": {
        "executable_dir": os.path.join(DIST_DIR, "fcc-tool-linux"),
        "icon": os.path.join("resources", "fcc-tool.png"),
        "separator": ":",
        "extension": ""
    },
    "macos": {
        "executable_dir": os.path.join(DIST_DIR, "fcc-tool-macos"),
        "icon": os.path.join("resources", "fcc-tool.icns"),
        "separator": ":",
        "extension": ".app"
    }
}

def clean_build_directories():
    """Remove previous build artifacts"""
    print("Cleaning build directories...")
    for directory in [DIST_DIR, BUILD_DIR]:
        if os.path.exists(directory):
            shutil.rmtree(directory)

def install_requirements():
    """Install required packages for building"""
    print("Installing required packages...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

def build_executable(target_platform=None):
    """Build the executable using PyInstaller for the specified platform"""
    if target_platform is None:
        # Detect current platform
        system = platform.system().lower()
        if system == "darwin":
            target_platform = "macos"
        elif system == "windows":
            target_platform = "windows"
        elif system == "linux":
            target_platform = "linux"
        else:
            print(f"Unsupported platform: {system}")
            return False
    
    if target_platform not in PLATFORMS:
        print(f"Unsupported target platform: {target_platform}")
        return False
    
    platform_config = PLATFORMS[target_platform]
    print(f"Building executable for {target_platform}...")
    
    # Create platform-specific output directory
    os.makedirs(platform_config["executable_dir"], exist_ok=True)
    
    # Determine icon file
    icon_option = []
    if os.path.exists(platform_config["icon"]):
        icon_option = ["--icon", platform_config["icon"]]
    
    # Prepare data files with platform-specific separator
    separator = platform_config["separator"]
    data_files = [
        f"--add-data=LICENSE{separator}.",
        f"--add-data=README.md{separator}.",
        f"--add-data=OPTIMIZATIONS.md{separator}."
    ]
    
    # Build command
    cmd = [
        "pyinstaller",
        f"--name=fcc-tool",
        "--onedir",
        "--clean",
        "--noconfirm",
        f"--distpath={platform_config['executable_dir']}",
    ] + icon_option + data_files + ["fcc_tool.py"]
    
    try:
        subprocess.check_call(cmd)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error building executable: {e}")
        return False

def create_directory_structure():
    """Create the final directory structure"""
    print("Creating directory structure...")
    
    # Create source directory if it doesn't exist
    if not os.path.exists(SOURCE_DIR):
        os.makedirs(SOURCE_DIR)
    
    # Copy Python source files to src directory
    for item in os.listdir():
        if item.endswith(".py") and item != "build_executable.py":
            shutil.copy(item, os.path.join(SOURCE_DIR, item))
    
    # Copy modules directory to src
    if os.path.exists("modules"):
        if os.path.exists(os.path.join(SOURCE_DIR, "modules")):
            shutil.rmtree(os.path.join(SOURCE_DIR, "modules"))
        shutil.copytree("modules", os.path.join(SOURCE_DIR, "modules"))
    
    # Copy tests directory to src if it exists
    if os.path.exists("tests"):
        if os.path.exists(os.path.join(SOURCE_DIR, "tests")):
            shutil.rmtree(os.path.join(SOURCE_DIR, "tests"))
        shutil.copytree("tests", os.path.join(SOURCE_DIR, "tests"))
    
    # Copy resources directory to src if it exists
    if os.path.exists("resources"):
        if os.path.exists(os.path.join(SOURCE_DIR, "resources")):
            shutil.rmtree(os.path.join(SOURCE_DIR, "resources"))
        shutil.copytree("resources", os.path.join(SOURCE_DIR, "resources"))

def create_platform_scripts():
    """Create platform-specific installation scripts"""
    print("Creating platform-specific installation scripts...")
    
    # Windows batch file (already created separately)
    
    # Linux shell script
    with open("install.sh", "w") as f:
        f.write("""#!/bin/bash
echo "FCC Tool Installer"
echo "================="
echo

# Check for Python installation
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed or not in PATH."
    echo "Please install Python 3.7 or higher."
    exit 1
fi

echo "Installing required packages..."
pip3 install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "Failed to install required packages."
    exit 1
fi

echo "Building executable..."
python3 build_executable.py --platform linux
if [ $? -ne 0 ]; then
    echo "Failed to build executable."
    exit 1
fi

echo
echo "Installation completed successfully!"
echo "The executable is located in the dist/fcc-tool-linux directory."
echo
echo "You can run the application by executing dist/fcc-tool-linux/fcc-tool/fcc-tool"
echo
""")
    os.chmod("install.sh", 0o755)
    
    # macOS shell script
    with open("install_macos.sh", "w") as f:
        f.write("""#!/bin/bash
echo "FCC Tool Installer for macOS"
echo "==========================="
echo

# Check for Python installation
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed or not in PATH."
    echo "Please install Python 3.7 or higher."
    exit 1
fi

echo "Installing required packages..."
pip3 install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "Failed to install required packages."
    exit 1
fi

echo "Building executable..."
python3 build_executable.py --platform macos
if [ $? -ne 0 ]; then
    echo "Failed to build executable."
    exit 1
fi

echo
echo "Installation completed successfully!"
echo "The executable is located in the dist/fcc-tool-macos directory."
echo
echo "You can run the application by executing the fcc-tool app in dist/fcc-tool-macos/fcc-tool/"
echo
""")
    os.chmod("install_macos.sh", 0o755)

def main():
    """Main build function"""
    parser = argparse.ArgumentParser(description="Build FCC Tool executable")
    parser.add_argument("--platform", choices=["windows", "linux", "macos", "all"], 
                        help="Target platform (default: current platform)")
    parser.add_argument("--skip-clean", action="store_true", 
                        help="Skip cleaning build directories")
    args = parser.parse_args()
    
    if not args.skip_clean:
        clean_build_directories()
    
    install_requirements()
    
    if args.platform == "all":
        # Build for all platforms
        success = True
        for platform_name in PLATFORMS.keys():
            if not build_executable(platform_name):
                success = False
        if not success:
            print("Failed to build executables for all platforms.")
            return 1
    else:
        # Build for specified or current platform
        if not build_executable(args.platform):
            print("Failed to build executable.")
            return 1
    
    create_directory_structure()
    create_platform_scripts()
    
    print("\nBuild completed successfully!")
    if args.platform == "all":
        print("Executables can be found in the following directories:")
        for platform_name, config in PLATFORMS.items():
            print(f"- {platform_name}: {config['executable_dir']}")
    else:
        platform_name = args.platform or platform.system().lower()
        if platform_name == "darwin":
            platform_name = "macos"
        print(f"Executable can be found in the '{PLATFORMS[platform_name]['executable_dir']}' directory")
    
    print("Source code has been organized in the 'src' directory")
    return 0

if __name__ == "__main__":
    sys.exit(main()) 