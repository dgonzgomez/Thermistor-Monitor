import cantools
from pprint import pprint

SENSOR_BUFFER = {}

def load_dbc_file(path):
    global dbc_db
    dbc_db = cantools.database.load_file(path)

def dbc_decode(msg):
    if dbc_db is None:
        return False

    try:
        message = dbc_db.get_message_by_frame_id(msg.arbitration_id)
    except KeyError as e:
        print(f"ID not defined in DBC: {msg.arbitration_id}")
        return False

    decoded = message.decode(msg.data)    
    
    for signal_id, value in decoded.items():
        full_signal_name = f"{message.name}.{signal_id}"

        if full_signal_name not in SENSOR_BUFFER:
            SENSOR_BUFFER[full_signal_name] = {"repackaged": None}
            
        SENSOR_BUFFER[full_signal_name]["repackaged"] = value
    return True

def parse(msg):
    # attempt to decode with DBC if available
    if dbc_decode(msg):
        return