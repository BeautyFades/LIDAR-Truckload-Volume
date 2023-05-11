from PyQt5.QtCore import pyqtSignal, QObject
import random
import time

# Worker thread for real-time plotting of LiDAR data
class PlottingWorker(QObject):
    data_ready = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self.data = []  # Data to plot
        self.running = False

    def start(self):
        self.running = True
        while self.running:
            # Retrieve real-time data (e.g., from a sensor)
            new_data = self.get_real_time_data()

            # Add new data to the existing data
            self.data.append(new_data)

            # Emit a signal to update the plot in the main thread
            self.data_ready.emit(self.data)

    def stop(self):
        self.running = False

    def get_real_time_data(self):
        # Simulate real-time data retrieval (replace with your implementation)
        time.sleep(0.05)
        return random.randint(0, 100)