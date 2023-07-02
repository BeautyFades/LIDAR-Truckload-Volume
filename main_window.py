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

# Create a PyQt5 main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.offsetInputValues = {}

        self.setWindowTitle("UFSC - Coontrol - LiDAR Volume Measurement")
        self.setWindowIcon(QIcon("interface/coontrol-icon.png"))
        self.resize(800, 600)

        self.setMinimumSize(QSize(800, 600))
        self.setMaximumSize(QSize(800, 600))

        self.central_widget = QWidget(self)
        self.central_widget.setObjectName('centralWidget')
        layout = QVBoxLayout()
        self.central_widget.setLayout(layout)
        self.setCentralWidget(self.central_widget)

        self.topSensorLabel = QLabel('Top Sensor Offsets:', self)
        self.topSensorLabel.setObjectName('topSensorLabel')
        self.topSensorLabel.move(630, 120)
        

        self.topSensorAngleValidator = QDoubleValidator()
        self.topSensorAngleValidator.setDecimals(4)
        self.topSensorAngleValidator.setRange(-90, 90)
        self.topSensorAngleBox = QLineEdit(self)
        self.topSensorAngleBox.setObjectName('topSensorAngleBox')
        self.topSensorAngleBox.setValidator(self.topSensorAngleValidator)
        self.topSensorAngleBox.textChanged.connect(self.update_formatting)
        self.topSensorAngleBox.textChanged.connect(lambda: self.get_value(self.topSensorAngleBox))


        self.stopButton = QPushButton(self.central_widget)
        self.stopButton.setObjectName('stopButton')
        self.stopButton.setText('Stop Scanning')
        self.stopButton.setGeometry(QRect(630, 550, 161, 41))
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
        self.startButton.setGeometry(QRect(460, 550, 161, 41))
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
        
        self.processButton = QPushButton(self.central_widget)
        self.processButton.setObjectName('processButton')
        self.processButton.setText('Process Data')
        self.processButton.setGeometry(QRect(630, 55, 161, 41))
        self.processButton.setEnabled(True)
        self.processButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.processButton.clicked.connect(self.stop_button_task)
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
        self.headerLabel.setGeometry(QRect(0, 0, 800, 44))
        self.headerLabel.setMinimumSize(QSize(800, 44))
        self.headerLabel.setMaximumSize(QSize(800, 44))
        self.headerLabel.setPixmap(QPixmap("interface/appheader.png"))

        self.plotLabel = QLabel(self.central_widget)
        self.plotLabel.setObjectName(u"plotLabel")
        self.plotLabel.setGeometry(QRect(10, 50, 541, 491))
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout(self.plotLabel)

        QMetaObject.connectSlotsByName(self)

        # Create a FigureCanvas to display the polar plot
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        # Create the UDP server thread and start it
        self.udp_thread1 = UDPServerThread(ip_address='127.0.0.1', udp_port=54321, verbose=False)
        self.udp_thread2 = UDPServerThread(ip_address='127.0.0.1', udp_port=54322, verbose=False)
        self.udp_thread3 = UDPServerThread(ip_address='127.0.0.1', udp_port=54323, verbose=False)

        # Create a polar plot
        self.angle = [radians(a / 10) for a in range(0, 3600, 2)]
        
        self.ax1 = self.figure.add_subplot(1, 3, 1, projection='polar')
        self.ax1.set_theta_zero_location('N')
        self.ax1.set_theta_direction(-1)
        self.ax1.set_rlim(0, 3000)
        self.ax1.set_rmax(3000)
        self.line1, = self.ax1.plot([], [], 'b')

        self.ax2 = self.figure.add_subplot(1, 3, 2, projection='polar')
        self.ax2.set_theta_zero_location('N')
        self.ax2.set_theta_direction(-1)
        self.ax2.set_rlim(0, 3000)
        self.ax2.set_rmax(3000)
        self.line2, = self.ax2.plot([], [], 'b')

        self.ax3 = self.figure.add_subplot(1, 3, 3, projection='polar')
        self.ax3.set_theta_zero_location('N')
        self.ax3.set_theta_direction(-1)
        self.ax3.set_rlim(0, 3000)
        self.ax3.set_rmax(3000)
        self.line3, = self.ax3.plot([], [], 'b')

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

        if self.udp_thread1.isRunning():
            self.udp_thread1.packet_received.disconnect(self.update_plot)
            self.udp_thread1.stop()
            self.udp_thread1.wait()
            self.line.set_data([0], [0])
            self.canvas.draw()


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