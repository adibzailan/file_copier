from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from PyQt6.QtCore import pyqtSignal
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
        self.setLayout(layout)

        # Header
        header_layout = QHBoxLayout()
        header_label = QLabel(f"Copy Set {self.set_id}")
        remove_button = QPushButton("Remove")
        remove_button.clicked.connect(self.remove_set)
        header_layout.addWidget(header_label)
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
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        add_button = QPushButton("Add New Copy Set")
        add_button.clicked.connect(self.add_copy_set)
        self.layout.addWidget(add_button)

    def add_copy_set(self):
        new_set = CopySetWidget(len(self.copy_sets) + 1)
        new_set.removed.connect(self.remove_copy_set)
        new_set.folders_selected.connect(self.update_folders)
        self.copy_sets.append(new_set)
        self.layout.insertWidget(self.layout.count() - 1, new_set)
        self.set_added.emit(new_set)

    def remove_copy_set(self, copy_set):
        self.copy_sets.remove(copy_set)
        self.layout.removeWidget(copy_set)
        copy_set.deleteLater()
        self.set_removed.emit(copy_set)

    def update_folders(self, copy_set, source, destination):
        self.folders_updated.emit(copy_set, source, destination)