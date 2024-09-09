from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt

class FooterWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        footer_label = QLabel('Alpha 1.1.0 | Built in Singapore, <a href="https://www.linkedin.com/in/adibzailan/">AZ</a>')
        footer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        footer_label.setOpenExternalLinks(True)
        layout.addWidget(footer_label)