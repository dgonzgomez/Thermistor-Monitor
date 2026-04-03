# CAN Viewer

A simple GUI application for reading values off the CAN line.

## How to Install

Click on Releases on the GitHub page and download the file under the latest release for your operating system.

For macOS, you need to unzip the zip file to run the app.

For Linux, you need to make the program executable.

## How to Build

You will need Python 3 to develop this application.

### Installing Dependencies
```
python -m pip install -r requirements.txt
```
Will install the following from requirements.txt:
- python-can[serial]
- pyserial
- pyinstaller
- cantools
- customtkinter

If you're on Linux, you need to separately install Tkinter for Python.

### Build Into Executable
```
python -m PyInstaller --onefile --windowed gui.py --hidden-import=can.interfaces.slcan --hidden-import=can.interfaces.serial --hidden-import=serial
```
Will put executable in 'dist' directory.
