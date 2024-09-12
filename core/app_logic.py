import os
import json
import time
from PyQt6.QtCore import QObject, pyqtSignal, QTimer

from ui.ui_file_watcher import FileWatcher
from ui.ui_file_copier import FileCopier
from core.file_operations import FileOperations

class CopySet:
    def __init__(self, set_id, source_folder='', destination_folder=''):
        self.set_id = set_id
        self.source_folder = source_folder
        self.destination_folder = destination_folder
        self.file_watcher = None
        self.file_copier = None

class AppLogic(QObject):
    status_updated = pyqtSignal(str)
    countdown_updated = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.config = {
            'copy_interval': 30,
            'copy_sets': []
        }
        self.copy_sets = {}
        self.countdown_timer = QTimer(self)
        self.countdown_timer.timeout.connect(self.update_countdown)
        self.countdown_remaining = 0
        self.last_sync_time = 0
        self.sync_cooldown = 5  # 5 seconds cooldown between syncs

    def load_config(self):
        try:
            with open('config.json', 'r') as config_file:
                self.config = json.load(config_file)
                for set_data in self.config['copy_sets']:
                    copy_set = CopySet(set_data['set_id'], set_data['source_folder'], set_data['destination_folder'])
                    self.copy_sets[copy_set.set_id] = copy_set
                    self.start_file_watcher(copy_set)
                    self.start_file_copier(copy_set)
            self.restart_countdown()
        except FileNotFoundError:
            pass

    def save_config(self):
        self.config['copy_sets'] = [
            {'set_id': cs.set_id, 'source_folder': cs.source_folder, 'destination_folder': cs.destination_folder}
            for cs in self.copy_sets.values()
        ]
        with open('config.json', 'w') as config_file:
            json.dump(self.config, config_file)

    def add_copy_set(self, copy_set_widget):
        copy_set = CopySet(copy_set_widget.set_id)
        self.copy_sets[copy_set.set_id] = copy_set
        self.save_config()

    def remove_copy_set(self, copy_set_widget):
        copy_set = self.copy_sets.pop(copy_set_widget.set_id, None)
        if copy_set:
            if copy_set.file_watcher:
                copy_set.file_watcher.stop()
            if copy_set.file_copier:
                copy_set.file_copier.stop()
        self.save_config()

    def update_copy_set(self, copy_set_widget, source_folder, destination_folder):
        copy_set = self.copy_sets.get(copy_set_widget.set_id)
        if copy_set:
            copy_set.source_folder = source_folder
            copy_set.destination_folder = destination_folder
            self.start_file_watcher(copy_set)
            self.start_file_copier(copy_set)
        self.save_config()

    def set_copy_interval(self, interval):
        self.config['copy_interval'] = interval
        for copy_set in self.copy_sets.values():
            if copy_set.file_copier:
                copy_set.file_copier.config['copy_interval'] = interval
        self.save_config()
        self.restart_countdown()

    def start_file_watcher(self, copy_set):
        if copy_set.file_watcher:
            copy_set.file_watcher.stop()
        if os.path.exists(copy_set.source_folder):
            copy_set.file_watcher = FileWatcher(copy_set.source_folder)
            copy_set.file_watcher.file_changed.connect(lambda *args: self.on_file_changed(copy_set, *args))
            copy_set.file_watcher.start()
            self.status_updated.emit(f"File watcher started for Copy Set {copy_set.set_id} source folder.")
        else:
            self.status_updated.emit(f"Source folder for Copy Set {copy_set.set_id} does not exist. Please select a valid folder.")

    def start_file_copier(self, copy_set):
        if copy_set.file_copier:
            copy_set.file_copier.stop()
        if copy_set.source_folder and copy_set.destination_folder:
            config = {
                'source_folder': copy_set.source_folder,
                'destination_folder': copy_set.destination_folder,
                'copy_interval': self.config['copy_interval']
            }
            copy_set.file_copier = FileCopier(config)
            copy_set.file_copier.copy_completed.connect(lambda msg: self.on_copy_completed(copy_set, msg))
            copy_set.file_copier.sync_started.connect(lambda: self.on_sync_started(copy_set))
            copy_set.file_copier.resume()
            self.status_updated.emit(f"File copier started for Copy Set {copy_set.set_id}. Initial full synchronization will begin shortly.")
        else:
            self.status_updated.emit(f"Both source and destination folders must be specified for Copy Set {copy_set.set_id} to start synchronization.")

    def on_file_changed(self, copy_set, event_type, src_path, dest_path=''):
        source_folder = copy_set.source_folder
        dest_folder = copy_set.destination_folder

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

        self.status_updated.emit(f"Copy Set {copy_set.set_id}: {result}")

    def on_copy_completed(self, copy_set, msg):
        self.status_updated.emit(f"Copy Set {copy_set.set_id}: {msg}")

    def on_sync_started(self, copy_set):
        self.status_updated.emit(f"Copy Set {copy_set.set_id}: Starting synchronization...")

    def restart_countdown(self):
        self.countdown_remaining = self.config['copy_interval'] * 60
        self.countdown_timer.start(1000)  # Update every second
        self.update_countdown()

    def update_countdown(self):
        self.countdown_updated.emit(self.countdown_remaining)
        self.countdown_remaining -= 1
        if self.countdown_remaining < 0:
            self.sync_all_copy_sets()

    def sync_all_copy_sets(self):
        current_time = time.time()
        if current_time - self.last_sync_time < self.sync_cooldown:
            self.status_updated.emit("Sync cooldown in effect. Skipping this sync cycle.")
            self.restart_countdown()
            return

        self.status_updated.emit("Starting synchronization for all copy sets...")
        for copy_set in self.copy_sets.values():
            if copy_set.file_copier:
                copy_set.file_copier.full_sync()
        self.status_updated.emit("Synchronization completed for all copy sets.")
        self.last_sync_time = current_time
        self.restart_countdown()

    def cleanup(self):
        for copy_set in self.copy_sets.values():
            if copy_set.file_copier:
                copy_set.file_copier.stop()
            if copy_set.file_watcher:
                copy_set.file_watcher.stop()
        
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