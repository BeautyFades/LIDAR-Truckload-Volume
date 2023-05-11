import socket
from threading import Thread
import numpy as np
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt

# UDP server settings
UDP_IP = "127.0.0.1"  # IP address to bind the server
UDP_PORT = 54321       # Port to listen for incoming packets

# Create a custom thread for receiving UDP packets
class UDPServerThread(Thread):
    def __init__(self):
        super().__init__()
        self.data = np.array([])  # Array to store the received data

    def run(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_socket.bind((UDP_IP, UDP_PORT))

        while True:
            data, _ = server_socket.recvfrom(2048)
            self.data = np.append(self.data, float(data))

# Create the UDP server thread and start it
udp_thread = UDPServerThread()
udp_thread.start()

# Create a polar plot
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1, projection='polar')

# Set initial plot properties
line, = ax.plot([], [], 'b')
ax.set_rticks([])  # Hide radial tick labels
ax.set_title('Real-Time Distance Plot')

# Initialize the plot data
theta = np.linspace(0, 2 * np.pi, len(udp_thread.data), endpoint=False)

# Function to update the plot
def update_plot(frame):
    # Update the plot data
    line.set_data(theta, udp_thread.data)

# Create an animation to update the plot
ani = FuncAnimation(fig, update_plot, interval=100)

# Show the plot
plt.show()
