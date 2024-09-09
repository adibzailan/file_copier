from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget
from PyQt6.QtGui import QFont

class StatusListWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        status_label = QLabel("STATUS:")
        status_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        layout.addWidget(status_label)

        self.status_list = QListWidget()
        self.status_list.setFont(QFont("Arial", 12))
        layout.addWidget(self.status_list)

    def add_status(self, message):
        self.status_list.addItem(message)
        self.status_list.scrollToBottom()

    def clear_status(self):
        self.status_list.clear()