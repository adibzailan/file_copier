import os
import shutil
import time
from PyQt6.QtCore import QThread, pyqtSignal

class FileCopier(QThread):
    copy_completed = pyqtSignal(str)
    sync_started = pyqtSignal()

    def __init__(self, config):
        super().__init__()
        self.config = config
        self.running = True
        self.paused = True
        print(f"FileCopier initialized with config: {self.config}")

    def run(self):
        while self.running:
            if not self.paused:
                print("FileCopier running sync cycle")
                self.sync_started.emit()
                self.full_sync()
                time.sleep(self.config.get('copy_interval', 30) * 60)  # Wait for next interval
            else:
                time.sleep(1)  # Check every second if we're still paused

    def full_sync(self):
        source_folder = self.config.get('source_folder')
        destination_folder = self.config.get('destination_folder')
        selected_files = self.config.get('selected_files', [])

        # Convert paths to Windows format
        if source_folder:
            source_folder = os.path.normpath(source_folder)
        if destination_folder:
            destination_folder = os.path.normpath(destination_folder)

        print(f"Starting sync from {source_folder} to {destination_folder}")
        print(f"Selected files: {selected_files}")

        if not source_folder or not destination_folder:
            self.copy_completed.emit("Both source and destination folders must be specified.")
            return

        if not os.path.exists(source_folder):
            self.copy_completed.emit(f"Source folder does not exist: {source_folder}")
            return

        self.copy_completed.emit("Starting full synchronization...")

        try:
            # Create destination folder if it doesn't exist
            os.makedirs(destination_folder, exist_ok=True)
            print(f"Created/verified destination folder: {destination_folder}")

            # Copy selected files from source to destination
            if selected_files:
                self.copy_completed.emit(f"Copying {len(selected_files)} selected files...")
                for file_path in selected_files:
                    src_path = os.path.join(source_folder, file_path)
                    dest_path = os.path.join(destination_folder, file_path)
                    print(f"Attempting to copy: {src_path} -> {dest_path}")
                    
                    if os.path.exists(src_path):
                        # Create destination directory structure
                        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                        try:
                            shutil.copy2(src_path, dest_path)
                            print(f"Successfully copied: {file_path}")
                            self.copy_completed.emit(f"Copied: {file_path}")
                        except Exception as e:
                            error_msg = f"Error copying {file_path}: {str(e)}"
                            print(error_msg)
                            self.copy_completed.emit(error_msg)
                    else:
                        error_msg = f"Source file not found: {src_path}"
                        print(error_msg)
                        self.copy_completed.emit(error_msg)
            else:
                self.copy_completed.emit("No files selected for copying.")

            self.copy_completed.emit("Full synchronization completed.")
        except Exception as e:
            error_msg = f"Sync error: {str(e)}"
            print(error_msg)
            self.copy_completed.emit(error_msg)

    def pause(self):
        print("Pausing sync")
        self.paused = True

    def resume(self):
        print("FileCopier resuming")
        print(f"Current config: {self.config}")
        self.paused = False
        # Perform immediate sync when started
        self.sync_started.emit()
        self.full_sync()

    def stop(self):
        print("Stopping sync")
        self.running = False
        self.paused = True
        self.wait()