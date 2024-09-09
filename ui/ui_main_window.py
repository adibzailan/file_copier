import os
import json
import shutil
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLabel, QFileDialog, QListWidget, QSlider, QLineEdit)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QIntValidator
from .ui_file_watcher import FileWatcher
from .ui_file_copier import FileCopier

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
        source_layout = QHBoxLayout()
        self.source_label = QLabel("SOURCE FOLDER:")
        self.source_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        self.source_path = QLabel()
        self.source_path.setFont(QFont("Arial", 12))
        self.source_button = QPushButton("SELECT")
        self.source_button.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        self.source_button.clicked.connect(self.select_source_folder)
        source_layout.addWidget(self.source_label)
        source_layout.addWidget(self.source_path)
        source_layout.addWidget(self.source_button)
        layout.addLayout(source_layout)

        # Destination folder selection
        dest_layout = QHBoxLayout()
        self.dest_label = QLabel("DESTINATION FOLDER:")
        self.dest_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        self.dest_path = QLabel()
        self.dest_path.setFont(QFont("Arial", 12))
        self.dest_button = QPushButton("SELECT")
        self.dest_button.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        self.dest_button.clicked.connect(self.select_dest_folder)
        dest_layout.addWidget(self.dest_label)
        dest_layout.addWidget(self.dest_path)
        dest_layout.addWidget(self.dest_button)
        layout.addLayout(dest_layout)

        # Copy interval slider and input
        interval_layout = QHBoxLayout()
        interval_label = QLabel("COPY INTERVAL (MINUTES):")
        interval_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        self.interval_slider = QSlider(Qt.Orientation.Horizontal)
        self.interval_slider.setMinimum(1)
        self.interval_slider.setMaximum(60)
        self.interval_slider.setValue(30)
        self.interval_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.interval_slider.setTickInterval(5)
        self.interval_input = QLineEdit()
        self.interval_input.setFont(QFont("Arial", 12))
        self.interval_input.setValidator(QIntValidator(1, 60))
        self.interval_input.setText("30")
        self.interval_input.setFixedWidth(50)
        self.interval_slider.valueChanged.connect(self.update_interval_input)
        self.interval_input.textChanged.connect(self.update_interval_slider)
        interval_layout.addWidget(interval_label)
        interval_layout.addWidget(self.interval_slider)
        interval_layout.addWidget(self.interval_input)
        layout.addLayout(interval_layout)

        # Status messages
        status_label = QLabel("STATUS:")
        status_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        layout.addWidget(status_label)
        self.status_list = QListWidget()
        self.status_list.setFont(QFont("Arial", 12))
        layout.addWidget(self.status_list)

        # Acknowledgement footer
        footer_label = QLabel('Alpha 1.0.0 | Built in Singapore, <a href="https://www.linkedin.com/in/adibzailan/">AZ</a>')
        footer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        footer_label.setOpenExternalLinks(True)
        layout.addWidget(footer_label)

        # Apply styling
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

    def update_interval_input(self, value):
        self.interval_input.setText(str(value))

    def update_interval_slider(self, text):
        if text and text.isdigit():
            value = int(text)
            if 1 <= value <= 60:
                self.interval_slider.setValue(value)

    def load_config(self):
        try:
            with open('config.json', 'r') as config_file:
                self.config = json.load(config_file)
                self.source_path.setText(self.config['source_folder'])
                self.dest_path.setText(self.config['destination_folder'])
                interval = self.config.get('copy_interval', 30)
                self.interval_slider.setValue(interval)
                self.interval_input.setText(str(interval))
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
        self.config['copy_interval'] = int(self.interval_input.text())
        with open('config.json', 'w') as config_file:
            json.dump(self.config, config_file)

    def select_source_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Source Folder")
        if folder:
            self.config['source_folder'] = folder
            self.source_path.setText(folder)
            self.save_config()
            self.start_file_watcher()
            self.start_file_copier()

    def select_dest_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Destination Folder")
        if folder:
            self.config['destination_folder'] = folder
            self.dest_path.setText(folder)
            self.save_config()
            if self.config['source_folder']:
                self.start_file_copier()

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

        self.update_status("Starting initial full copy...")
        for root, dirs, files in os.walk(source_folder):
            for file in files:
                src_path = os.path.join(root, file)
                rel_path = os.path.relpath(src_path, source_folder)
                dest_path = os.path.join(dest_folder, rel_path)
                self.copy_file(src_path, dest_path)
        self.update_status("Initial full copy completed.")

    def on_file_changed(self, event_type, src_path, dest_path=''):
        source_folder = self.config['source_folder']
        dest_folder = self.config['destination_folder']

        if event_type == 'created' or event_type == 'modified':
            relative_path = os.path.relpath(src_path, source_folder)
            dest_path = os.path.join(dest_folder, relative_path)
            self.copy_file(src_path, dest_path)
        elif event_type == 'deleted':
            relative_path = os.path.relpath(src_path, source_folder)
            dest_path = os.path.join(dest_folder, relative_path)
            self.delete_file(dest_path)
        elif event_type == 'moved':
            src_relative_path = os.path.relpath(src_path, source_folder)
            dest_relative_path = os.path.relpath(dest_path, source_folder)
            src_dest_path = os.path.join(dest_folder, src_relative_path)
            new_dest_path = os.path.join(dest_folder, dest_relative_path)
            self.move_file(src_dest_path, new_dest_path)

    def copy_file(self, src_path, dest_path):
        try:
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            shutil.copy2(src_path, dest_path)
            self.update_status(f"File copied: {os.path.basename(src_path)}")
        except Exception as e:
            self.update_status(f"Error copying file: {str(e)}")

    def delete_file(self, dest_path):
        try:
            if os.path.exists(dest_path):
                os.remove(dest_path)
                self.update_status(f"File deleted: {os.path.basename(dest_path)}")
        except Exception as e:
            self.update_status(f"Error deleting file: {str(e)}")

    def move_file(self, src_path, dest_path):
        try:
            if os.path.exists(src_path):
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                shutil.move(src_path, dest_path)
                self.update_status(f"File moved: {os.path.basename(src_path)} to {os.path.basename(dest_path)}")
        except Exception as e:
            self.update_status(f"Error moving file: {str(e)}")

    def update_status(self, message):
        self.status_list.addItem(message)
        self.status_list.scrollToBottom()