from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QSlider, QLineEdit
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QIntValidator

class IntervalSettingsWidget(QWidget):
    interval_changed = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        layout = QHBoxLayout()
        self.setLayout(layout)

        interval_label = QLabel("Copy Interval (minutes):")
        interval_label.setFont(QFont("Cerebri Sans", 16, QFont.Weight.Bold))

        self.interval_slider = QSlider(Qt.Orientation.Horizontal)
        self.interval_slider.setMinimum(1)
        self.interval_slider.setMaximum(60)
        self.interval_slider.setValue(30)
        self.interval_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.interval_slider.setTickInterval(5)

        self.interval_input = QLineEdit()
        self.interval_input.setFont(QFont("Hanken Grotesk", 16))
        self.interval_input.setValidator(QIntValidator(1, 60))
        self.interval_input.setText("30")
        self.interval_input.setFixedWidth(50)

        self.interval_slider.valueChanged.connect(self.update_interval_input)
        self.interval_input.textChanged.connect(self.update_interval_slider)

        layout.addWidget(interval_label)
        layout.addWidget(self.interval_slider)
        layout.addWidget(self.interval_input)

        self.setStyleSheet("""
            QLabel {
                color: #333333;
                font-size: 16px;
                font-weight: bold;
            }
            QSlider::groove:horizontal {
                border: 1px solid #E0E0E0;
                height: 8px;
                background: #FFFFFF;
                margin: 2px 0;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: #FF6F61;
                border: 1px solid #FF6F61;
                width: 18px;
                margin: -2px 0;
                border-radius: 9px;
            }
            QLineEdit {
                background-color: #FFFFFF;
                color: #333333;
                border: 2px solid #E0E0E0;
                padding: 4px 8px;
                border-radius: 8px;
                font-size: 16px;
            }
        """)

    def update_interval_input(self, value):
        self.interval_input.setText(str(value))
        self.interval_changed.emit(value)

    def update_interval_slider(self, text):
        if text and text.isdigit():
            value = int(text)
            if 1 <= value <= 60:
                self.interval_slider.setValue(value)
                self.interval_changed.emit(value)

    def set_interval(self, value):
        self.interval_slider.setValue(value)
        self.interval_input.setText(str(value))

    def get_interval(self):
        return int(self.interval_input.text())