import struct
import matplotlib.pyplot as plt
import numpy as np
import json
from math import radians

POLAR_ANGLES = [radians(a / 10) for a in range(0, 3600, 2)]
def polar2cart(r, theta):
    return r * np.exp(1j * theta)


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
            packet_int = list(packet_int)
            final_packet_int = []
            for elem in packet_int:
                if elem > 3000 or elem < -3000:
                    elem = 0
                final_packet_int.append(elem)
            
            # Append the integers to the temporary group
            temp_group.extend(final_packet_int)
            
            # Check if we have formed a group of 6 packets
            if len(temp_group) == 1800:
                temp_group2 = []
                for index, elem in enumerate(temp_group):
                    complex_num = polar2cart(elem, POLAR_ANGLES[index])
                    cart_tuple = (round(complex_num.real, 3), round(complex_num.imag, 3))
                    temp_group2.append(cart_tuple)


                packets[i] = temp_group2
                temp_group = []
                i = i + 1
            
            # Move the start_index to the next valid position
            start_index = end_index + len(magic_byte)

    return packets

DICT = parse_binary_file('saved_sensor_data/left_sensor.bin')

# def save_dict_to_file(dictionary, file_path):
#     with open(file_path, 'w') as file:
#         json.dump(dictionary, file)
# save_dict_to_file(parse_binary_file('saved_sensor_data/top_sensor.bin'), 'sensor_data_dict_format/top_sensor_dict.py')
# save_dict_to_file(parse_binary_file('saved_sensor_data/left_sensor.bin'), 'sensor_data_dict_format/left_sensor_dict.py')
# save_dict_to_file(parse_binary_file('saved_sensor_data/right_sensor.bin'), 'sensor_data_dict_format/right_sensor_dict.py')


# def plot_key(dictionary, key):
#     x_coords, y_coords = zip(*dictionary[key])
#     plt.plot(x_coords, y_coords)
#     plt.xlabel('X')
#     plt.ylabel('Y')
#     plt.title(f'Plot of Key: {key}')
#     plt.show()

# plot_key(DICT, 0)

