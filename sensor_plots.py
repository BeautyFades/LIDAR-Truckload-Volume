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
        self.plt1.grid(True)

        self.line1, = self.plt1.plot(0, 0, label='Top', color='black')
        self.line2, = self.plt1.plot(0, 0, label='Left', color='blue')
        self.line3, = self.plt1.plot(0, 0, label='Right', color='red')
        
    def get_widget(self):
        widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        widget.setLayout(layout)

        return widget
    
    def update_plot_top(self, dict_index, x_offset, y_offset, rotation_angle):
        dict_values_top = top_sensor_dict.TOP[str(dict_index)]

        if isinstance(x_offset, QDoubleSpinBox):
            x_offset = x_offset.value()
        else:
            x_offset = float(x_offset)

        if isinstance(y_offset, QDoubleSpinBox):
            y_offset = y_offset.value()
        else:
            y_offset = float(y_offset)

        if isinstance(rotation_angle, QDoubleSpinBox):
            rotation_angle = rotation_angle.value()
        else:
            rotation_angle = float(rotation_angle)

        dict_values_top = self.rotate_points(dict_values_top, rotation_angle)

        x_values_t = [t[1] + float(x_offset)          for t in dict_values_top]
        y_values_t = [t[0] + float(y_offset)          for t in dict_values_top]
        print(x_values_t)

        self.line1.set_data(x_values_t, y_values_t)
        self.canvas.draw_idle()

    def update_plot_left(self, dict_index, x_offset, y_offset, rotation_angle):
        dict_values_left = left_sensor_dict.LEFT[str(dict_index)]

        if isinstance(x_offset, QDoubleSpinBox):
            x_offset = x_offset.value()
        else:
            x_offset = float(x_offset)

        if isinstance(y_offset, QDoubleSpinBox):
            y_offset = y_offset.value()
        else:
            y_offset = float(y_offset)

        if isinstance(rotation_angle, QDoubleSpinBox):
            rotation_angle = rotation_angle.value()
        else:
            rotation_angle = float(rotation_angle)

        dict_values_left = self.rotate_points(dict_values_left, rotation_angle)

        x_values_l = [t[1]*-1 - 1226 + float(x_offset) for t in dict_values_left]
        y_values_l = [t[0]    - 1020 + float(y_offset) for t in dict_values_left]

        self.line2.set_data(x_values_l, y_values_l)
        self.canvas.draw_idle()

    def update_plot_right(self, dict_index, x_offset, y_offset, rotation_angle):
        dict_values_right = right_sensor_dict.RIGHT[str(dict_index)]

        if isinstance(x_offset, QDoubleSpinBox):
            x_offset = x_offset.value()
        else:
            x_offset = float(x_offset)

        if isinstance(y_offset, QDoubleSpinBox):
            y_offset = y_offset.value()
        else:
            y_offset = float(y_offset)

        if isinstance(rotation_angle, QDoubleSpinBox):
            rotation_angle = rotation_angle.value()
        else:
            rotation_angle = float(rotation_angle)

        dict_values_right = self.rotate_points(dict_values_right, rotation_angle)

        x_values_r = [t[1]    + 1180 + float(x_offset) for t in dict_values_right]
        y_values_r = [t[0]    - 1070 + float(y_offset) for t in dict_values_right]

        self.line3.set_data(x_values_r, y_values_r)
        self.canvas.draw_idle()

    def rotate_points(self, points, angle):
        points_array = np.array(points)
        x = points_array[:, 0]
        y = points_array[:, 1]
        pivot = (0, 0)

        # Calculate the translation vector to move the pivot point to the origin
        translation = -np.array(pivot)
        translated_x = x + translation[0]
        translated_y = y + translation[1]

        # Apply the rotation transformation
        theta = np.radians(angle)
        rotated_x = np.cos(theta) * translated_x - np.sin(theta) * translated_y
        rotated_y = np.sin(theta) * translated_x + np.cos(theta) * translated_y

        # Translate the points back to the original position
        translated_back_x = rotated_x - translation[0]
        translated_back_y = rotated_y - translation[1]

        # Combine translated back x and y coordinates into points array
        translated_back_points = np.column_stack((translated_back_x, translated_back_y))

        # Convert the NumPy array back to a list of tuples
        rotated_points_list = translated_back_points.tolist()

        return rotated_points_list