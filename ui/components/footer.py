from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

class FooterWidget(QWidget):
    def __init__(self, version="1.2.4", parent=None):
        super().__init__(parent)
        self.version = version
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.footer_label = QLabel()
        self.set_version(self.version)
        self.footer_label.setFont(QFont("Hanken Grotesk", 14))
        self.footer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.footer_label.setOpenExternalLinks(True)
        layout.addWidget(self.footer_label)

        self.setStyleSheet("""
            QLabel {
                color: #333333;
                margin: 8px 0;
                background-color: #4ECDC4;  /* Add a background color to make the change more noticeable */
                padding: 5px;
                border-radius: 5px;
            }
            QLabel a {
                color: #FFFFFF;
                text-decoration: none;
            }
            QLabel a:hover {
                color: #F5F5F5;
                text-decoration: underline;
            }
        """)

    def set_version(self, version):
        self.version = version
        footer_text = f'UPDATED: Alpha {self.version} | Built in Singapore, <a href="https://www.linkedin.com/in/adibzailan/">AZ</a>'
        self.footer_label.setText(footer_text)