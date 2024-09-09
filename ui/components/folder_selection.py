from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton, QFileDialog
from PyQt6.QtGui import QFont
from PyQt6.QtCore import pyqtSignal

class FolderSelectionWidget(QWidget):
    folder_selected = pyqtSignal(str, str)

    def __init__(self, label_text, parent=None):
        super().__init__(parent)
        self.label_text = label_text
        self.setup_ui()

    def setup_ui(self):
        layout = QHBoxLayout()
        self.setLayout(layout)

        label = QLabel(self.label_text)
        label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        self.path_label = QLabel()
        self.path_label.setFont(QFont("Arial", 12))
        select_button = QPushButton("SELECT")
        select_button.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        select_button.clicked.connect(self.select_folder)

        layout.addWidget(label)
        layout.addWidget(self.path_label)
        layout.addWidget(select_button)

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, f"Select {self.label_text}")
        if folder:
            self.path_label.setText(folder)
            self.folder_selected.emit(self.label_text, folder)

    def set_path(self, path):
        self.path_label.setText(path)

    def get_path(self):
        return self.path_label.text()