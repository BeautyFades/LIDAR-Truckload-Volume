import matplotlib.pyplot as plt
import numpy as np
from math import radians
import socket
from matplotlib.animation import FuncAnimation
import struct
import threading
from queue import Queue
import requests
from sensor_library import request_handle_udp, start_scanoutput, set_scanoutput_config, get_parameters, stop_scanoutput


# [START global variables]
# CLIENT_IP_ADDRESS = '192.168.1.50'
# [END global variables]

# [START turn on sensor]
R_REQUEST_HANDLE_UDP = request_handle_udp('192.168.1.12', 54321, skip_scans=46)
print('Handle is: ' + str(R_REQUEST_HANDLE_UDP['handle']))

R_START_SCANOUPUT = requests.get(f"http://192.168.1.12/cmd/start_scanoutput?handle={R_REQUEST_HANDLE_UDP['handle']}")
r_so = R_START_SCANOUPUT.json()
print(r_so)
# [END turn on sensor]


# [START network configs]
CLIENT_ADDRESS = '192.168.1.50'
PORT = 54321
# [END network configs]


# [START plotting configs]
distances = np.zeros(1800)

angle = [radians(a / 10) for a in range(0, 3600, 2)]
print(angle)

fig, ax = plt.subplots(subplot_kw=dict(projection='polar'))
ax.set_theta_zero_location('N')
ax.set_theta_direction(-1)
ax.set_rlim(0, 600)
ax.set_rmax(600)
plt.ion()
# [END plotting configs]

queue = Queue()


# [START grouping packets by scan]
packets_by_scan = {}
# [END grouping packets by scan]


# [START create UDP socket]
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((CLIENT_ADDRESS, PORT))
# [END create UDP socket]


# [START receiving loop]
def receive_data():
    while True:
        data, address = sock.recvfrom(2048)

        # If packet is small (i.e. corrupt packet), ignore it. Only process larger packets.
        if len(data) > 2:
            # Log magic byte to guarantee it is working
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


            # Check if we've received any packets for this scan yet.
            if scan_number not in packets_by_scan:
            # If not, create a new list inside the packets_by_scan dict to store the packets for this scan.
                packets_by_scan[scan_number] = []

            # Add the packet to the list of packets for this scan
            packets_by_scan[scan_number].append(data)

            # Check if we've received all the packets for this scan
            # For 46Hz, 1800 points per scan (0.2deg step) we have 6 packets to receive all data from a single scan.
            TOTAL_PACKETS_PER_SCAN = 6 
            if packet_number == TOTAL_PACKETS_PER_SCAN:
                print(f'We can process scan number: {scan_number}')

                # packets_for_this_scan is a list containing all binary from the 6 packets. If we loop through it we can
                # extract all distances for the current scan.
                packets_for_this_scan = packets_by_scan.pop(scan_number)
                #print(packets_for_this_scan)

                distances = []

                for packet in packets_for_this_scan:
                    start_byte = 76
                    while start_byte < len(packet):
                        dist = struct.unpack('<i', packet[start_byte:start_byte+4])[0]
                        distances.append(dist)
                        start_byte += 4

                #print(distances)
                print(len(distances))
                queue.put(distances)

        else:
            print('Empty or corrupt packet!')

        


# Create and start the threads
data_thread = threading.Thread(target=receive_data)
data_thread.daemon = True
data_thread.start()

# Define the function to update the plot
def update(frame):
    # Check if there is new data in the queue
    if not queue.empty():
        distances = queue.get()

        # Plot the distances
        ax.clear()
        ax.plot(angle, distances)

ani = FuncAnimation(fig, update, interval=10)

# Show the plot
plt.show()
