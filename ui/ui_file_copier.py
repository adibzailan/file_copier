import os
import shutil
import time
from PyQt6.QtCore import QThread, pyqtSignal

class FileCopier(QThread):
    copy_completed = pyqtSignal(str)

    def __init__(self, config):
        super().__init__()
        self.config = config
        self.running = True
        self.paused = True  # Add a paused state

    def run(self):
        while self.running:
            if not self.paused:
                self.full_sync()
                time.sleep(self.config.get('copy_interval', 30) * 60)  # Convert minutes to seconds
            else:
                time.sleep(1)  # Check every second if we're still paused

    def full_sync(self):
        source_folder = self.config.get('source_folder')
        destination_folder = self.config.get('destination_folder')

        if not source_folder or not destination_folder:
            self.copy_completed.emit("Both source and destination folders must be specified.")
            return

        self.copy_completed.emit("Starting full synchronization...")

        for root, dirs, files in os.walk(source_folder):
            for file in files:
                src_path = os.path.join(root, file)
                rel_path = os.path.relpath(src_path, source_folder)
                dest_path = os.path.join(destination_folder, rel_path)
                
                if not os.path.exists(dest_path) or os.path.getmtime(src_path) > os.path.getmtime(dest_path):
                    self.copy_file(src_path, dest_path)

        # Remove files from destination that don't exist in source
        for root, dirs, files in os.walk(destination_folder):
            for file in files:
                dest_path = os.path.join(root, file)
                rel_path = os.path.relpath(dest_path, destination_folder)
                src_path = os.path.join(source_folder, rel_path)
                
                if not os.path.exists(src_path):
                    self.delete_file(dest_path)

        self.copy_completed.emit("Full synchronization completed.")

    def copy_file(self, src_path, dest_path):
        try:
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            shutil.copy2(src_path, dest_path)
            self.copy_completed.emit(f"Copied {os.path.basename(src_path)}")
        except Exception as e:
            self.copy_completed.emit(f"Error copying {os.path.basename(src_path)}: {str(e)}")

    def delete_file(self, dest_path):
        try:
            if os.path.exists(dest_path):
                os.remove(dest_path)
                self.copy_completed.emit(f"Deleted {os.path.basename(dest_path)}")
        except Exception as e:
            self.copy_completed.emit(f"Error deleting {os.path.basename(dest_path)}: {str(e)}")

    def stop(self):
        self.running = False

    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False