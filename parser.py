import cantools

SENSOR_BUFFER = {}
dbc_db = None

def load_dbc_file(path):
    global dbc_db
    dbc_db = cantools.database.load_file(path)

def dbc_decode(msg):
    if dbc_db is None:
        key = f"0x{msg.arbitration_id:03X}"
        if key not in SENSOR_BUFFER:
            SENSOR_BUFFER[key] = {"id": msg.arbitration_id, "repackaged": None}
        SENSOR_BUFFER[key]["repackaged"] = list(msg.data)
        return True
    try:
        message = dbc_db.get_message_by_frame_id(msg.arbitration_id)
    except KeyError as e:
        print(f"ID not defined in DBC: {msg.arbitration_id}")
        return False

    decoded = message.decode(msg.data)
    
    for signal_id, value in decoded.items():
        full_signal_name = f"{message.name}.{signal_id}"

        if full_signal_name not in SENSOR_BUFFER:
            SENSOR_BUFFER[full_signal_name] = {"id": None, "repackaged": None}
            
        SENSOR_BUFFER[full_signal_name]["repackaged"] = value
        SENSOR_BUFFER[full_signal_name]["id"] = int(msg.arbitration_id)
    return True

def parse(msg):

    dbc_decode(msg)
