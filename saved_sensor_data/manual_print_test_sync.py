import struct
import time

CLIENT_UDP_IP = "127.0.0.1" # IP address of the Receiver UDP server
CLIENT_UDP_PORT = 54321 # Port number of the Receiver UDP server
INTERVAL = 0.1 # Time interval between each packet (in seconds)

print('Sensor starting...')


# Open the binary file in read-binary mode
with open('saved_sensor_data/right_sensor.bin', 'rb') as f:

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
                    timestamp_raw = struct.unpack('<Q', packet_with_magic[14:22])[0]
                    scan_number = struct.unpack('<H', packet_with_magic[10:12])[0]
                    #print(f'{str(int(scan_number))} | {str(int(timestamp_raw))}')
                    if int(scan_number == 289+6):
                        start_byte = 76
                        while start_byte < len(packet_with_magic):
                            dist = struct.unpack('<i', packet_with_magic[start_byte:start_byte+4])[0]
                            print(dist)
                            start_byte += 4

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
            #time.sleep(INTERVAL) # Wait for the specified interval