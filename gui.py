import tkinter as tk
from tkinter import ttk, filedialog
from interface import get_ports, Interface
from parser import SENSOR_BUFFER, parse
from parser import load_dbc_file

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

def refresh_ports():
    ports = get_ports()
    port_dropdown['values'] = ports
    if ports:
        selected_port.set(ports[0])
    else:
        selected_port.set("No Ports Available")

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
global sensor_labels 
sensor_labels = {}

# scrollable sensor container
sensor_container = ttk.Frame(main)
sensor_container.grid(row=2, column=0, sticky="nsew")

canvas = tk.Canvas(sensor_container, highlightthickness=0)
scrollbar = ttk.Scrollbar(sensor_container, orient="vertical", command=canvas.yview)

canvas.configure(yscrollcommand=scrollbar.set)

scrollbar.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)

# holds labels
sensor_frame = ttk.Frame(canvas)
canvas_window = canvas.create_window((0, 0), window=sensor_frame, anchor="nw")

sensor_labels = {}

# allow layout expansion
main.rowconfigure(2, weight=1)
main.columnconfigure(0, weight=1)

# update scroll region automatically
def _configure_scroll_region(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

sensor_frame.bind("<Configure>", _configure_scroll_region)

# optional mouse wheel support
def _on_mousewheel(event):
    canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

canvas.bind_all("<MouseWheel>", _on_mousewheel)

# table headers
ttk.Label(sensor_frame, text="Signal", style="Header.TLabel").grid(row=0, column=0, sticky="ew")
ttk.Label(sensor_frame, text="Value", style="Header.TLabel").grid(row=0, column=1, sticky="ew")

sensor_frame.columnconfigure(0, weight=3)
sensor_frame.columnconfigure(1, weight=1)

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
    
    # Load DBC file if not empty
    load_dbc_file(path)
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

refresh_button = ttk.Button(
    ports_row,
    text="Refresh",
    command=refresh_ports
)
refresh_button.grid(row=0, column=5, sticky="w", padx=PADX)

def ensure_sensor_label(sensor_name):
    if sensor_name in sensor_labels:
        return

    # offset by 1 because of header row
    row = len(sensor_labels) + 1

    name_lbl = ttk.Label(sensor_frame, text=sensor_name, anchor="w")
    name_lbl.grid(row=row, column=0, sticky="ew", padx=4, pady=1)

    value_lbl = ttk.Label(sensor_frame, text="--", style="Value.TLabel", anchor="e")
    value_lbl.grid(row=row, column=1, sticky="ew", padx=4, pady=1)

    sensor_labels[sensor_name] = value_lbl

def update_screen():
    if interface is not None:
        while True:
            msg = interface.receive(timeout=0)
            if msg is None:
                break
            parse(msg)

    pending_updates = []

    for sensor, data in SENSOR_BUFFER.items():
        ensure_sensor_label(sensor)  # create new sensors if needed

        repackaged = data["repackaged"]
        if repackaged is not None:
            pending_updates.append((sensor, repackaged))
            SENSOR_BUFFER[sensor]["repackaged"] = None

    # apply UI updates in one batch
    for sensor, value in pending_updates:
        sensor_labels[sensor].config(text=str(value))

    # start the update loop
    root.after(100, update_screen)

def on_closing():
    if interface is not None:
        interface.close()
    root.destroy()
    
root.protocol("WM_DELETE_WINDOW", on_closing)
update_screen()
root.mainloop()