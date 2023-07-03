import struct
import matplotlib.pyplot as plt
import numpy as np
import json

def parse_binary_file(file_path):
    packets = {}

    with open(file_path, 'rb') as file:
        binary_data = file.read()

        magic_byte = b'\x5c\xa2'
        start_index = 0
        temp_group = []
        i = 0

        while start_index < len(binary_data):
            end_index = binary_data.find(magic_byte, start_index)
            if end_index == -1:
                end_index = len(binary_data)
            
            # Include the magic byte at the start of each packet
            packet_data = magic_byte + binary_data[start_index:end_index]
            
            # Extract the data from position 76 to the end of the packet
            packet_data = packet_data[76:]
            
            # Determine the number of elements based on the byte length
            num_elements = len(packet_data) // 4
            
            # Adjust the buffer size to match the number of elements
            buffer_size = num_elements * 4
            
            # Unpack the bytes to integers in Little-Endian byte order
            packet_int = struct.unpack(f'<{num_elements}I', packet_data[:buffer_size])
            
            # Append the integers to the temporary group
            temp_group.extend(list(packet_int))
            
            # Check if we have formed a group of 6 packets
            if len(temp_group) == 1800:
                packets[i] = (temp_group)
                temp_group = []
                i = i + 1
            
            # Move the start_index to the next valid position
            start_index = end_index + len(magic_byte)

            
    
    return packets


def save_dict_to_file(dictionary, file_path):
    with open(file_path, 'w') as file:
        json.dump(dictionary, file)
save_dict_to_file(parse_binary_file('saved_sensor_data/top_sensor.bin'), 'top_sensor_dict.py')


def plot_first_packet(packets):
    packet = packets[0]
    num_elements = len(packet)
    
    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
    ax.set_rlim(0, 4000)  # Set the radial axis limit
    
    theta = np.linspace(0, 2*np.pi, num_elements, endpoint=False)
    r = packet
    
    ax.plot(theta, r)
    ax.set_rticks([])  # Remove radial tick labels if not needed
    
    plt.title('Packet Values (First 1800 Elements)')
    plt.show()
#plot_first_packet(parse_binary_file('saved_sensor_data/left_sensor.bin'))