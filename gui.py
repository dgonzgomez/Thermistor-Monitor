import tkinter as tk
import time
from interface import Interface
from parser import SENSOR_BUFFER, parse

# gui setup
root = tk.Tk()
root.title("Thermistor Monitor")
root.geometry("800x600")

#create the sensor lables for the gui
sensor_labels = {}
for i in range(1, 7):
    sensor = f"S{i}"
    lbl = tk.Label(root, text=f"{sensor}: waiting for data...")
    lbl.pack(pady=5)
    sensor_labels[sensor] = lbl

# connect to the can bus
interface = Interface()

def update_screen():
    msg = interface.receive()
    if msg is not None:
        parse(msg)
    
    for sensor, data in SENSOR_BUFFER.items():
        if data["repackaged"] is not None:
            sensor_labels[sensor].config(text=f"{sensor}: {data['repackaged']}")
        else:
            sensor_labels[sensor].config(text=f"{sensor}: waiting for data...")
    root.after(100, update_screen)

# start the update loop
root.after(100, update_screen)
root.mainloop()

# close the can bus connection on exit
interface.close()