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
        self.selected_files = set()  # Track selected files
        self.file_watcher = None
        self.file_copier = None
        self.copy_interval = 30  # Default copy interval in minutes
        self.last_update = time.time()  # Last update timestamp

class AppLogic(QObject):
    status_updated = pyqtSignal(str)
    countdown_updated = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.copy_sets = {}
        self.file_copier = None
        print("AppLogic initialized")

    def load_config(self):
        try:
            with open('config.json', 'r') as config_file:
                config_data = json.load(config_file)
                for set_data in config_data['copy_sets']:
                    copy_set = CopySet(set_data['set_id'], set_data['source_folder'], set_data['destination_folder'])
                    if 'selected_files' in set_data:  # Load selected files from config
                        copy_set.selected_files = set(set_data['selected_files'])
                    self.copy_sets[copy_set.set_id] = copy_set
                    self.start_file_watcher(copy_set)
                    self.start_file_copier(copy_set)
            self.restart_countdown()
        except FileNotFoundError:
            pass

    def save_config(self):
        config_data = {
            'copy_sets': [
                {
                    'set_id': cs.set_id,
                    'source_folder': cs.source_folder,
                    'destination_folder': cs.destination_folder,
                    'selected_files': list(cs.selected_files)  # Save selected files to config
                }
                for cs in self.copy_sets.values()
            ]
        }
        with open('config.json', 'w') as config_file:
            json.dump(config_data, config_file, indent=4)

    def add_copy_set(self, copy_set):
        print(f"Adding copy set {copy_set.set_id}")
        self.copy_sets[copy_set.set_id] = copy_set
        
        # Initialize file copier if not already done
        if not self.file_copier:
            config = {
                'source_folder': copy_set.source_folder,
                'destination_folder': copy_set.destination_folder,
                'selected_files': list(copy_set.selected_files),
                'copy_interval': 30,
                'last_update': time.time()
            }
            self.file_copier = FileCopier(config)
            self.file_copier.copy_completed.connect(self.on_copy_completed)
            self.file_copier.sync_started.connect(self.on_sync_started)
            self.file_copier.start()
            print("File copier initialized and started")
        
        self.status_updated.emit(f"Copy Set {copy_set.set_id} added")

    def update_copy_set(self, copy_set, source, destination):
        print(f"Updating folders for Copy Set {copy_set.set_id}")
        print(f"Source: {source}")
        print(f"Destination: {destination}")
        
        if copy_set.set_id in self.copy_sets:
            copy_set = self.copy_sets[copy_set.set_id]
            copy_set.source_folder = source
            copy_set.destination_folder = destination
            
            # Update file copier config
            if self.file_copier:
                config = {
                    'source_folder': source,
                    'destination_folder': destination,
                    'selected_files': list(copy_set.selected_files),
                    'copy_interval': self.file_copier.config.get('copy_interval', 30),
                    'last_update': time.time()
                }
                self.file_copier.config.update(config)
                print(f"Updated file copier config: {self.file_copier.config}")
            
            self.status_updated.emit(f"Updated folders for Copy Set {copy_set.set_id}")

    def update_copy_set_files(self, set_id, selected_files):
        print(f"AppLogic: Updating files for Copy Set {set_id}")
        print(f"Selected files: {selected_files}")
        
        if set_id in self.copy_sets:
            copy_set = self.copy_sets[set_id]
            copy_set.selected_files = set(selected_files)  # Update the CopySet object
            
            # Update file copier config
            if self.file_copier:
                config = {
                    'source_folder': copy_set.source_folder,
                    'destination_folder': copy_set.destination_folder,
                    'selected_files': selected_files,
                    'copy_interval': self.file_copier.config.get('copy_interval', 30),
                    'last_update': time.time()
                }
                self.file_copier.config.update(config)
                print(f"Updated file copier config with files: {selected_files}")
                print(f"Current file copier config: {self.file_copier.config}")
            
            self.status_updated.emit(f"Updated selected files for Copy Set {set_id}")

    def remove_copy_set(self, copy_set):
        if copy_set.set_id in self.copy_sets:
            del self.copy_sets[copy_set.set_id]
            self.status_updated.emit(f"Copy Set {copy_set.set_id} removed")

    def set_copy_interval(self, minutes):
        for copy_set in self.copy_sets.values():
            copy_set.copy_interval = minutes
            copy_set.last_update = time.time()
            
        if self.file_copier:
            self.file_copier.config['copy_interval'] = minutes
        
        self.status_updated.emit(f"Copy interval set to {minutes} minutes")

    def on_copy_completed(self, message):
        self.status_updated.emit(message)

    def on_sync_started(self):
        self.status_updated.emit("Starting synchronization...")

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
                'copy_interval': copy_set.copy_interval,
                'selected_files': list(copy_set.selected_files) if copy_set.selected_files else None
            }
            copy_set.file_copier = FileCopier(config)
            copy_set.file_copier.copy_completed.connect(lambda msg: self.on_copy_completed(copy_set, msg))
            copy_set.file_copier.sync_started.connect(lambda: self.on_sync_started(copy_set))
            # Don't auto-resume, wait for manual start
            self.status_updated.emit(f"File copier configured for Copy Set {copy_set.set_id}. Click 'Start Sync' to begin synchronization.")
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

    def restart_countdown(self):
        self.countdown_remaining = self.copy_sets[list(self.copy_sets.keys())[0]].copy_interval * 60
        self.countdown_timer = QTimer(self)
        self.countdown_timer.timeout.connect(self.update_countdown)
        self.countdown_timer.start(1000)  # Update every second
        self.update_countdown()

    def update_countdown(self):
        self.countdown_updated.emit(str(self.countdown_remaining))
        self.countdown_remaining -= 1
        if self.countdown_remaining < 0:
            self.sync_all_copy_sets()

    def sync_all_copy_sets(self):
        # Check if we have valid source and destination folders
        for copy_set in self.copy_sets.values():
            if not copy_set.source_folder or not copy_set.destination_folder:
                self.status_updated.emit("Error: Both source and destination folders must be set before syncing.")
                return

        current_time = time.time()
        if self.copy_sets and current_time - list(self.copy_sets.values())[0].last_update < 5:
            self.status_updated.emit("Sync cooldown in effect. Skipping this sync cycle.")
            self.restart_countdown()
            return

        self.status_updated.emit("Starting synchronization for all copy sets...")
        if self.file_copier:
            self.file_copier.resume()  # This will trigger an immediate sync
        self.status_updated.emit("Synchronization started.")

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