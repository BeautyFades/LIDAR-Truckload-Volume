import numpy as np
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import *
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtCore import Qt, QTimer
from math import radians
from matplotlib.figure import Figure

from sensor_data_dict_format import top_sensor_dict

# Create a polar plot
class SensorPlots(QWidget):
    def __init__(self):
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        
        
        self.plt1 = self.figure.add_subplot(1, 3, 1)
        self.plt1.set_ylim(-3000, 3000)
        self.plt1.set_xlim(-2500, 500)

        # self.ax2 = self.figure.add_subplot(1, 3, 2, projection='polar')
        # self.ax2.set_theta_zero_location('N')
        # self.ax2.set_theta_direction(-1)
        # self.ax2.set_rlim(0, 3000)
        # self.ax2.set_rmax(3000)
        # self.line2, = self.ax2.plot([], [], 'b')

        # self.ax3 = self.figure.add_subplot(1, 3, 3, projection='polar')
        # self.ax3.set_theta_zero_location('N')
        # self.ax3.set_theta_direction(-1)
        # self.ax3.set_rlim(0, 3000)
        # self.ax3.set_rmax(3000)
        # self.line3, = self.ax3.plot([], [], 'b')
        
        self.figure.subplots_adjust(wspace=0.5)  # Increase the value to increase the spacing
        
    def get_widget(self):
        canvas = FigureCanvas(self.figure)

        widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(canvas)
        widget.setLayout(layout)

        return widget
    
    def update_plot1(self, dict_index):
        dict_values = top_sensor_dict.TOP[str(dict_index)]
        x_values_t = [t[1]           for t in dict_values]
        y_values_t = [t[0]           for t in dict_values]

        self.plt1.cla()
        self.plt1.plot(x_values_t, y_values_t, marker=None, color='black')
        self.canvas.draw_idle()
        