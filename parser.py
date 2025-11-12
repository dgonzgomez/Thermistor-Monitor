ID_MAPPINGS = {
    0x151: 1, 0x152: 1,
    0x251: 2, 0x252: 2,
    0x351: 3, 0x352: 3,
    0x451: 4, 0x452: 4,
    0x551: 5, 0x552: 5,
    0x651: 6, 0x652: 6,
}

SUBPACK_DATA = {
  1: [0] * 12,
  2: [0] * 12,
  3: [0] * 12,
  4: [0] * 12,
  5: [0] * 12,
  6: [0] * 12
}

def parse(msg):
    msg_id = msg.arbitration_id
    
    if msg_id not in ID_MAPPINGS: return
    
    subpack_num = ID_MAPPINGS.get(msg_id, None)
    
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

