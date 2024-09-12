from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

class FooterWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        footer_label = QLabel('Alpha 1.1.0 | Built in Singapore, <a href="https://www.linkedin.com/in/adibzailan/">AZ</a>')
        footer_label.setFont(QFont("Hanken Grotesk", 14))
        footer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        footer_label.setOpenExternalLinks(True)
        layout.addWidget(footer_label)

        self.setStyleSheet("""
            QLabel {
                color: #333333;
                margin: 8px 0;
            }
            QLabel a {
                color: #FF6F61;
                text-decoration: none;
            }
            QLabel a:hover {
                text-decoration: underline;
            }
        """)

    def set_version(self, version):
        footer_text = f'Alpha {version} | Built in Singapore, <a href="https://www.linkedin.com/in/adibzailan/">AZ</a>'
        self.findChild(QLabel).setText(footer_text)