import os
import json
import time
from PyQt6.QtCore import QObject, pyqtSignal, QTimer
from .file_copier import FileCopier
from ui.ui_file_watcher import FileWatcher
from core.file_operations import FileOperations

class CopySet:
    def __init__(self, set_id, source_folder='', destination_folder=''):
        self.set_id = set_id
        self.source_folder = source_folder
        self.destination_folder = destination_folder
        self.selected_files = set()  # Track selected files
        self.live_sync = False  # New flag for live sync
        self.file_watcher = None
        self.file_copier = None  # FileCopier instance for this copy set
        self.copy_interval = 30  # Default copy interval in minutes
        self.last_update = time.time()  # Last update timestamp
        self.widget = None  # Reference to the UI widget

    def cleanup(self):
        if self.file_watcher:
            self.file_watcher.stop()
            self.file_watcher = None
        if self.file_copier:
            self.file_copier.stop_sync()
            self.file_copier = None

class AppLogic(QObject):
    status_updated = pyqtSignal(str)
    countdown_updated = pyqtSignal(float)

    def __init__(self):
        super().__init__()
        self.copy_sets = {}
        self.countdown_timer = None
        self.last_sync_time = time.time()
        self.sync_interval = 60  # Default 1 minute
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
        copy_set.live_sync = False  # Ensure live sync starts disabled
        copy_set.file_watcher = None  # Initialize file watcher as None
        self.status_updated.emit(f"Copy Set {copy_set.set_id} added")

    def update_copy_set(self, copy_set, source, destination):
        """Update source and destination folders for a copy set"""
        print(f"Updating folders for Copy Set {copy_set.set_id}")
        print(f"Source: {source}")
        print(f"Destination: {destination}")
        
        if copy_set.set_id in self.copy_sets:
            copy_set.source_folder = source
            copy_set.destination_folder = destination
            
            # If we have selected files, update the file copier config
            if copy_set.selected_files:
                config = {
                    'source_folder': source,
                    'destination_folder': destination,
                    'selected_files': list(copy_set.selected_files),
                    'copy_interval': copy_set.copy_interval,
                    'last_update': time.time()
                }
                
                # Create new file copier or update existing one
                if copy_set.file_copier:
                    copy_set.file_copier.config.update(config)
                else:
                    copy_set.file_copier = FileCopier(config)
                    copy_set.file_copier.copy_completed.connect(lambda msg: self.on_copy_completed(msg))
                    copy_set.file_copier.sync_started.connect(lambda: self.on_sync_started())
                
                print(f"Updated file copier config: {config}")
            
            self.status_updated.emit(f"Updated folders for Copy Set {copy_set.set_id}")

    def update_copy_set_files(self, set_id, selected_files):
        """Update selected files for a copy set and configure file copier"""
        print(f"Updating files for Copy Set {set_id}")
        print(f"Selected files: {selected_files}")
        
        if set_id in self.copy_sets:
            copy_set = self.copy_sets[set_id]
            copy_set.selected_files = set(selected_files)  # Update the CopySet object
            
            # Configure file copier for this copy set
            config = {
                'source_folder': copy_set.source_folder,
                'destination_folder': copy_set.destination_folder,
                'selected_files': list(selected_files),  # Convert set to list
                'copy_interval': copy_set.copy_interval,
                'last_update': time.time()
            }
            
            # Create new file copier instance for this copy set
            copy_set.file_copier = FileCopier(config)
            copy_set.file_copier.copy_completed.connect(lambda msg: self.on_copy_completed(msg))
            copy_set.file_copier.sync_started.connect(lambda: self.on_sync_started())
            
            print(f"Configured file copier for Copy Set {set_id}")
            print(f"Config: {config}")
            self.status_updated.emit(f"Updated selected files for Copy Set {set_id}")

    def remove_copy_set(self, copy_set):
        if copy_set.set_id in self.copy_sets:
            del self.copy_sets[copy_set.set_id]
            self.status_updated.emit(f"Copy Set {copy_set.set_id} removed")

    def set_copy_interval(self, minutes):
        """Set the copy interval for all copy sets"""
        for copy_set in self.copy_sets.values():
            copy_set.copy_interval = minutes
            copy_set.last_update = time.time()
            
            # Update file copier if it exists
            if copy_set.file_copier:
                copy_set.file_copier.config['copy_interval'] = minutes
        
        self.status_updated.emit(f"Copy interval set to {minutes} minutes")

    def on_copy_completed(self, message):
        self.status_updated.emit(message)

    def on_sync_started(self):
        self.status_updated.emit("Starting synchronization...")

    def start_file_watcher(self, copy_set):
        """Start the file watcher for a copy set"""
        # Only stop existing watcher if it's actually running
        if copy_set.file_watcher and copy_set.file_watcher.isRunning():
            print(f"Stopping existing file watcher for Copy Set {copy_set.set_id}")
            copy_set.file_watcher.stop()
            copy_set.file_watcher = None
            
        if os.path.exists(copy_set.source_folder):
            print(f"Starting new file watcher for Copy Set {copy_set.set_id}")
            copy_set.file_watcher = FileWatcher(copy_set.source_folder)
            copy_set.file_watcher.file_changed.connect(
                lambda event_type, src_path, dest_path: 
                self.on_file_changed(copy_set, event_type, src_path, dest_path)
                if copy_set.live_sync else None  # Only process if live sync is enabled
            )
            copy_set.file_watcher.start()
            self.status_updated.emit(f"File watcher started for Copy Set {copy_set.set_id} source folder.")
        else:
            self.status_updated.emit(f"Source folder for Copy Set {copy_set.set_id} does not exist. Please select a valid folder.")

    def start_file_copier(self, copy_set):
        if copy_set.file_copier:
            copy_set.file_copier.stop_sync()
        if copy_set.source_folder and copy_set.destination_folder:
            config = {
                'source_folder': copy_set.source_folder,
                'destination_folder': copy_set.destination_folder,
                'copy_interval': copy_set.copy_interval,
                'selected_files': list(copy_set.selected_files) if copy_set.selected_files else None
            }
            copy_set.file_copier = FileCopier(config)
            copy_set.file_copier.copy_completed.connect(lambda msg: self.on_copy_completed(msg))
            copy_set.file_copier.sync_started.connect(lambda: self.on_sync_started())
            # Don't auto-resume, wait for manual start
            self.status_updated.emit(f"File copier configured for Copy Set {copy_set.set_id}. Click 'Start Sync' to begin synchronization.")
        else:
            self.status_updated.emit(f"Both source and destination folders must be specified for Copy Set {copy_set.set_id} to start synchronization.")

    def set_live_sync(self, copy_set_id, enabled):
        """Enable or disable live sync for a specific copy set"""
        if copy_set_id in self.copy_sets:
            copy_set = self.copy_sets[copy_set_id]
            old_state = copy_set.live_sync
            
            # Only process if state is actually changing
            if old_state != enabled:
                print(f"Changing live sync state for Copy Set {copy_set_id} from {old_state} to {enabled}")
                
                # If disabling live sync, stop the file watcher
                if not enabled and copy_set.file_watcher:
                    print(f"Stopping file watcher for Copy Set {copy_set_id}")
                    copy_set.file_watcher.stop()
                    copy_set.file_watcher = None
                    
                copy_set.live_sync = enabled
                
                # Update UI state
                if copy_set.widget:
                    copy_set.widget.set_live_sync_state(enabled)
                
                if enabled:
                    # Start file watcher if not already running
                    self.start_file_watcher(copy_set)
                    self.status_updated.emit(f"Live sync enabled for Copy Set {copy_set_id}")
                else:
                    self.status_updated.emit(f"Live sync disabled for Copy Set {copy_set_id}")
                    # Restart interval sync countdown when disabling live sync
                    self.restart_countdown()
            else:
                print(f"Live sync state unchanged for Copy Set {copy_set_id} (already {enabled})")

    def set_copy_set_widget(self, set_id, widget):
        """Associate a widget with a copy set"""
        if set_id in self.copy_sets:
            self.copy_sets[set_id].widget = widget

    def on_file_changed(self, copy_set, event_type, src_path, dest_path=''):
        # Only process if live sync is enabled
        if not copy_set.live_sync:
            return
            
        source_folder = copy_set.source_folder
        dest_folder = copy_set.destination_folder

        # Check if the changed file is in the selected files (if any are selected)
        relative_path = os.path.relpath(src_path, source_folder)
        if copy_set.selected_files and relative_path not in copy_set.selected_files:
            return

        if event_type == 'created' or event_type == 'modified':
            dest_path = os.path.join(dest_folder, relative_path)
            result = FileOperations.copy_file(src_path, dest_path)
            self.status_updated.emit(f"Live sync: Copied {relative_path}")
        elif event_type == 'deleted':
            dest_path = os.path.join(dest_folder, relative_path)
            result = FileOperations.delete_file(dest_path)
            self.status_updated.emit(f"Live sync: Deleted {relative_path}")
        elif event_type == 'moved':
            src_relative_path = os.path.relpath(src_path, source_folder)
            dest_relative_path = os.path.relpath(dest_path, source_folder)
            src_dest_path = os.path.join(dest_folder, src_relative_path)
            new_dest_path = os.path.join(dest_folder, dest_relative_path)
            result = FileOperations.move_file(src_dest_path, new_dest_path)
            self.status_updated.emit(f"Live sync: Moved {src_relative_path} to {dest_relative_path}")
        else:
            result = f"Unknown event type: {event_type}"

        copy_set.last_update = time.time()

    def restart_countdown(self):
        if not self.copy_sets:
            self.countdown_updated.emit("No copy sets configured")
            return
            
        # Get the copy interval from the first copy set
        self.countdown_remaining = self.copy_sets[list(self.copy_sets.keys())[0]].copy_interval * 60
        self.countdown_timer = QTimer(self)
        self.countdown_timer.timeout.connect(self.update_countdown)
        self.countdown_timer.start(1000)  # Update every second
        self.update_countdown()

    def update_countdown(self):
        if not self.copy_sets:
            return
            
        minutes = self.countdown_remaining // 60
        seconds = self.countdown_remaining % 60
        time_str = f"Next sync in: {minutes:02d}:{seconds:02d}"
        self.countdown_updated.emit(time_str)
        
        self.countdown_remaining -= 1
        if self.countdown_remaining < 0:
            self.sync_all_copy_sets()
            # Restart countdown after sync
            self.restart_countdown()

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

        self.status_updated.emit("Starting interval synchronization for all copy sets...")
        
        for copy_set in self.copy_sets.values():
            # Skip copy sets that are in live sync mode
            if copy_set.live_sync:
                continue
                
            source_folder = copy_set.source_folder
            dest_folder = copy_set.destination_folder
            
            if copy_set.selected_files:
                for file_path in copy_set.selected_files:
                    src_path = os.path.join(source_folder, file_path)
                    dest_path = os.path.join(dest_folder, file_path)
                    
                    if os.path.exists(src_path):
                        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                        try:
                            FileOperations.copy_file(src_path, dest_path)
                            self.status_updated.emit(f"Interval sync: Copied {file_path}")
                        except Exception as e:
                            self.status_updated.emit(f"Error copying {file_path}: {str(e)}")
                    else:
                        self.status_updated.emit(f"Source file not found: {src_path}")
            
            copy_set.last_update = current_time
            
        self.status_updated.emit("Interval synchronization completed.")
        self.restart_countdown()

    def sync_copy_set(self, set_id):
        """Manually sync a specific copy set"""
        if set_id in self.copy_sets:
            copy_set = self.copy_sets[set_id]
            if copy_set.file_copier:
                print(f"Starting manual sync for Copy Set {set_id}")
                copy_set.file_copier.start_sync()
                self.status_updated.emit(f"Manual sync started for Copy Set {set_id}")
            else:
                print(f"No file copier configured for Copy Set {set_id}")
                self.status_updated.emit(f"Cannot start sync - no file copier configured for Copy Set {set_id}")

    def stop_sync(self, set_id):
        """Stop sync for a specific copy set"""
        if set_id in self.copy_sets:
            copy_set = self.copy_sets[set_id]
            if copy_set.file_copier:
                print(f"Stopping sync for Copy Set {set_id}")
                copy_set.file_copier.stop_sync()
                self.status_updated.emit(f"Sync stopped for Copy Set {set_id}")
            else:
                print(f"No file copier configured for Copy Set {set_id}")

    def cleanup(self):
        for copy_set in self.copy_sets.values():
            if copy_set.file_copier:
                copy_set.file_copier.stop_sync()
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