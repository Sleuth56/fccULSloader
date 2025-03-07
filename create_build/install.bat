@echo off
echo FCC Tool Installer for Windows
echo ============================
echo.

REM Check for Python installation
python --version > nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Python is not installed or not in PATH.
    echo Please install Python 3.7 or higher from https://www.python.org/downloads/
    echo and make sure to check "Add Python to PATH" during installation.
    pause
    exit /b 1
)

echo Installing required packages...
pip install -r requirements.txt
if %ERRORLEVEL% neq 0 (
    echo Failed to install required packages.
    pause
    exit /b 1
)

echo Building executable...
python create_build\build_executable.py --platform windows
if %ERRORLEVEL% neq 0 (
    echo Failed to build executable.
    pause
    exit /b 1
)

echo Cleaning up temporary build files...
if exist build rmdir /s /q build
if exist *.spec del /f /q *.spec
if exist __pycache__ rmdir /s /q __pycache__
for /d /r . %%d in (__pycache__) do @if exist "%%d" rmdir /s /q "%%d"

echo.
echo Installation completed successfully!
echo The executable is located in the dist\fcc-tool-windows directory.
echo.
echo You can run the application by executing dist\fcc-tool-windows\fcc-tool.exe
echo.
echo Press any key to exit...
pause > nul 