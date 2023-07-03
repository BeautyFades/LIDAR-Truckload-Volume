import numpy as np
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import *
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from math import radians

# Create a polar plot
class SensorPlots:
    def __init__(self):
        self.figure = plt.figure()
        
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
        
        self.figure.subplots_adjust(wspace=0.5)  # Increase the value to increase the spacing
        
    def get_widget(self):
        canvas = FigureCanvas(self.figure)
        # canvas.setMinimumSize(600, 400)

        widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(canvas)
        widget.setLayout(layout)

        return widget
    
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