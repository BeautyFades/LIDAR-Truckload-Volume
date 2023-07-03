import numpy as np
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import *
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtCore import Qt, QTimer
from math import radians
from matplotlib.figure import Figure

from sensor_data_dict_format import top_sensor_dict
from sensor_data_dict_format import left_sensor_dict
from sensor_data_dict_format import right_sensor_dict

# Create a polar plot
class SensorPlots():
    def __init__(self):
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        
        self.plt1 = self.figure.add_subplot(111)
        self.plt1.set_ylim(-2500, 500)
        self.plt1.set_xlim(-1500, 1500)

        self.line1, = self.plt1.plot(0, 0, label='Top', color='black')
        self.line2, = self.plt1.plot(0, 0, label='Left', color='blue')
        self.line3, = self.plt1.plot(0, 0, label='Right', color='red')
        
    def get_widget(self):
        widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        widget.setLayout(layout)

        return widget
    
    def update_plot_top(self, dict_index, x_offset, y_offset):
        dict_values_top = top_sensor_dict.TOP[str(dict_index)]

        x_values_t = [t[1] + x_offset          for t in dict_values_top]
        y_values_t = [t[0] + y_offset          for t in dict_values_top]
        print(x_values_t)

        self.line1.set_data(x_values_t, y_values_t)
        self.canvas.draw_idle()

    def update_plot_left(self, dict_index):
        update_plot_left = left_sensor_dict.LEFT[str(dict_index)]

        x_values_l = [t[1]*-1 - 1226 for t in update_plot_left]
        y_values_l = [t[0]    - 1020 for t in update_plot_left]

        self.line2.set_data(x_values_l, y_values_l)
        self.canvas.draw_idle()

    def update_plot_right(self, dict_index):
        dict_values_right = right_sensor_dict.RIGHT[str(dict_index)]

        x_values_r = [t[1]    + 1180 for t in dict_values_right]
        y_values_r = [t[0]    - 1070 for t in dict_values_right]

        self.line3.set_data(x_values_r, y_values_r)
        self.canvas.draw_idle()