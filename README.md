Build:
python -m PyInstaller --onefile --windowed gui.py `
  --hidden-import=can.interfaces.slcan `
  --hidden-import=can.interfaces.serial `
  --hidden-import=serial

Dependencies:
python-can[serial]
pyserial
pyinstaller
