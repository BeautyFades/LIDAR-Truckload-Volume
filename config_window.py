from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from sensor_plots import SensorPlots


class ConfigWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sensor Settings")
        
        sidebar = Sidebar()
        
        content = QWidget()
        content_layout = QVBoxLayout()
        content_layout.addStretch(1)

        sensor_plots = SensorPlots()
        content_layout.addWidget(sensor_plots.get_widget())
        
        sensor_sliders = Sliders()
        content_layout.addWidget(sensor_sliders.get_widget())
        
        content.setLayout(content_layout)
        
        main_layout = QHBoxLayout()
        main_layout.addWidget(sidebar)
        main_layout.addWidget(content)
        self.setLayout(main_layout)
        
class Sidebar(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: lightgray;")
        # self.setMaximumWidth(220)
        
        sidebar_layout = QVBoxLayout()
        
        groups = [
            ("Left Sensor", ["Measure Offset", "Angle Offset (º)", "Sensor Height (m)"]),
            ("Top Sensor", ["Measure Offset", "Angle Offset (º)", "Sensor Height (m)"]),
            ("Right Sensor", ["Measure Offset", "Angle Offset (º)", "Sensor Height (m)"]),
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
                input_box.setRange(0, 1000)
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
        label1 = QLabel("Left Sensor")
        self.spin_box1 = QSpinBox()
        self.spin_box1.setRange(0, 100)
        self.spin_box1.valueChanged.connect(lambda value: self.slider1.setValue(value))
        self.slider1.valueChanged.connect(lambda value: self.spin_box1.setValue(value))

        self.slider2 = QSlider()
        self.slider2.setOrientation(Qt.Horizontal)
        label2 = QLabel("Top Sensor")
        self.spin_box2 = QSpinBox()
        self.spin_box2.setRange(0, 100)
        self.spin_box2.valueChanged.connect(lambda value: self.slider2.setValue(value))
        self.slider2.valueChanged.connect(lambda value: self.spin_box2.setValue(value))

        self.slider3 = QSlider()
        self.slider3.setOrientation(Qt.Horizontal)
        label3 = QLabel("Right Sensor") 
        self.spin_box3 = QSpinBox()
        self.spin_box3.setRange(0, 100)
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