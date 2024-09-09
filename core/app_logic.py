import os
import json
from PyQt6.QtCore import QObject, pyqtSignal
from ui.ui_file_watcher import FileWatcher
from ui.ui_file_copier import FileCopier
from core.file_operations import FileOperations

class AppLogic(QObject):
    status_updated = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.config = {
            'source_folder': '',
            'destination_folder': '',
            'copy_interval': 30
        }
        self.file_copier = None
        self.file_watcher = None

    def load_config(self):
        try:
            with open('config.json', 'r') as config_file:
                self.config = json.load(config_file)
        except FileNotFoundError:
            pass

    def save_config(self):
        with open('config.json', 'w') as config_file:
            json.dump(self.config, config_file)

    def set_source_folder(self, folder):
        self.config['source_folder'] = folder
        self.save_config()
        self.start_file_watcher()
        self.check_start_file_copier()

    def set_destination_folder(self, folder):
        self.config['destination_folder'] = folder
        self.save_config()
        self.check_start_file_copier()

    def set_copy_interval(self, interval):
        self.config['copy_interval'] = interval
        self.save_config()
        if self.file_copier:
            self.file_copier.config['copy_interval'] = interval

    def check_start_file_copier(self):
        if self.config['source_folder'] and self.config['destination_folder']:
            self.start_file_copier()
        else:
            self.status_updated.emit("Both source and destination folders must be specified to start synchronization.")

    def start_file_copier(self):
        if self.file_copier:
            self.file_copier.stop()
        self.file_copier = FileCopier(self.config)
        self.file_copier.copy_completed.connect(self.status_updated.emit)
        self.file_copier.resume()  # Start the copier
        self.file_copier.start()
        self.status_updated.emit("File copier started. Initial full synchronization will begin shortly.")

    def start_file_watcher(self):
        if self.file_watcher:
            self.file_watcher.stop()
        if os.path.exists(self.config['source_folder']):
            self.file_watcher = FileWatcher(self.config['source_folder'])
            self.file_watcher.file_changed.connect(self.on_file_changed)
            self.file_watcher.start()
            self.status_updated.emit("File watcher started for the source folder.")
        else:
            self.status_updated.emit("Source folder does not exist. Please select a valid folder.")

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

        self.status_updated.emit(result)

    def cleanup(self):
        if self.file_copier:
            self.file_copier.stop()
        if self.file_watcher:
            self.file_watcher.stop()
        
        # Delete the config file
        try:
            os.remove('config.json')
            print("Config file deleted successfully.")
        except FileNotFoundError:
            print("Config file not found.")
        except PermissionError:
            print("Permission denied: Unable to delete config file.")
        except Exception as e:
            print(f"An error occurred while deleting the config file: {str(e)}")