import struct
import time

CLIENT_UDP_IP = "127.0.0.1" # IP address of the Receiver UDP server
CLIENT_UDP_PORT = 54321 # Port number of the Receiver UDP server
INTERVAL = 0.1 # Time interval between each packet (in seconds)

print('Sensor starting...')


# Open the binary file in read-binary mode
with open('saved_sensor_data/left_sensor.bin', 'rb') as f:

    # Read each row from the binary file and print it
    while True:

        # Read the first chunk of chunk from the file
        chunk = f.read(2048)
        remaining = b''
        while chunk:
        # Search for the next occurrence of the magic byte in the chunk
            magic_idx = chunk.find(b'\x5c\xa2')
            while magic_idx >= 0:

                # Extract the packet up until the magic byte
                packet = remaining + chunk[:magic_idx]
                magic_byte = b'\x5c\xa2'
                packet_with_magic = magic_byte + packet

                # Send the packet via UDP
                if len(packet_with_magic) > 2:
                    # Log magic byte to guarantee it is working
                    magic = struct.unpack('<H', packet_with_magic[:2])[0]
                    print('magic byte: ' + str(hex(magic)))

                    packet_type = struct.unpack('<H', packet_with_magic[2:4])[0]
                    print('packet_type: ' + str(hex(packet_type)))
                    
                    packet_size = struct.unpack('<i', packet_with_magic[4:8])[0]
                    print('packet_size: ' + str(int(packet_size)))

                    header_size = struct.unpack('<H', packet_with_magic[8:10])[0]
                    print('header_size: ' + str(int(header_size)))

                    scan_number = struct.unpack('<H', packet_with_magic[10:12])[0]
                    print('scan_number: ' + str(int(scan_number)))

                    packet_number = struct.unpack('<H', packet_with_magic[12:14])[0]
                    print('packet_number in scan: ' + str(int(packet_number)))

                    timestamp_raw = struct.unpack('<Q', packet_with_magic[14:22])[0]
                    print('timestamp_raw in scan: ' + str(int(timestamp_raw)))

                    timestamp_sync = struct.unpack('<Q', packet_with_magic[22:30])[0]
                    print('timestamp_sync in scan: ' + str(int(timestamp_sync)))

                    status_flags = struct.unpack('<i', packet_with_magic[30:34])[0]
                    print('status_flags in scan: ' + str(int(status_flags)))

                    scan_frequency = struct.unpack('<i', packet_with_magic[34:38])[0]
                    print('scan_frequency in scan: ' + str(int(scan_frequency)))

                # Remove the sent packet from the chunk
                chunk = chunk[magic_idx+2:]

                # Search for the next occurrence of the magic byte in the chunk
                magic_idx = chunk.find(b'\x5c\xa2')

                # Clear the remaining bytes
                remaining = b''

            # Append the remaining bytes to the next chunk
            remaining += chunk
            # Read the next chunk of chunk from the file
            chunk = f.read(2048)
            time.sleep(INTERVAL) # Wait for the specified interval