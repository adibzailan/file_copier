from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QSlider, QLineEdit
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QIntValidator
from ..theme import Theme

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
        interval_label.setStyleSheet(f"color: {Theme.TEXT}; background-color: transparent;")

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

        self.setStyleSheet(f"""
            QLabel {{ 
                color: {Theme.TEXT};
                font-size: 16px;
                font-weight: bold;
                background-color: transparent;
            }}
            QSlider::groove:horizontal {{ 
                border: 1px solid {Theme.BORDER};
                height: 8px;
                background: {Theme.SURFACE};
                margin: 2px 0;
                border-radius: 4px;
            }}
            QSlider::handle:horizontal {{ 
                background: {Theme.PRIMARY};
                border: none;
                width: 18px;
                margin: -6px 0;
                border-radius: 9px;
            }}
            QSlider::sub-page:horizontal {{ 
                background: {Theme.PRIMARY};
                border-radius: 4px;
            }}
            QSlider::add-page:horizontal {{ 
                background: {Theme.SURFACE};
                border-radius: 4px;
            }}
            QLineEdit {{ 
                color: {Theme.TEXT};
                background-color: {Theme.SURFACE};
                border: 1px solid {Theme.BORDER};
                border-radius: 4px;
                padding: 4px;
            }}
            QLineEdit:focus {{ 
                border: 1px solid {Theme.PRIMARY};
            }}
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

    def get_interval(self):
        return self.interval_slider.value()