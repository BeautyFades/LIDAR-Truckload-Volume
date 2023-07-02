DATA = {
    1: [86, 132, 84, 124, 97],
    2: [128, 73, 96, 99, 121],
    3: [97, 123, 66, 88, 111],
    4: [95, 74, 102, 127, 65],
    5: [78, 99, 102, 111, 86]
}
from PyQt5.QtWidgets import QApplication, QMainWindow, QSlider, QLabel, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt

def slider_value_changed(value):
    selected_index = value + 1  # Adjusting the index to match dictionary keys
    label.setText(f"Selected Index: {selected_index}")
    selected_value = DATA.get(selected_index)
    if selected_value is not None:
        value_label.setText(f"Value: {selected_value}")
    else:
        value_label.setText("Value: N/A")

app = QApplication([])
window = QMainWindow()
window.setWindowTitle("Index Selector")
central_widget = QWidget()
window.setCentralWidget(central_widget)
layout = QVBoxLayout()
central_widget.setLayout(layout)

label = QLabel("Selected Index: 1")
layout.addWidget(label)

slider = QSlider(Qt.Horizontal)
slider.setMinimum(0)  # Adjust if necessary
slider.setMaximum(len(DATA) - 1)  # Adjust if necessary
slider.valueChanged.connect(slider_value_changed)
layout.addWidget(slider)

value_label = QLabel("Value: ")
layout.addWidget(value_label)

window.show()
app.exec()
