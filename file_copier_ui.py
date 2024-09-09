import sys
import os
import shutil
import json
import time
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFileDialog, QListWidget
from PyQt6.QtCore import Qt, QTimer, QThread, pyqtSignal
from PyQt6.QtGui import QColor, QPalette
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class FileWatcher(QThread):
    file_changed = pyqtSignal(str)

    def __init__(self, path, files):
        super().__init__()
        self.path = path
        self.files = files

    def run(self):
        event_handler = FileChangeHandler(self.files, self.file_changed)
        observer = Observer()
        observer.schedule(event_handler, self.path, recursive=False)
        observer.start()
        try:
            while True:
                time.sleep(1)
        except:
            observer.stop()
        observer.join()

class FileChangeHandler(FileSystemEventHandler):
    def __init__(self, files, signal):
        self.files = files
        self.signal = signal

    def on_modified(self, event):
        if not event.is_directory and event.src_path.split(os.path.sep)[-1] in self.files:
            self.signal.emit(event.src_path)

class FileCopier(QThread):
    copy_completed = pyqtSignal(str)

    def __init__(self, config):
        super().__init__()
        self.config = config

    def run(self):
        while True:
            self.copy_files()
            time.sleep(1800)  # 30 minutes

    def copy_files(self):
        source_folder = self.config['source_folder']
        destination_folder = self.config['destination_folder']
        files_to_copy = self.config['files_to_copy']

        for file in files_to_copy:
            source_path = os.path.join(source_folder, file)
            destination_path = os.path.join(destination_folder, file)
            
            try:
                if os.path.exists(source_path):
                    shutil.copy2(source_path, destination_path)
                    self.copy_completed.emit(f"Copied {file} to {destination_folder}")
                else:
                    self.copy_completed.emit(f"Source file {file} not found")
            except Exception as e:
                self.copy_completed.emit(f"Error copying {file}: {str(e)}")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("File Copier")
        self.setGeometry(100, 100, 600, 400)
        self.setup_ui()
        self.load_config()
        self.start_file_copier()
        self.start_file_watcher()

    def setup_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout()
        main_widget.setLayout(layout)

        # Set the color scheme
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(255, 255, 255))
        palette.setColor(QPalette.ColorRole.WindowText, QColor(0, 0, 0))
        palette.setColor(QPalette.ColorRole.Button, QColor(240, 240, 240))
        palette.setColor(QPalette.ColorRole.ButtonText, QColor(0, 0, 0))
        palette.setColor(QPalette.ColorRole.Highlight, QColor(248, 132, 35))
        self.setPalette(palette)

        # Source folder selection
        source_layout = QHBoxLayout()
        self.source_label = QLabel("Source Folder:")
        self.source_path = QLabel()
        self.source_button = QPushButton("Select")
        self.source_button.clicked.connect(self.select_source_folder)
        source_layout.addWidget(self.source_label)
        source_layout.addWidget(self.source_path)
        source_layout.addWidget(self.source_button)
        layout.addLayout(source_layout)

        # Destination folder selection
        dest_layout = QHBoxLayout()
        self.dest_label = QLabel("Destination Folder:")
        self.dest_path = QLabel()
        self.dest_button = QPushButton("Select")
        self.dest_button.clicked.connect(self.select_dest_folder)
        dest_layout.addWidget(self.dest_label)
        dest_layout.addWidget(self.dest_path)
        dest_layout.addWidget(self.dest_button)
        layout.addLayout(dest_layout)

        # File list
        self.file_list = QListWidget()
        layout.addWidget(self.file_list)

        # Status messages
        self.status_label = QLabel("Status:")
        self.status_list = QListWidget()
        layout.addWidget(self.status_label)
        layout.addWidget(self.status_list)

        # Apply some styling
        self.setStyleSheet("""
            QMainWindow {
                background-color: white;
            }
            QLabel {
                font-size: 14px;
                color: black;
            }
            QPushButton {
                background-color: #f0f0f0;
                border: 1px solid #d0d0d0;
                padding: 5px 10px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
            QListWidget {
                border: 1px solid #d0d0d0;
                background-color: white;
            }
        """)

    def load_config(self):
        try:
            with open('config.json', 'r') as config_file:
                self.config = json.load(config_file)
                self.source_path.setText(self.config['source_folder'])
                self.dest_path.setText(self.config['destination_folder'])
                self.file_list.addItems(self.config['files_to_copy'])
        except FileNotFoundError:
            self.config = {
                'source_folder': '',
                'destination_folder': '',
                'files_to_copy': []
            }

    def save_config(self):
        with open('config.json', 'w') as config_file:
            json.dump(self.config, config_file)

    def select_source_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Source Folder")
        if folder:
            self.config['source_folder'] = folder
            self.source_path.setText(folder)
            self.save_config()

    def select_dest_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Destination Folder")
        if folder:
            self.config['destination_folder'] = folder
            self.dest_path.setText(folder)
            self.save_config()

    def start_file_copier(self):
        self.file_copier = FileCopier(self.config)
        self.file_copier.copy_completed.connect(self.update_status)
        self.file_copier.start()

    def start_file_watcher(self):
        self.file_watcher = FileWatcher(self.config['source_folder'], self.config['files_to_copy'])
        self.file_watcher.file_changed.connect(self.on_file_changed)
        self.file_watcher.start()

    def on_file_changed(self, file_path):
        self.file_copier.copy_files()

    def update_status(self, message):
        self.status_list.addItem(message)
        self.status_list.scrollToBottom()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())