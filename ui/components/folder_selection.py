from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton, QFileDialog, QLineEdit
from PyQt6.QtGui import QFont
from PyQt6.QtCore import pyqtSignal, Qt

class FolderSelectionWidget(QWidget):
    folder_selected = pyqtSignal(str, str)

    def __init__(self, label_text, parent=None):
        super().__init__(parent)
        self.label_text = label_text
        self.folder_path = ""
        self.setup_ui()

    def setup_ui(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)
        self.setLayout(layout)

        label = QLabel(self.label_text)
        label.setFont(QFont("Cerebri Sans", 14, QFont.Weight.Bold))
        self.path_input = QLineEdit()
        self.path_input.setFont(QFont("Hanken Grotesk", 12))
        self.path_input.setReadOnly(True)
        self.path_input.setPlaceholderText("Select a folder...")
        select_button = QPushButton("Select")
        select_button.setFont(QFont("Cerebri Sans", 12, QFont.Weight.Bold))
        select_button.clicked.connect(self.select_folder)

        layout.addWidget(label)
        layout.addWidget(self.path_input, 1)  # Give the path input more space
        layout.addWidget(select_button)

        self.setStyleSheet("""
            FolderSelectionWidget {
                margin-bottom: 8px;
            }
            QLabel {
                color: #333333;
                font-size: 14px;
                font-weight: bold;
                min-width: 80px;
            }
            QLineEdit {
                background-color: #FFFFFF;
                color: #333333;
                border: 1px solid #E0E0E0;
                padding: 4px 8px;
                border-radius: 4px;
                font-size: 12px;
            }
            QLineEdit:focus {
                border: 1px solid #FF6F61;
            }
            QPushButton {
                background-color: #FF6F61;
                color: #FFFFFF;
                border: none;
                padding: 4px 12px;
                font-family: 'Cerebri Sans';
                font-weight: bold;
                border-radius: 4px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #FF8D82;
            }
        """)

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, f"Select {self.label_text}")
        if folder:
            self.folder_path = folder
            self.path_input.setText(folder)
            self.folder_selected.emit(self.label_text, folder)

    def set_path(self, path):
        self.folder_path = path
        self.path_input.setText(path)

    def get_path(self):
        return self.folder_path