from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton, QFileDialog, QLineEdit
from PyQt6.QtGui import QFont
from PyQt6.QtCore import pyqtSignal, Qt
from ..theme import Theme

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
        label.setStyleSheet(f"color: {Theme.TEXT}; background-color: transparent;")
        
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

        self.setStyleSheet(f"""
            FolderSelectionWidget {{
                margin-bottom: 8px;
            }}
            QLabel {{
                color: {Theme.TEXT};
                font-size: 14px;
                font-weight: bold;
                min-width: 80px;
                background-color: transparent;
            }}
            QLineEdit {{
                background-color: {Theme.SURFACE};
                color: {Theme.TEXT};
                border: 1px solid {Theme.BORDER};
                padding: 4px 8px;
                border-radius: 4px;
                font-size: 12px;
            }}
            QLineEdit:focus {{
                border: 1px solid {Theme.PRIMARY};
            }}
            QPushButton {{
                background-color: {Theme.PRIMARY};
                color: {Theme.TEXT};
                border: none;
                padding: 4px 12px;
                border-radius: 4px;
                font-family: 'Cerebri Sans';
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {Theme.PRIMARY}DD;
            }}
        """)

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(
            self,
            "Select Folder",
            "",
            QFileDialog.Option.ShowDirsOnly | QFileDialog.Option.DontResolveSymlinks
        )
        if folder:
            # Convert to proper Windows path format
            folder = folder.replace('/', '\\')
            print(f"Selected folder: {folder} for {self.label_text}")
            self.folder_path = folder
            self.path_input.setText(folder)
            folder_type = "source" if "Source" in self.label_text else "destination"
            print(f"Emitting folder_selected signal with type: {folder_type}")
            self.folder_selected.emit(folder_type, folder)

    def set_path(self, path):
        self.folder_path = path
        self.path_input.setText(path)

    def get_path(self):
        return self.folder_path