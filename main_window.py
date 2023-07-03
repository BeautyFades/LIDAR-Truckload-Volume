import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import *
from udp_server_thread import UDPServerThread
from math import radians

from config_window import ConfigWindow
from sensor_plots import SensorPlots

# Create a PyQt5 main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

        self.offsetInputValues = {}

        QMetaObject.connectSlotsByName(self)

        # Create the UDP server thread and start it
        self.udp_thread1 = UDPServerThread(ip_address='127.0.0.1', udp_port=54321, verbose=False)
        self.udp_thread2 = UDPServerThread(ip_address='127.0.0.1', udp_port=54322, verbose=False)
        self.udp_thread3 = UDPServerThread(ip_address='127.0.0.1', udp_port=54323, verbose=False)

    def initUI(self):
        self.setWindowTitle("Truckload Volume Calculator")
        self.setWindowIcon(QIcon("interface/coontrol-icon.png"))

        self.central_widget = QWidget(self)
        self.central_widget.setObjectName('centralWidget')
        self.layout = QVBoxLayout(self.central_widget)

        start_stop_layout = QHBoxLayout()  # Horizontal layout for buttons

        self.stopButton = QPushButton(self.central_widget)
        self.stopButton.setObjectName('stopButton')
        self.stopButton.setText('Stop Scanning')
        self.stopButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.stopButton.setCheckable(False)
        self.stopButton.setEnabled(False)
        self.stopButton.clicked.connect(self.stop_button_task)
        self.stopButton.setStyleSheet("border: none;\n"
                                    "font-family: 'Lato';\n"
                                    "background-color: #FF6766;\n"
                                    "cursor: pointer;\n"
                                    "padding: 15px 20px;\n"
                                    "display: inline-block;\n"
                                    "text-transform: uppercase;\n"
                                    "letter-spacing: 1px;\n"
                                    "font-weight: 700;"
                                    )

        self.startButton = QPushButton(self.central_widget)
        self.startButton.setObjectName('startButton')
        self.startButton.setText('Start Scanning')
        self.startButton.setCheckable(False)
        self.startButton.setEnabled(True)
        self.startButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.startButton.clicked.connect(self.start_button_task)
        self.startButton.setStyleSheet("border: none;\n"
                                    "font-family: 'Lato';\n"
                                    "background-color: #2ecc71;\n"
                                    "cursor: pointer;\n"
                                    "padding: 15px 20px;\n"
                                    "display: inline-block;\n"
                                    "text-transform: uppercase;\n"
                                    "letter-spacing: 1px;\n"
                                    "font-weight: 700;"
                                    )
        
        start_stop_layout.addWidget(self.startButton)  # Add startButton to the horizontal layout
        start_stop_layout.addWidget(self.stopButton)  # Add stopButton to the horizontal layout

        self.processButton = QPushButton(self.central_widget)
        self.processButton.setObjectName('processButton')
        self.processButton.setText('Process Data')
        self.processButton.setEnabled(True)
        self.processButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.processButton.clicked.connect(self.stop_button_task)
        self.processButton.clicked.connect(self.open_config_window)
        self.processButton.setStyleSheet("border: none;\n"
                                        "font-family: 'Lato';\n"
                                        "background-color: #FF8C00;\n"
                                        "cursor: pointer;\n"
                                        "padding: 15px 20px;\n"
                                        "display: inline-block;\n"
                                        "text-transform: uppercase;\n"
                                        "letter-spacing: 1px;\n"
                                        "font-weight: 700;"
                                        )

        self.headerLabel = QLabel(self.central_widget)
        self.headerLabel.setObjectName('headerLabel')
        self.headerLabel.setMinimumSize(QSize(800, 44))
        self.headerLabel.setMaximumSize(QSize(800, 44))
        self.headerLabel.setPixmap(QPixmap("interface/appheader.png"))

        self.plotLabel = QLabel(self.central_widget)
        self.plotLabel.setObjectName(u"plotLabel")
        
        sensor_plots = SensorPlots()

        self.layout.addWidget(self.headerLabel)
        self.layout.addWidget(sensor_plots.get_widget())
        self.layout.addLayout(start_stop_layout) 
        self.layout.addWidget(self.processButton)
        self.layout.addWidget(self.plotLabel)

        self.setCentralWidget(self.central_widget)
        
    def open_config_window(self):
        print("Opening Config Window")
        self.config_window = ConfigWindow()
        self.config_window.show()

    def checkboxStateChanged(self, state):
        if state == 0:
            print("Checkbox is unchecked")
        else:
            print("Checkbox is checked")

    def start_button_task(self):
        self.startButton.setEnabled(False)
        self.stopButton.setEnabled(True)
        self.startButton.setText('Scanning...')
        self.udp_thread1.start()
        self.udp_thread1.packet_received.connect(self.update_plot1)

        self.udp_thread2.start()
        self.udp_thread2.packet_received.connect(self.update_plot2)

        self.udp_thread3.start()
        self.udp_thread3.packet_received.connect(self.update_plot3)

    def stop_button_task(self):
        self.startButton.setEnabled(True)
        self.stopButton.setEnabled(False)
        self.startButton.setText('Start Scanning')

        # if self.udp_thread1.isRunning():
        #     self.udp_thread1.packet_received.disconnect(self.update_plot1)
        #     self.udp_thread1.stop()
        #     self.udp_thread1.wait()
        #     self.line.set_data([0], [0])
        #     self.canvas.draw()


    def update_plot1(self, distances):
        distances = np.array(distances)

        if len(distances) != 1800:
            print('Received partial scan data only. Discard current plot.')
        
        else:
            self.line1.set_data(self.angle, distances)
            self.canvas.draw()

    def update_plot2(self, distances):
        distances = np.array(distances)

        if len(distances) != 1800:
            print('Received partial scan data only. Discard current plot.')
        
        else:
            self.line2.set_data(self.angle, distances)
            self.canvas.draw()

    def update_plot3(self, distances):
        distances = np.array(distances)

        if len(distances) != 1800:
            print('Received partial scan data only. Discard current plot.')
        
        else:
            self.line3.set_data(self.angle, distances)
            self.canvas.draw()

    def update_formatting(self):
        # Get the QLineEdit widget that emitted the signal
        line_edit = self.sender()

        # Get the inputted text
        text = line_edit.text()

        # Convert the input to a float with 3 decimals
        try:
            value = float(text)
            line_edit.setText("{:.3f}".format(value))
        except ValueError:
            # Handle non-numeric input if desired
            line_edit.setText(str(0))

    
    def get_value(self, line_edit):
        # Get the inputted text from the specified QLineEdit
        input_text = line_edit.text()

        # Convert the input to a float, if desired
        try:
            value = float(input_text)
            # Save the input value to the dictionary using the line_edit as the key
            self.offsetInputValues[line_edit.objectName()] = value
            print(self.offsetInputValues)
        except ValueError:
            print("Invalid input")

# Create the PyQt5 application
app = QApplication([])

# Create the main window and show it
main_window = MainWindow()
main_window.show()

# Start the PyQt5 event loop
app.exec_()