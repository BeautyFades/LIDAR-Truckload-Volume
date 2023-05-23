import time
import struct
INTERVAL = 0.1

# Open the binary file in read-binary mode
with open('saved_sensor_data/top_sensor.bin', 'rb') as f:
    data = f.read(8192)
    print(data)

    magic = struct.unpack('<H', data[:2])[0]
    print('magic byte: ' + str(hex(magic))) 
    packet_type = struct.unpack('<H', data[2:4])[0]
    print('packet_type: ' + str(hex(packet_type)))  
    packet_size = struct.unpack('<i', data[4:8])[0]
    print('packet_size: ' + str(int(packet_size)))  
    header_size = struct.unpack('<H', data[8:10])[0]
    print('header_size: ' + str(int(header_size)))  
    scan_number = struct.unpack('<H', data[10:12])[0]
    print('scan_number: ' + str(int(scan_number)))  
    packet_number = struct.unpack('<H', data[12:14])[0]
    print('packet_number in scan: ' + str(int(packet_number)))

    timestamp = struct.unpack('<Q', data[14:22])[0]
    print('Timestamp for scan: ' + str(int(timestamp)))

    timestamp_sync = struct.unpack('<Q', data[22:30])[0]
    print('Timestamp_sync for scan: ' + str(int(timestamp_sync)))

    status_flags = struct.unpack('<i', data[30:34])[0]
    print('status_flags for scan: ' + str(int(status_flags)))

    scan_frequency = struct.unpack('<i', data[34:38])[0]
    print('scan_frequency: ' + str(int(scan_frequency)))