from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import matplotlib.pyplot as plt
import sys
import random
import time
import plotter_class


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("UFSC - Coontrol - LiDAR Volume Measurement")
        self.setWindowIcon(QIcon("interface/coontrol-icon.png"))
        self.resize(800, 600)

        self.setMinimumSize(QSize(800, 600))
        self.setMaximumSize(QSize(800, 600))
        self.centralwidget = QWidget()
        self.centralwidget.setObjectName('centralwidget')

        self.stopButton = QPushButton(self.centralwidget)
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
        
        self.startButton = QPushButton(self.centralwidget)
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
        
    
        
        self.headerLabel = QLabel(self.centralwidget)
        self.headerLabel.setObjectName('headerLabel')
        self.headerLabel.setGeometry(QRect(0, 0, 800, 44))
        self.headerLabel.setMinimumSize(QSize(800, 44))
        self.headerLabel.setMaximumSize(QSize(800, 44))
        self.headerLabel.setPixmap(QPixmap("interface/appheader.png"))

        self.plotLabel = QLabel(self.centralwidget)
        self.plotLabel.setObjectName(u"plotLabel")
        self.plotLabel.setGeometry(QRect(10, 50, 541, 491))
        self.setCentralWidget(self.centralwidget)
        self.layout = QVBoxLayout(self.plotLabel)

        QMetaObject.connectSlotsByName(self)

        # Create the plotting worker
        self.plotting_worker = plotter_class.PlottingWorker()
        self.plotting_thread = QThread()
        self.plotting_worker.moveToThread(self.plotting_thread)
        self.plotting_worker.data_ready.connect(self.update_plot)
        self.plotting_thread.started.connect(self.plotting_worker.start)


    def start_button_task(self):
        # Placeholder for your long-running task
        print("Start button clicked!")
        self.startButton.setEnabled(False)
        self.stopButton.setEnabled(True)
        self.startButton.setText('Scanning...')
        self.start_plotting()


    def stop_button_task(self):
        # Placeholder for your long-running task
        print("Stop button clicked!")
        self.startButton.setEnabled(True)
        self.stopButton.setEnabled(False)
        self.startButton.setText('Start Scanning')

        if (len(self.layout) == 1):
            plt.close()


    def start_plotting(self):
        if (len(self.layout) < 1):
            # Create the plot
            self.fig, self.ax = plt.subplots()
            self.line, = self.ax.plot([], [])
            # Add the plot to the layout
            self.layout.addWidget(self.fig.canvas)
            print(type(len(self.layout)))
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
