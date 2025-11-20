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
    
    subpack_num = ID_MAPPINGS[msg_id]
    data = list(msg.data)
    copy_start_range = 0 if msg_id % 2 else 6  
    
    for i, data in enumerate(data):
        

