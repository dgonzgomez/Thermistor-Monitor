from interface import SENSOR_IDS
import cantools
from pprint import pprint

SENSOR_BUFFER = {
  "S1": {"A": None, "B": None, "repackaged": None},
  "S2": {"A": None, "B": None, "repackaged": None},
  "S3": {"A": None, "B": None, "repackaged": None},
  "S4": {"A": None, "B": None, "repackaged": None},
  "S5": {"A": None, "B": None, "repackaged": None},
  "S6": {"A": None, "B": None, "repackaged": None}
}

dbc_db = None

def load_dbc_file(path):
    global dbc_db
    dbc_db = cantools.database.load_file(path)

def dbc_decode(msg):
    global dbc_db

    if dbc_db is None:
        return False

    try:
        message = dbc_db.get_message_by_frame_id(msg.arbitration_id)
    except KeyError as e:
        print(f"ID not defined in DBC: {msg.arbitration_id}")
        return False

    decoded = message.decode(msg.data)    
    
    for signal_id, value in decoded.items():
        if signal_id not in SENSOR_BUFFER:
            SENSOR_BUFFER[signal_id] = {"repackaged": None}

        SENSOR_BUFFER[signal_id]["repackaged"] = value
    return True

def parse(msg):
    # attempt to decode with DBC if available
    if dbc_decode(msg) is not None:
        return
    
    # fallback
    if msg.arbitration_id in SENSOR_IDS:

        # parse the message for it's sensor id and data
        can_id = msg.arbitration_id
        sensor_id = SENSOR_IDS.get(can_id, None)
        
        if sensor_id is None:
            return None
        
        # split the sensor number and the part (A or B)
        sensor_number, part = sensor_id.split("_")

        # add the data to the buffer
        SENSOR_BUFFER[sensor_number][part] = list(msg.data)

        a_side = SENSOR_BUFFER[sensor_number]["A"]
        b_side = SENSOR_BUFFER[sensor_number]["B"]

        # repackage the data into a single list
        if a_side is not None or b_side is not None:
            new_data = (a_side or []) + (b_side or [])
            SENSOR_BUFFER[sensor_number]["repackaged"] = new_data

            # Terminal output for debugging
            # print(f"Sensor: {sensor_number} | Data: {new_data}")
