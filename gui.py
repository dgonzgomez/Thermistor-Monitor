from customtkinter import (
    CTk,
    CTkButton,
    CTkCanvas,
    CTkComboBox,
    CTkFrame,
    CTkLabel,
    CTkEntry,
    CTkScrollbar,
    StringVar,
    filedialog
)
import cantools
from interface import get_ports, Interface
from parser import SENSOR_BUFFER, parse, load_dbc_file
from ui_style import (
    FONTS,
    apply_styles,
    GEOMETRY,
    PADDING,
    PADX,
    PADY_HEADER,
    PADY_PORTS,
    PADY_STATUS,
    STATUS_COLOR,
    TABLE_HEADER_BG,
    TABLE_ROW_BG,
    TABLE_ROW_ALT_BG,
    TABLE_BORDER,
    TABLE_TEXT,
    APP_BG,
)

# gui setup
root = CTk()
root.title("CAN Interface")
root.geometry(GEOMETRY)
root.configure(fg_color=APP_BG)
apply_styles()

ports = get_ports()
selected_port = StringVar(value=ports[0] if ports else "No Ports Available")
status_text = StringVar(value="Disconnected")
dbc_text = StringVar(value="DBC: not loaded")
dbc_db = None
CONNECTED_COLOR = "#2ecc71"
DISCONNECTED_COLOR = STATUS_COLOR
DBC_LOADED_COLOR = "#2ecc71"
DBC_UNLOADED_COLOR = STATUS_COLOR

main = CTkFrame(root, fg_color=APP_BG)
main.grid(row=0, column=0, sticky="nsew", padx=PADDING, pady=PADDING)
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# gui header layout 
header = CTkLabel(main, text="CAN Interface", font=FONTS["header"])
header.grid(row=0, column=0, sticky="w", pady=PADY_HEADER)

ports_row = CTkFrame(main, fg_color=APP_BG)
ports_row.grid(row=1, column=0, sticky="w", pady=PADY_PORTS)
CTkLabel(ports_row, text="Port").grid(row=0, column=0, sticky="w")

port_dropdown = CTkComboBox(ports_row, variable=selected_port, values=ports)
port_dropdown.grid(row=0, column=1, sticky="w", padx=PADX)

# sensor display layout
sensor_labels = {}
sensor_container = CTkFrame(
    main,
    corner_radius=10,
    border_width=1,
    border_color=TABLE_BORDER,
    fg_color=APP_BG,
)
sensor_container.grid(row=2, column=0, sticky="nsew")

canvas = CTkCanvas(sensor_container, highlightthickness=0, bg=TABLE_ROW_BG)
scrollbar = CTkScrollbar(sensor_container, orientation="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)

sensor_frame = CTkFrame(canvas, fg_color=TABLE_ROW_BG)
canvas.create_window((0, 0), window=sensor_frame, anchor="nw")

def on_frame_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

sensor_frame.bind("<Configure>", on_frame_configure)
main.rowconfigure(2, weight=1)
main.columnconfigure(0, weight=1)

# edit this if you want more columns in the spread sheet
# maybe we can tie this to a setting it should be easy, not sure if it's necessary
MAX_COLUMNS = 4

# table setup
header_row = CTkFrame(
    sensor_frame, fg_color=TABLE_HEADER_BG, corner_radius=8
)
header_row.grid(
    row=0, column=0, columnspan=MAX_COLUMNS * 2, sticky="ew", padx=6, pady=(6, 4)
)
header_row.columnconfigure(0, weight=3)
header_row.columnconfigure(1, weight=1)
CTkLabel(
    header_row,
    text="Signal",
    font=FONTS["table_header"],
    text_color=TABLE_TEXT,
).grid(row=0, column=0, sticky="w", padx=8, pady=6)
CTkLabel(
    header_row,
    text="Value",
    font=FONTS["table_header"],
    text_color=TABLE_TEXT,
).grid(row=0, column=1, sticky="e", padx=8, pady=6)
for col in range(MAX_COLUMNS * 2):
    sensor_frame.columnconfigure(col, weight=3 if col % 2 == 0 else 1)

interface = None

# helper functions for button commands
def refresh_ports():
    ports = get_ports()
    port_dropdown.configure(values=ports)
    selected_port.set(ports[0] if ports else "No Ports Available")

def connect_to_bus():
    global interface
    selected = selected_port.get()
    if selected == "No Ports Available":
        print("No valid port selected.")
        return

    interface = Interface(channel=selected)
    status_text.set(f"Connected: {selected}")
    status_label.configure(text_color=CONNECTED_COLOR)
    if dbc_db is not None:
        dbc_label.configure(text_color=DBC_LOADED_COLOR)
    connect_to_bus_button.configure(state="disabled")
    port_dropdown.configure(state="disabled")
    disconnect_button.configure(state="normal")

def disconnect_from_bus():
    global interface
    if interface is not None:
        interface.close()
    interface = None
    status_text.set("Disconnected")
    status_label.configure(text_color=DISCONNECTED_COLOR)
    dbc_label.configure(text_color=DBC_UNLOADED_COLOR)
    connect_to_bus_button.configure(state="normal")
    port_dropdown.configure(state="normal")
    disconnect_button.configure(state="disabled")

def load_dbc():
    global dbc_db
    path = filedialog.askopenfilename(
        title="Select DBC file",
        filetypes=[("DBC files", "*.dbc"), ("All files", "*.*")],
    )
    if not path:
        return
    # try loading the DBC into the parser before updating GUI
    try:
        load_dbc_file(path)
    except Exception as exc:
        # let's in the future have this displayed in the GUI
        status_text.set(f"DBC load failed: {exc}")
        return
    # try loading the DBC file into the cantools database
    try:
        dbc_db = cantools.database.load_file(path)
    except Exception as exc:
        dbc_db = None
        status_text.set(f"DBC load failed: {exc}")
        return

    dbc_text.set(f"DBC loaded: {path.split('/')[-1]}")
    dbc_label.configure(text_color=DBC_LOADED_COLOR)

# actual setup of button styling
connect_to_bus_button = CTkButton(ports_row, text="Connect", command=connect_to_bus)
connect_to_bus_button.grid(row=0, column=2, sticky="w", padx=PADX)

disconnect_button = CTkButton(
    ports_row, text="Disconnect", command=disconnect_from_bus, state="disabled"
)
disconnect_button.grid(row=0, column=3, sticky="w", padx=PADX)

dbc_button = CTkButton(ports_row, text="Load DBC", command=load_dbc)
dbc_button.grid(row=0, column=4, sticky="w", padx=PADX)

refresh_button = CTkButton(ports_row, text="Refresh", command=refresh_ports)
refresh_button.grid(row=0, column=5, sticky="w", padx=PADX)

search_ids = []
search_box = CTkEntry(ports_row, placeholder_text="Enter a CANID")
search_box.grid(row=0, column=6, sticky="w", padx=PADX)

status_label = CTkLabel(main, textvariable=status_text, text_color=STATUS_COLOR)
status_label.grid(row=3, column=0, sticky="w", pady=PADY_STATUS)
dbc_label = CTkLabel(main, textvariable=dbc_text, text_color=STATUS_COLOR)
dbc_label.grid(row=4, column=0, sticky="w")

# process the incoming messages and put them into a table
def ensure_sensor_label(sensor_name):
    # does not update if the label already exists
    # only creates a new label if the sensor is new
    if sensor_name in sensor_labels:
        return

    index = len(sensor_labels)
    row = (index // MAX_COLUMNS) + 1
    col_base = (index % MAX_COLUMNS) * 2

    # styling
    row_color = TABLE_ROW_ALT_BG if row % 2 == 0 else TABLE_ROW_BG
    row_frame = CTkFrame(
        sensor_frame,
        fg_color=row_color,
        corner_radius=6,
    )
    row_frame.grid(
        row=row, column=col_base, columnspan=2, sticky="ew", padx=6, pady=2
    )
    row_frame.columnconfigure(0, weight=3)
    row_frame.columnconfigure(1, weight=1)

    name_lbl = CTkLabel(
        row_frame,
        text=sensor_name,
        anchor="w",
        text_color=TABLE_TEXT,
        font=FONTS["label"],
    )
    name_lbl.grid(row=0, column=0, sticky="w", padx=8, pady=4)
    value_lbl = CTkLabel(
        row_frame,
        text="--",
        font=FONTS["value"],
        anchor="e",
        text_color=TABLE_TEXT,
    )
    value_lbl.grid(row=0, column=1, sticky="e", padx=8, pady=4)

    sensor_labels[sensor_name] = {"name": name_lbl, "value": value_lbl}

def delete_sensor_label(sname):
    if sname in sensor_labels:
        sensor_labels[sname]["name"].grid_forget()
        sensor_labels[sname]["value"].grid_forget()
        del sensor_labels[sname]
    
# Returns true if the given ID is not currently in the search
def in_search(id):
    if not search_ids:
        return True
    return id in search_ids
    
def update_search():
    global search_ids
    global search_box
    text = search_box.get()
    
    try:
        search_ids = [int(term, 0) for term in text.split(',')]
    except:
        search_ids = []

# the meat of the program
def update_screen():
    if interface is not None:
        while True:
            msg = interface.receive(timeout=0)
            if msg is None:
                break
            parse(msg)
    
    update_search()
    
    # store the new data in a buffer
    pending_updates = []
    for sensor, data in SENSOR_BUFFER.items():
        if (not in_search(data["id"])):
            delete_sensor_label(sensor)
            continue
        ensure_sensor_label(sensor)
        repackaged = data["repackaged"]
        if repackaged is not None:
            pending_updates.append((sensor, repackaged))
            SENSOR_BUFFER[sensor]["repackaged"] = None

    # update the labels in the GUI for all the sensors that have new data
    for sensor, value in pending_updates:
        sensor_labels[sensor]["value"].configure(text=str(value))

    root.after(100, update_screen)

def on_closing():
    if interface is not None:
        interface.close()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)
update_screen()
root.mainloop()
