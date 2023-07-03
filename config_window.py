from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QTimer
from sensor_plots import SensorPlots

class ConfigWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sensor Settings")
        
        sidebar = Sidebar()
        
        content = QWidget()
        content_layout = QVBoxLayout()

        sensor_plots = SensorPlots()
        content_layout.addWidget(sensor_plots.get_widget(), stretch=9)
        
        sensor_sliders = Sliders()
        content_layout.addWidget(sensor_sliders.get_widget(), stretch=1)
                
        content.setLayout(content_layout)
        
        main_layout = QHBoxLayout()
        main_layout.addWidget(sidebar)
        main_layout.addWidget(content)

        sensor_sliders.slider1.valueChanged.connect(lambda value: sensor_plots.update_plot_top(str(value),   sidebar.top_x_offset_mm,   sidebar.top_y_offset_mm, sidebar.top_angle_offset))
        sensor_sliders.slider2.valueChanged.connect(lambda value: sensor_plots.update_plot_left(str(value),  sidebar.left_x_offset_mm,  sidebar.left_y_offset_mm, sidebar.left_angle_offset))
        sensor_sliders.slider3.valueChanged.connect(lambda value: sensor_plots.update_plot_right(str(value), sidebar.right_x_offset_mm, sidebar.right_y_offset_mm, sidebar.right_angle_offset))



        sidebar.top_x_offset_mm.valueChanged.connect(lambda value: sensor_plots.update_plot_top(str(sensor_sliders.slider1.value()), sidebar.top_x_offset_mm, sidebar.top_y_offset_mm, sidebar.top_angle_offset))
        sidebar.top_y_offset_mm.valueChanged.connect(lambda value: sensor_plots.update_plot_top(str(sensor_sliders.slider1.value()), sidebar.top_x_offset_mm, sidebar.top_y_offset_mm, sidebar.top_angle_offset))
        sidebar.top_angle_offset.valueChanged.connect(lambda value: sensor_plots.update_plot_top(str(sensor_sliders.slider1.value()), sidebar.top_x_offset_mm, sidebar.top_y_offset_mm, sidebar.top_angle_offset))



        sidebar.left_x_offset_mm.valueChanged.connect(lambda value: sensor_plots.update_plot_left(str(sensor_sliders.slider2.value()), sidebar.left_x_offset_mm, sidebar.left_y_offset_mm, sidebar.left_angle_offset))
        sidebar.left_y_offset_mm.valueChanged.connect(lambda value: sensor_plots.update_plot_left(str(sensor_sliders.slider2.value()), sidebar.left_x_offset_mm, sidebar.left_y_offset_mm, sidebar.left_angle_offset))
        sidebar.left_angle_offset.valueChanged.connect(lambda value: sensor_plots.update_plot_left(str(sensor_sliders.slider2.value()), sidebar.left_x_offset_mm, sidebar.left_y_offset_mm, sidebar.left_angle_offset))




        sidebar.right_x_offset_mm.valueChanged.connect(lambda value: sensor_plots.update_plot_right(str(sensor_sliders.slider3.value()), sidebar.right_x_offset_mm, sidebar.right_y_offset_mm, sidebar.right_angle_offset))
        sidebar.right_y_offset_mm.valueChanged.connect(lambda value: sensor_plots.update_plot_right(str(sensor_sliders.slider3.value()), sidebar.right_x_offset_mm, sidebar.right_y_offset_mm, sidebar.right_angle_offset))
        sidebar.right_angle_offset.valueChanged.connect(lambda value: sensor_plots.update_plot_right(str(sensor_sliders.slider3.value()), sidebar.right_x_offset_mm, sidebar.right_y_offset_mm, sidebar.right_angle_offset))
        self.setLayout(main_layout)

        
class Sidebar(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: lightgray;")
        
        sidebar_layout = QVBoxLayout()
        
        groups = [
            ("Top Sensor", [  "Angle Offset", "X Offset mm", "Y Offset mm"]),
            ("Left Sensor", [ "Angle Offset", "X Offset mm", "Y Offset mm"]),
            ("Right Sensor", ["Angle Offset", "X Offset mm", "Y Offset mm"]),
        ]
        
        for group_label, inputs in groups:
            group_widget = QWidget()
            group_layout = QFormLayout(group_widget)
            
            group_label_widget = QLabel(group_label)
            group_label_widget.setStyleSheet("font-weight: bold; text-align:center;")
            group_layout.addRow(group_label_widget)
            
            for input_label in inputs:
                label = QLabel(input_label)
                if input_label == "Measure Offset":
                    input_box = QSpinBox()
                else:
                    input_box = QDoubleSpinBox()
                    input_box.setSingleStep(1)  # Set the step to 1
                input_box.setRange(-2000, 2000)
                group_layout.addRow(label, input_box)
                
                # Dynamically store variables for each input on self
                var_name = f"{group_label.split(' ')[0]}_{input_label}".lower().replace(" ", "_")
                setattr(self, var_name, input_box)
                
                input_box.valueChanged.connect(lambda value, var=var_name: setattr(self, var, value))
                input_box.valueChanged.connect(lambda value, var=var_name: print(f"{var} = {value}"))
                            
            sidebar_layout.addWidget(group_widget)
        
        self.setLayout(sidebar_layout)        
        
class Sliders(QWidget):
    def __init__(self):
        super().__init__()
        # Add sliders below each polar plot
        self.slider1 = QSlider()
        self.slider1.setOrientation(Qt.Horizontal)
        self.slider1.setMaximum(548)
        label1 = QLabel("Top Sensor")
        self.spin_box1 = QSpinBox()
        self.spin_box1.setRange(0, 548)
        self.spin_box1.valueChanged.connect(lambda value: self.slider1.setValue(value))
        self.slider1.valueChanged.connect(lambda value: self.spin_box1.setValue(value))

        self.slider2 = QSlider()
        self.slider2.setOrientation(Qt.Horizontal)
        self.slider2.setMaximum(705)
        label2 = QLabel("Left Sensor")
        self.spin_box2 = QSpinBox()
        self.spin_box2.setRange(0, 705)
        self.spin_box2.valueChanged.connect(lambda value: self.slider2.setValue(value))
        self.slider2.valueChanged.connect(lambda value: self.spin_box2.setValue(value))

        self.slider3 = QSlider()
        self.slider3.setOrientation(Qt.Horizontal)
        self.slider3.setMaximum(802)
        label3 = QLabel("Right Sensor") 
        self.spin_box3 = QSpinBox()
        self.spin_box3.setRange(0, 802)
        self.spin_box3.valueChanged.connect(lambda value: self.slider3.setValue(value))
        self.slider3.valueChanged.connect(lambda value: self.spin_box3.setValue(value))        

        sliders_layout = QHBoxLayout()
        sliders_layout.addWidget(label1)
        sliders_layout.addWidget(self.slider1)
        sliders_layout.addWidget(self.spin_box1)
        sliders_layout.addWidget(label2)
        sliders_layout.addWidget(self.slider2)
        sliders_layout.addWidget(self.spin_box2)
        sliders_layout.addWidget(label3)
        sliders_layout.addWidget(self.slider3)
        sliders_layout.addWidget(self.spin_box3)
        
        self.setLayout(sliders_layout)
        
    def get_data_range(self, data):
        '''
        Receives the data measures file
        Returns min and max values of data measures
        '''
        return [list(data)[0], list(data)[-1]]
        
        
    def get_widget(self):
        return self