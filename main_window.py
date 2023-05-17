import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from udp_server_thread import UDPServerThread
from math import radians

# Create a PyQt5 main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("UFSC - Coontrol - LiDAR Volume Measurement")
        self.setWindowIcon(QIcon("interface/coontrol-icon.png"))
        self.resize(800, 600)

        self.setMinimumSize(QSize(800, 600))
        self.setMaximumSize(QSize(800, 600))

        self.central_widget = QWidget(self)
        self.central_widget.setObjectName('centralwidget')
        layout = QVBoxLayout()
        self.central_widget.setLayout(layout)
        self.setCentralWidget(self.central_widget)

        self.stopButton = QPushButton(self.central_widget)
        self.stopButton.setObjectName('stopButton')
        self.stopButton.setText('Stop Scanning')
        self.stopButton.setGeometry(QRect(630, 550, 161, 41))
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
        self.udp_thread = UDPServerThread(verbose=False)

        # Create a polar plot
        self.ax = self.figure.add_subplot(1, 1, 1, projection='polar')
        self.ax.set_theta_zero_location('N')
        self.ax.set_theta_direction(-1)
        self.ax.set_rlim(0, 800)
        self.ax.set_rmax(800)
        self.angle = [radians(a / 10) for a in range(0, 3600, 2)]
        self.line, = self.ax.plot([], [], 'b')


    def start_button_task(self):
        self.startButton.setEnabled(False)
        self.stopButton.setEnabled(True)
        self.startButton.setText('Scanning...')
        self.udp_thread.start()
        self.udp_thread.packet_received.connect(self.update_plot)
        

    def stop_button_task(self):
        self.startButton.setEnabled(True)
        self.stopButton.setEnabled(False)
        self.startButton.setText('Start Scanning')

        if self.udp_thread.isRunning():
            self.udp_thread.packet_received.disconnect(self.update_plot)
            self.udp_thread.stop()
            self.udp_thread.wait()
            self.line.set_data([0], [0])
            self.canvas.draw()


    def update_plot(self, distances):
        distances = np.array(distances)

        if len(distances) != 1800:
            print('Received partial scan data only. Discard current plot.')
        
        else:
            self.line.set_data(self.angle, distances)
            self.canvas.draw()


# Create the PyQt5 application
app = QApplication([])


# Create the main window and show it
main_window = MainWindow()
main_window.show()

# Start the PyQt5 event loop
app.exec_()