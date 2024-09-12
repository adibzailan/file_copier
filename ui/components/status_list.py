from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget, QListWidgetItem
from PyQt6.QtGui import QFont, QColor
from PyQt6.QtCore import Qt

class StatusListWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        status_label = QLabel("Status:")
        status_label.setFont(QFont("Cerebri Sans", 20, QFont.Weight.Bold))
        layout.addWidget(status_label)

        self.status_list = QListWidget()
        self.status_list.setFont(QFont("Hanken Grotesk", 14))
        self.status_list.setMinimumHeight(200)
        self.status_list.setMaximumHeight(400)
        layout.addWidget(self.status_list)

        self.setStyleSheet("""
            StatusListWidget {
                background-color: #F5F5F5;
                border: 2px solid #FF6F61;
                border-radius: 8px;
                padding: 8px;
                min-height: 300px;
            }
            QLabel {
                color: #333333;
                margin-bottom: 8px;
            }
            QListWidget {
                background-color: #FFFFFF;
                color: #333333;
                border: 1px solid #E0E0E0;
                border-radius: 8px;
                padding: 8px;
            }
            QListWidget::item {
                color: #333333;
                padding: 4px 0;
            }
            QListWidget::item:selected {
                background-color: #FF6F61;
                color: #FFFFFF;
            }
        """)

    def add_status(self, message):
        item = QListWidgetItem(message)
        item.setForeground(QColor("#333333"))  # Set text color to dark gray
        self.status_list.addItem(item)
        self.status_list.scrollToBottom()
        print(f"Debug: Status added to list - {message}")

    def clear_status(self):
        self.status_list.clear()
        print("Debug: Status list cleared")