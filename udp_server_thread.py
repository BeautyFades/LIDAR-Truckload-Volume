import socket
from PyQt5.QtCore import QThread, pyqtSignal
import struct


UDP_IP = "127.0.0.1"  # IP address to bind the server
UDP_PORT = 54321      # Port to listen for incoming packets
PCK_SIZE = 4096

class UDPServerThread(QThread):
    packet_received = pyqtSignal(list)  # Signal to emit the received packet when thread finishes
    stop_signal = pyqtSignal()          # Signal to emit the received packet when thread is ordered to stop

    def __init__(self, verbose: bool = False):

        super().__init__()
        self.is_running = True
        self.packets_by_scan = dict()
        self.verbose = verbose


    def run(self):
        print('Started UDP Server Thread...')

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_socket.bind((UDP_IP, UDP_PORT))
        self.running = True

        while self.is_running:

            if self.isInterruptionRequested():
                break

            data, _ = self.server_socket.recvfrom(PCK_SIZE)

            if len(data) > 2:
                magic = struct.unpack('<H', data[:2])[0]
                packet_type = struct.unpack('<H', data[2:4])[0]
                packet_size = struct.unpack('<i', data[4:8])[0]
                header_size = struct.unpack('<H', data[8:10])[0]
                scan_number = struct.unpack('<H', data[10:12])[0]
                packet_number = struct.unpack('<H', data[12:14])[0]

                if self.verbose:
                    print('packet_number in scan: ' + str(int(packet_number)))
                    print('magic byte: ' + str(hex(magic)))
                    print('packet_type: ' + str(hex(packet_type)))
                    print('packet_size: ' + str(int(packet_size)))
                    print('header_size: ' + str(int(header_size)))
                    print('scan_number: ' + str(int(scan_number)))

                # Check if we've received any packets for this scan yet.
                if scan_number not in self.packets_by_scan:
                    # If not, create a new list inside the packets_by_scan dict to store the packets for this scan.
                    self.packets_by_scan[scan_number] = []

                # Add the packet to the list of packets for this scan
                self.packets_by_scan[scan_number].append(data)
                # Check if we've received all the packets for this scan
                # For 46Hz, 1800 points per scan (0.2deg step) we have 6 packets to receive all data from a single scan.
                # This must be changed if the sensor scanning configurations change.
                TOTAL_PACKETS_PER_SCAN = 6 
                if packet_number == TOTAL_PACKETS_PER_SCAN:
                    print(f'Received a full scan: {scan_number}')

                    # packets_for_this_scan is a list containing all binary from all the packets for a given scan. If we 
                    # loop through it we can extract all distances for the current scan.
                    packets_for_this_scan = self.packets_by_scan.pop(scan_number)
                    #print(packets_for_this_scan)
                    distances = []

                    for packet in packets_for_this_scan:
                        # Header has 76 bytes, so we start getting actual distance data at this index.
                        start_byte = 76
                        while start_byte < len(packet):
                            dist = struct.unpack('<i', packet[start_byte:start_byte+4])[0]
                            distances.append(dist)
                            # Each distance is 4 bytes, so to get the next distance value, add 4 to the start_byte.
                            start_byte += 4

                    if self.verbose:
                        print(distances)

                    # Emit the signal that data is ready to the interface.
                    self.packet_received.emit(distances)


    def stop(self):
        self.requestInterruption()
        print('Stopped the UDP Server Thread')
