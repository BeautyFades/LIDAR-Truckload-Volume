import socket
import time

CLIENT_UDP_IP = "127.0.0.1" # IP address of the Receiver UDP server
CLIENT_UDP_PORT = 54323 # Port number of the Receiver UDP server
INTERVAL = 0.1 # Time interval between each packet (in seconds)

print('Sensor starting...')


# Open the binary file in read-binary mode
with open('right_sensor.bin', 'rb') as f:
    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Read each row from the binary file and send it as a UDP packet
    while True:
        
        # Read the first chunk of data from the file
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
                sock.sendto(packet_with_magic, (CLIENT_UDP_IP, CLIENT_UDP_PORT))
                print('Sent a new packet!')

                # Remove the sent packet from the chunk
                chunk = chunk[magic_idx+2:]

                # Search for the next occurrence of the magic byte in the chunk
                magic_idx = chunk.find(b'\x5c\xa2')

                # Clear the remaining bytes
                remaining = b''

            # Append the remaining bytes to the next chunk
            remaining += chunk
            # Read the next chunk of data from the file
            chunk = f.read(2048)
            time.sleep(INTERVAL) # Wait for the specified interval
