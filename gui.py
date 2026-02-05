import tkinter as tk
import cantools
from tkinter import ttk, filedialog
from interface import get_ports
from interface import Interface
from parser import SENSOR_BUFFER, parse
from ui_style import (
    apply_styles,
    GEOMETRY,
    PADDING,
    PADX,
    PADY_HEADER,
    PADY_PORTS,
    PADY_STATUS,
    STATUS_COLOR,
)

# gui setup
root = tk.Tk()
root.title("CAN Interface")
root.geometry(GEOMETRY)

# gui styling
apply_styles()

ports = get_ports()
selected_port = tk.StringVar(value=ports[0] if ports else "No Ports Available")
status_text = tk.StringVar(value="Disconnected")
dbc_text = tk.StringVar(value="DBC: not loaded")
dbc_db = None

main = ttk.Frame(root, padding=PADDING)
main.grid(row=0, column=0, sticky="nsew")
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

header = ttk.Label(main, text="CAN Interface", style="Header.TLabel")
header.grid(row=0, column=0, sticky="w", pady=PADY_HEADER)

ports_row = ttk.Frame(main)
ports_row.grid(row=1, column=0, sticky="w", pady=PADY_PORTS)
ttk.Label(ports_row, text="Port").grid(row=0, column=0, sticky="w")

port_dropdown = ttk.Combobox(
    ports_row,
    textvariable=selected_port,
    values=ports,
    state="readonly"
)
port_dropdown.grid(row=0, column=1, sticky="w", padx=PADX)


# create the sensor labels for the gui
sensor_labels = {}
sensor_frame = ttk.Frame(main)
sensor_frame.grid(row=2, column=0, sticky="nsew")

for i, sensor in enumerate(SENSOR_BUFFER.keys()):
    ttk.Label(sensor_frame, text=sensor).grid(row=i, column=0, sticky="w")
    lbl = ttk.Label(sensor_frame, text="waiting...", style="Value.TLabel")
    lbl.grid(row=i, column=1, sticky="w", padx=PADX)
    sensor_labels[sensor] = lbl

# delay initialization of the interface until successful connection
interface = None

# button callback to connect to the selected port on press
def connect_to_bus():
    global interface
    selected = selected_port.get()
    if selected == "No Ports Available":
        print("No valid port selected.")
        return
    
    interface = Interface(channel=selected)
    status_text.set(f"Connected: {selected}")

    connect_to_bus_button.config(state=tk.DISABLED)
    port_dropdown.config(state=tk.DISABLED)

    disconnect_button.config(state=tk.NORMAL)

def disconnect_from_bus():
    global interface
    if interface is not None:
        interface.close()
    interface = None
    status_text.set("Disconnected")

    connect_to_bus_button.config(state=tk.NORMAL)
    port_dropdown.config(state=tk.NORMAL)
    disconnect_button.config(state=tk.DISABLED)

def load_dbc():
    global dbc_db

    path = filedialog.askopenfilename(
        title="Select DBC file",
        filetypes=[("DBC files", "*.dbc")],
    )
    if not path: # No file selected
        return
    
    # Load DBC file
    if cantools.database.load_file(path) is not None:
        dbc_db = cantools.database.load_file(path)
        dbc_text.set(f"DBC loaded: {path.split('/')[-1]}")

# button calls its callback function
connect_to_bus_button = ttk.Button(
    ports_row,
    text="Connect",
    command=connect_to_bus
)
connect_to_bus_button.grid(row=0, column=2, sticky="w", padx=PADX)

disconnect_button = ttk.Button(
    ports_row,
    text="Disconnect",
    command=disconnect_from_bus,
    state=tk.DISABLED
)
disconnect_button.grid(row=0, column=3, sticky="w", padx=PADX)

dbc_button = ttk.Button(
    ports_row,
    text="Load DBC",
    command=load_dbc,
)
dbc_button.grid(row=0, column=4, sticky="w", padx=PADX)

status_label = ttk.Label(main, textvariable=status_text, foreground=STATUS_COLOR)
status_label.grid(row=3, column=0, sticky="w", pady=PADY_STATUS)
dbc_label = ttk.Label(main, textvariable=dbc_text, foreground=STATUS_COLOR)
dbc_label.grid(row=4, column=0, sticky="w")

def update_screen():
    if interface is not None:
        msg = interface.receive(timeout=0)
        if msg is not None:
            parse(msg)
            if dbc_db is not None:
                message = dbc_db.get_message_by_frame_id(msg.arbitration_id)
                decoded = message.decode(msg.data)
                dbc_text.set(f"{message.name}: {decoded}")
            else:
                dbc_text.set("DBC: not loaded")

    for sensor, data in SENSOR_BUFFER.items():
        repackaged = data["repackaged"]
        if repackaged is not None:
            sensor_labels[sensor].config(text=f"{sensor}: {repackaged}")
            SENSOR_BUFFER[sensor]["repackaged"] = None
    
    # start the update loop
    root.after(100, update_screen)

def on_closing():
    if interface is not None:
        interface.close()
    root.destroy()
    
root.protocol("WM_DELETE_WINDOW", on_closing)
update_screen()
root.mainloop()