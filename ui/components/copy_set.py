from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QGridLayout
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QFont
from .folder_selection import FolderSelectionWidget

class CopySetWidget(QWidget):
    removed = pyqtSignal(object)
    folders_selected = pyqtSignal(object, str, str)

    def __init__(self, set_id):
        super().__init__()
        self.set_id = set_id
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(4)
        self.setLayout(layout)

        # Header
        header_layout = QHBoxLayout()
        header_label = QLabel(f"Copy Set {self.set_id}")
        header_label.setFont(QFont("Cerebri Sans", 16, QFont.Weight.Bold))
        remove_button = QPushButton("Remove")
        remove_button.setFont(QFont("Cerebri Sans", 12, QFont.Weight.Bold))
        remove_button.clicked.connect(self.remove_set)
        header_layout.addWidget(header_label)
        header_layout.addStretch(1)
        header_layout.addWidget(remove_button)
        layout.addLayout(header_layout)

        # Folder selections
        self.source_folder = FolderSelectionWidget("Source:")
        self.dest_folder = FolderSelectionWidget("Destination:")
        layout.addWidget(self.source_folder)
        layout.addWidget(self.dest_folder)

        # Connect signals
        self.source_folder.folder_selected.connect(self.update_folders)
        self.dest_folder.folder_selected.connect(self.update_folders)

        self.setStyleSheet("""
            CopySetWidget {
                background-color: #FFFFFF;
                border: 1px solid #E0E0E0;
                border-radius: 4px;
            }
            QLabel {
                color: #333333;
                font-family: 'Cerebri Sans';
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton {
                background-color: #FF6F61;
                color: #FFFFFF;
                border: none;
                padding: 4px 8px;
                font-family: 'Cerebri Sans';
                font-weight: bold;
                border-radius: 4px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #FF8D82;
            }
        """)

    def remove_set(self):
        self.removed.emit(self)

    def update_folders(self):
        source = self.source_folder.get_path()
        destination = self.dest_folder.get_path()
        if source and destination:
            self.folders_selected.emit(self, source, destination)

class CopySetManager(QWidget):
    set_added = pyqtSignal(object)
    set_removed = pyqtSignal(object)
    folders_updated = pyqtSignal(object, str, str)

    def __init__(self):
        super().__init__()
        self.copy_sets = []
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(8)
        self.setLayout(main_layout)

        self.grid_layout = QGridLayout()
        self.grid_layout.setHorizontalSpacing(8)
        self.grid_layout.setVerticalSpacing(8)
        main_layout.addLayout(self.grid_layout)

        add_button = QPushButton("Add New Copy Set")
        add_button.setFont(QFont("Cerebri Sans", 14, QFont.Weight.Bold))
        add_button.clicked.connect(self.add_copy_set)
        main_layout.addWidget(add_button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setStyleSheet("""
            CopySetManager {
                background-color: #F5F5F5;
            }
            QPushButton {
                background-color: #FF6F61;
                color: #FFFFFF;
                border: none;
                padding: 8px 16px;
                font-family: 'Cerebri Sans';
                font-weight: bold;
                border-radius: 4px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #FF8D82;
            }
        """)

    def add_copy_set(self):
        new_set = CopySetWidget(len(self.copy_sets) + 1)
        new_set.removed.connect(self.remove_copy_set)
        new_set.folders_selected.connect(self.update_folders)
        self.copy_sets.append(new_set)
        
        row = (len(self.copy_sets) - 1) // 2
        col = (len(self.copy_sets) - 1) % 2
        self.grid_layout.addWidget(new_set, row, col)
        
        self.set_added.emit(new_set)

    def remove_copy_set(self, copy_set):
        self.copy_sets.remove(copy_set)
        self.grid_layout.removeWidget(copy_set)
        copy_set.deleteLater()
        self.set_removed.emit(copy_set)
        self.reorganize_grid()

    def reorganize_grid(self):
        for i, copy_set in enumerate(self.copy_sets):
            row = i // 2
            col = i % 2
            self.grid_layout.addWidget(copy_set, row, col)

    def update_folders(self, copy_set, source, destination):
        self.folders_updated.emit(copy_set, source, destination)