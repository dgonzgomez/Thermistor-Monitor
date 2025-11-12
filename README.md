# Thermistor GUI

## How to Build

## Installing Dependencies:
```
python -m pip install
```
Will install the following from requirements.txt:
python-can[serial]
pyserial
pyinstaller

## Build Into Executable
```
python -m PyInstaller --onefile --windowed gui.py --hidden-import=can.interfaces.slcan --hidden-import=can.interfaces.serial --hidden-import=serial
```
Will put executable in 'dist' directory.
