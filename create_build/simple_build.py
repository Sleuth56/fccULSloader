#!/usr/bin/env python3
"""
Simple build script for creating a standalone executable of FCC Tool
"""

import os
import subprocess
import sys
import platform
import importlib.util

# Import version from fcc_tool.py
def get_version():
    """Get version from fcc_tool.py"""
    try:
        # Try to import from src directory first
        if os.path.exists(os.path.join("src", "fcc_tool.py")):
            spec = importlib.util.spec_from_file_location("fcc_tool", os.path.join("src", "fcc_tool.py"))
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

def build_executable():
    """Build the executable using PyInstaller with minimal options"""
    print("Building executable...")
    
    # Create dist directory if it doesn't exist
    if not os.path.exists("dist"):
        os.makedirs("dist")
    
    # Determine the path to fcc_tool.py
    if os.path.exists(os.path.join("src", "fcc_tool.py")):
        fcc_tool_path = os.path.join("src", "fcc_tool.py")
    elif os.path.exists("fcc_tool.py"):
        fcc_tool_path = "fcc_tool.py"
    else:
        print("Error: fcc_tool.py not found in src directory or root directory")
        return False
    
    print(f"Using source file: {fcc_tool_path}")
    
    # Build command with minimal options - using --onefile for a single executable
    cmd = [
        "pyinstaller",
        f"--name=fcc-tool-{VERSION}",  # Include version in executable name
        "--onefile",  # Single file executable
        "--clean",
        fcc_tool_path
    ]
    
    try:
        subprocess.check_call(cmd)
        print("Build completed successfully!")
        print(f"Executable can be found in the 'dist' directory as 'fcc-tool-{VERSION}.exe'")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error building executable: {e}")
        return False

if __name__ == "__main__":
    build_executable() 