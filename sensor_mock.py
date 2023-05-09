import socket
import time

UDP_IP = "127.0.0.1" # IP address of the UDP server
UDP_PORT = 54321 # Port number of the UDP server
INTERVAL = 0.1 # Time interval between sending packets (in seconds)

print('sensor up')


# Open the binary file in read-binary mode
with open('data.bin', 'rb') as f:
    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Read each row from the binary file and send it as a UDP packet
    while True:
        # read the first chunk of data from the file
        chunk = f.read(2048)
        remaining = b''
        while chunk:
        # search for the next occurrence of the magic byte in the chunk
            magic_idx = chunk.find(b'\x5c\xa2')
            while magic_idx >= 0:
                # extract the packet up until the magic byte
                packet = remaining + chunk[:magic_idx]
                magic_byte = b'\x5c\xa2'
                packet_with_magic = magic_byte + packet
                # send the packet via UDP
                sock.sendto(packet_with_magic, (UDP_IP, UDP_PORT))
                # remove the sent packet from the chunk
                chunk = chunk[magic_idx+2:]
                # search for the next occurrence of the magic byte in the chunk
                magic_idx = chunk.find(b'\x5c\xa2')
                # clear the remaining bytes
                remaining = b''
            # append the remaining bytes to the next chunk
            remaining += chunk
            # read the next chunk of data from the file
            chunk = f.read(2048)
            time.sleep(0.05) # Wait for the specified interval
