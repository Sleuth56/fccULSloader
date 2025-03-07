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
import importlib.util

# Define paths
DIST_DIR = "dist"
BUILD_DIR = "build"
SOURCE_DIR = "src"

# Import version from fcc_tool.py
def get_version():
    """Get version from fcc_tool.py"""
    try:
        # Try to import from src directory first
        if os.path.exists(os.path.join(SOURCE_DIR, "fcc_tool.py")):
            spec = importlib.util.spec_from_file_location("fcc_tool", os.path.join(SOURCE_DIR, "fcc_tool.py"))
            fcc_tool = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(fcc_tool)
            return fcc_tool.__version__
        # Fall back to root directory
        elif os.path.exists("fcc_tool.py"):
            spec = importlib.util.spec_from_file_location("fcc_tool", "fcc_tool.py")
            fcc_tool = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(fcc_tool)
            return fcc_tool.__version__
        else:
            return "1.5.0"  # Default version if fcc_tool.py not found
    except (ImportError, AttributeError):
        return "1.5.0"  # Default version if import fails

VERSION = get_version()
print(f"Building FCC Tool version {VERSION}")

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

def build_executable(target_platform=None, quiet=False):
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
            if not quiet:
                print(f"Unsupported platform: {system}")
            return False
    
    if target_platform not in PLATFORMS:
        if not quiet:
            print(f"Unsupported target platform: {target_platform}")
        return False
    
    platform_config = PLATFORMS[target_platform]
    if not quiet:
        print(f"Building FCC Tool version {VERSION} for {target_platform}...")
    
    # Create platform-specific output directory
    os.makedirs(platform_config["executable_dir"], exist_ok=True)
    
    # Determine icon file
    icon_option = []
    if os.path.exists(platform_config["icon"]):
        icon_option = ["--icon", platform_config["icon"]]
    
    # Prepare data files with platform-specific separator
    separator = platform_config["separator"]
    data_files = []
    
    # Check if files exist before adding them to the command
    file_list = [
        ("LICENSE", "LICENSE"),
        ("README.md", "README.md"),
        ("OPTIMIZATIONS.md", "OPTIMIZATIONS.md"),
        ("FCC_DATABASE_DOC.md", "FCC_DATABASE_DOC.md")
    ]
    
    for src_file, dest_name in file_list:
        if os.path.exists(src_file):
            data_files.append(f"--add-data={src_file}{separator}.")
        elif not quiet:
            print(f"Warning: {src_file} not found, it will not be included in the executable")
    
    # Determine the path to fcc_tool.py
    if os.path.exists(os.path.join(SOURCE_DIR, "fcc_tool.py")):
        fcc_tool_path = os.path.join(SOURCE_DIR, "fcc_tool.py")
        # Add modules directory if using source directory
        modules_path = os.path.join(SOURCE_DIR, "modules")
    elif os.path.exists("fcc_tool.py"):
        fcc_tool_path = "fcc_tool.py"
        # Add modules directory from root
        modules_path = "modules"
    else:
        if not quiet:
            print("Error: fcc_tool.py not found in src directory or root directory")
        return False
    
    if not quiet:
        print(f"Using source file: {fcc_tool_path}")
        print(f"Using modules path: {modules_path}")
    
    # Build command - using --onefile instead of --onedir for a single executable
    cmd = [
        "pyinstaller",
        f"--name=fcc-tool-{VERSION}",  # Include version in name
        "--onefile",  # Changed from --onedir to --onefile
        "--clean",
        "--noconfirm",
        f"--distpath={platform_config['executable_dir']}",
        "--hidden-import=modules.config",
        "--hidden-import=modules.database",
        "--hidden-import=modules.updater",
        "--hidden-import=modules.logger",
        "--hidden-import=modules.filesystemtools",
        "--hidden-import=modules.fcc_code_defs",
        f"--add-data={modules_path}{separator}modules",
    ] + icon_option + data_files + [fcc_tool_path]
    
    try:
        if quiet:
            # Redirect output to devnull if quiet mode is enabled
            with open(os.devnull, 'w') as devnull:
                subprocess.check_call(cmd, stdout=devnull, stderr=devnull)
        else:
            subprocess.check_call(cmd)
        return True
    except subprocess.CalledProcessError as e:
        if not quiet:
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
echo "You can run the application by executing dist/fcc-tool-linux/fcc-tool"
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
echo "You can run the application by executing dist/fcc-tool-macos/fcc-tool"
echo
""")
    os.chmod("install_macos.sh", 0o755)

def main():
    """Main function to parse arguments and build the executable"""
    parser = argparse.ArgumentParser(description="Build FCC Tool executable")
    parser.add_argument("--platform", choices=["windows", "linux", "macos"], 
                        help="Target platform (windows, linux, macos)")
    parser.add_argument("--clean", action="store_true", 
                        help="Clean build directories before building")
    parser.add_argument("--install-deps", action="store_true", 
                        help="Install required dependencies before building")
    parser.add_argument("--quiet", action="store_true",
                        help="Suppress output messages")
    
    args = parser.parse_args()
    
    if args.clean:
        clean_build_directories()
    
    if args.install_deps:
        install_requirements()
    
    success = build_executable(args.platform, args.quiet)
    
    if success:
        if not args.quiet:
            print("Build completed successfully!")
        return 0
    else:
        return 1

if __name__ == "__main__":
    sys.exit(main()) 