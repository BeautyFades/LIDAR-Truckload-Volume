from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QWidget
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QObject
from PyQt5.QtGui import QIcon
import matplotlib.pyplot as plt
import sys
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


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set window properties
        self.setWindowTitle("UFSC - Coontrol - LiDAR Volume Measurement")
        self.setWindowIcon(QIcon("interface/coontrol-icon.png"))
        self.resize(800, 600)

        # Create a central widget and set the layout
        self.central_widget = QWidget()
        self.layout = QVBoxLayout(self.central_widget)

        # Add buttons to the layout
        button1 = QPushButton("Start Scan", self.central_widget)
        self.layout.addWidget(button1)
        button1.setStyleSheet("background-color: red; color: white; border-radius: 5px;")
        button1.clicked.connect(self.start_task)

        button2 = QPushButton("Button 2", self.central_widget)
        self.layout.addWidget(button2)
        button2.clicked.connect(self.create_plot)

        # Set the central widget
        self.setCentralWidget(self.central_widget)

        # Create the plotting worker
        self.plotting_worker = PlottingWorker()
        self.plotting_thread = QThread()
        self.plotting_worker.moveToThread(self.plotting_thread)
        self.plotting_worker.data_ready.connect(self.update_plot)
        self.plotting_thread.started.connect(self.plotting_worker.start)

    def start_task(self):
        # Placeholder for your long-running task
        print("Button 1 clicked")

    def create_plot(self):
        # Create the plot
        self.fig, self.ax = plt.subplots()
        self.line, = self.ax.plot([], [])

        # Add the plot to the layout
        self.layout.addWidget(self.fig.canvas)

        # Start the plotting thread
        self.plotting_thread.start()

    def update_plot(self, data):
        # Update the plot with the new data
        self.line.set_data(range(len(data)), data)
        self.ax.relim()
        self.ax.autoscale_view()
        self.fig.canvas.draw()

    def closeEvent(self, event):
        # Stop the plotting thread when closing the window
        if self.plotting_thread.isRunning():
            self.plotting_worker.stop()
            self.plotting_thread.quit()
            self.plotting_thread.wait()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
