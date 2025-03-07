# FCC Tool Build Scripts

This directory contains scripts for building standalone executables of the FCC Tool application.

## Available Scripts

- **build_executable.py**: Main build script that supports building for Windows, Linux, and macOS
- **simple_build.py**: Simplified build script for quick builds
- **install.bat**: Windows installation script
- **install.sh**: Linux installation script
- **install_macos.sh**: macOS installation script
- **setup.py**: Setup script for packaging the application

## Building Executables

### Using the Installation Scripts

The easiest way to build the executable is to use the installation scripts:

#### Windows

```
cd <project_root>
create_build\install.bat
```

#### Linux

```
cd <project_root>
./create_build/install.sh
```

#### macOS

```
cd <project_root>
./create_build/install_macos.sh
```

### Using the Build Scripts Directly

You can also use the build scripts directly:

#### Building for a Specific Platform

```
cd <project_root>
python create_build/build_executable.py --platform <platform>
```

Where `<platform>` is one of: `windows`, `linux`, or `macos`.

#### Building for All Platforms

```
cd <project_root>
python create_build/build_executable.py --platform all
```

#### Quick Build

```
cd <project_root>
python create_build/simple_build.py
```

## Output

The executables will be created in the following directories:

- Windows: `dist/fcc-tool-windows/fcc-tool-<version>.exe`
- Linux: `dist/fcc-tool-linux/fcc-tool-<version>`
- macOS: `dist/fcc-tool-macos/fcc-tool-<version>`

Where `<version>` is the version number defined in `src/fcc_tool.py`. 