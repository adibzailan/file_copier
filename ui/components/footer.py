from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

class FooterWidget(QWidget):
    def __init__(self, version="v2.0.0", parent=None):
        super().__init__(parent)
        self.version = version
        self.setup_ui()

    def setup_ui(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(8, 4, 8, 4)
        self.setLayout(layout)

        self.version_label = QLabel(f"{self.version}")
        self.version_label.setFont(QFont("Cerebri Sans", 10))
        self.version_label.setStyleSheet("color: #CCCCCC;")
        layout.addWidget(self.version_label)
        layout.addStretch()

    def set_version(self, version):
        self.version = version
        self.version_label.setText(self.version)