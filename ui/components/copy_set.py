from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QGridLayout
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QFont
from .folder_selection import FolderSelectionWidget
from .file_selector import FileSelector
from .sync_control import SyncControl
from ..theme import Theme

class CopySetWidget(QWidget):
    removed = pyqtSignal(object)
    folders_selected = pyqtSignal(object, str, str)  # widget, folder_type, path
    files_selected = pyqtSignal(int, list)  # set_id, files
    sync_started = pyqtSignal(object)
    sync_stopped = pyqtSignal(object)

    def __init__(self, set_id):
        super().__init__()
        self.set_id = set_id
        self.selected_files = []
        self.setup_ui()
        print(f"CopySetWidget {set_id} initialized")

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
        remove_button.clicked.connect(lambda: self.removed.emit(self))
        
        header_layout.addWidget(header_label)
        header_layout.addStretch(1)
        header_layout.addWidget(remove_button)
        layout.addLayout(header_layout)

        # Folder selections
        self.source_folder_widget = FolderSelectionWidget("Source:")
        self.dest_folder_widget = FolderSelectionWidget("Destination:")
        layout.addWidget(self.source_folder_widget)
        layout.addWidget(self.dest_folder_widget)

        # File selector
        self.file_selector = FileSelector()
        layout.addWidget(self.file_selector)

        # Sync Control
        self.sync_control = SyncControl()
        layout.addWidget(self.sync_control)

        # Connect signals
        print("Connecting signals in CopySetWidget")
        self.source_folder_widget.folder_selected.connect(lambda type, path: self.on_folder_selected("source", path))
        self.dest_folder_widget.folder_selected.connect(lambda type, path: self.on_folder_selected("destination", path))
        self.source_folder_widget.folder_selected.connect(self.file_selector.update_folder)
        self.file_selector.files_selected.connect(self.on_files_selected)
        self.sync_control.sync_started.connect(lambda: self.sync_started.emit(self))
        self.sync_control.sync_stopped.connect(lambda: self.sync_stopped.emit(self))

        self.setStyleSheet(Theme.COPY_SET_STYLE)

    def on_folder_selected(self, folder_type, path):
        print(f"CopySet {self.set_id} folder selected: {folder_type} = {path}")
        self.folders_selected.emit(self, folder_type, path)
        if folder_type == "source":
            self.file_selector.update_folder("source", path)

    def on_files_selected(self, files):
        print(f"CopySet {self.set_id} files selected: {files}")
        self.selected_files = files
        self.files_selected.emit(self.set_id, files)  # Emit set_id and files directly

class CopySetManager(QWidget):
    set_added = pyqtSignal()  # Changed to just emit signal
    set_removed = pyqtSignal(object)
    folders_updated = pyqtSignal(object, str, str)
    files_updated = pyqtSignal(int, list)  # set_id, files

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
        add_button.setStyleSheet(Theme.ADD_BUTTON_STYLE)
        main_layout.addWidget(add_button)

    def add_copy_set(self):
        self.set_added.emit()  # Just emit signal, let MainWindow handle creation

    def on_copy_set_removed(self, copy_set):
        if copy_set in self.copy_sets:
            self.copy_sets.remove(copy_set)
            copy_set.setParent(None)
            self.update_layout()
            self.set_removed.emit(copy_set)

    def update_layout(self):
        # Clear existing widgets from grid
        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0)
            if item.widget():
                item.widget().setParent(None)

        # Re-add widgets in grid layout
        row = 0
        col = 0
        for copy_set in self.copy_sets:
            self.grid_layout.addWidget(copy_set, row, col)
            col += 1
            if col >= 2:  # 2 columns
                col = 0
                row += 1

    def add_copy_set_widget(self, widget):
        self.copy_sets.append(widget)
        self.update_layout()