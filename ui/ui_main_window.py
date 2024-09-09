import os
import json
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from .ui_file_watcher import FileWatcher
from .ui_file_copier import FileCopier
from .components.folder_selection import FolderSelectionWidget
from .components.interval_settings import IntervalSettingsWidget
from .components.status_list import StatusListWidget
from .components.footer import FooterWidget
from core.file_operations import FileOperations
from core.rename_logic import RenameLogic

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FILE COPIER")
        self.setGeometry(100, 100, 800, 600)
        self.file_copier = None
        self.file_watcher = None
        self.setup_ui()
        self.load_config()

    def setup_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout()
        main_widget.setLayout(layout)

        # Title
        title_label = QLabel("FILE COPIER")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        layout.addWidget(title_label)

        # Source folder selection
        self.source_folder = FolderSelectionWidget("SOURCE FOLDER:")
        self.source_folder.folder_selected.connect(self.on_source_folder_selected)
        layout.addWidget(self.source_folder)

        # Destination folder selection
        self.dest_folder = FolderSelectionWidget("DESTINATION FOLDER:")
        self.dest_folder.folder_selected.connect(self.on_dest_folder_selected)
        layout.addWidget(self.dest_folder)

        # Copy interval settings
        self.interval_settings = IntervalSettingsWidget()
        self.interval_settings.interval_changed.connect(self.on_interval_changed)
        layout.addWidget(self.interval_settings)

        # Status messages
        self.status_list = StatusListWidget()
        layout.addWidget(self.status_list)

        # Footer
        self.footer = FooterWidget()
        layout.addWidget(self.footer)

        self.apply_styling()

    def apply_styling(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1E1E1E;
                color: #FFFFFF;
            }
            QLabel {
                color: #FFFFFF;
            }
            QPushButton {
                background-color: #FF4D00;
                color: #FFFFFF;
                border: none;
                padding: 5px 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #FF6E00;
            }
            QListWidget {
                background-color: #2D2D2D;
                color: #FFFFFF;
                border: 1px solid #FF4D00;
            }
            QSlider::groove:horizontal {
                border: 1px solid #999999;
                height: 8px;
                background: #2D2D2D;
                margin: 2px 0;
            }
            QSlider::handle:horizontal {
                background: #FF4D00;
                border: 1px solid #FF4D00;
                width: 18px;
                margin: -2px 0;
                border-radius: 3px;
            }
            QLineEdit {
                background-color: #2D2D2D;
                color: #FFFFFF;
                border: 1px solid #FF4D00;
                padding: 2px;
            }
        """)

    def load_config(self):
        try:
            with open('config.json', 'r') as config_file:
                self.config = json.load(config_file)
                self.source_folder.set_path(self.config['source_folder'])
                self.dest_folder.set_path(self.config['destination_folder'])
                interval = self.config.get('copy_interval', 30)
                self.interval_settings.set_interval(interval)
                if self.config['source_folder'] and self.config['destination_folder']:
                    self.start_file_watcher()
                    self.start_file_copier()
        except FileNotFoundError:
            self.config = {
                'source_folder': '',
                'destination_folder': '',
                'copy_interval': 30
            }

    def save_config(self):
        self.config['copy_interval'] = self.interval_settings.get_interval()
        with open('config.json', 'w') as config_file:
            json.dump(self.config, config_file)

    def on_source_folder_selected(self, label, folder):
        self.config['source_folder'] = folder
        self.save_config()
        self.start_file_watcher()
        self.start_file_copier()

    def on_dest_folder_selected(self, label, folder):
        self.config['destination_folder'] = folder
        self.save_config()
        if self.config['source_folder']:
            self.start_file_copier()

    def on_interval_changed(self, value):
        self.config['copy_interval'] = value
        self.save_config()
        if self.file_copier:
            self.file_copier.set_interval(value)

    def start_file_copier(self):
        if self.file_copier:
            self.file_copier.stop()
        self.file_copier = FileCopier(self.config)
        self.file_copier.copy_completed.connect(self.update_status)
        self.file_copier.start()
        self.initial_full_copy()

    def start_file_watcher(self):
        if self.file_watcher:
            self.file_watcher.stop()
        if os.path.exists(self.config['source_folder']):
            self.file_watcher = FileWatcher(self.config['source_folder'])
            self.file_watcher.file_changed.connect(self.on_file_changed)
            self.file_watcher.start()
            self.update_status("File watcher started for the source folder.")
        else:
            self.update_status("Source folder does not exist. Please select a valid folder.")

    def initial_full_copy(self):
        source_folder = self.config['source_folder']
        dest_folder = self.config['destination_folder']
        if not (source_folder and dest_folder):
            return

        result = FileOperations.initial_full_copy(source_folder, dest_folder)
        self.update_status(result)

    def on_file_changed(self, event_type, src_path, dest_path=''):
        source_folder = self.config['source_folder']
        dest_folder = self.config['destination_folder']

        if event_type == 'created' or event_type == 'modified':
            relative_path = os.path.relpath(src_path, source_folder)
            dest_path = os.path.join(dest_folder, relative_path)
            result = FileOperations.copy_file(src_path, dest_path)
        elif event_type == 'deleted':
            relative_path = os.path.relpath(src_path, source_folder)
            dest_path = os.path.join(dest_folder, relative_path)
            result = FileOperations.delete_file(dest_path)
        elif event_type == 'moved':
            src_relative_path = os.path.relpath(src_path, source_folder)
            dest_relative_path = os.path.relpath(dest_path, source_folder)
            src_dest_path = os.path.join(dest_folder, src_relative_path)
            new_dest_path = os.path.join(dest_folder, dest_relative_path)
            result = FileOperations.move_file(src_dest_path, new_dest_path)
        else:
            result = f"Unknown event type: {event_type}"

        self.update_status(result)

    def update_status(self, message):
        self.status_list.add_status(message)