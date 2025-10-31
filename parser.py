from interface import SENSOR_IDS

SENSOR_BUFFER = {
  "S1": {"A": None, "B": None, "repackaged": None},
  "S2": {"A": None, "B": None, "repackaged": None},
  "S3": {"A": None, "B": None, "repackaged": None},
  "S4": {"A": None, "B": None, "repackaged": None},
  "S5": {"A": None, "B": None, "repackaged": None},
  "S6": {"A": None, "B": None, "repackaged": None}
}

def parse(msg):
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
        if a_side is not None and b_side is not None:
            new_data = a_side + b_side
            SENSOR_BUFFER[sensor_number]["repackaged"] = new_data # not sure if this is the best way to do this

            print(f"Sensor: {sensor_number} | Data: {new_data}")

            # clear the buffer
            SENSOR_BUFFER[sensor_number]["A"] = None
            SENSOR_BUFFER[sensor_number]["B"] = None

