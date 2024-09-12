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

    def run(self):
        while self.running:
            if not self.paused:
                self.sync_started.emit()
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

        # Delete all contents in the destination folder
        self.delete_folder_contents(destination_folder)

        # Copy all files from source to destination
        for root, dirs, files in os.walk(source_folder):
            for file in files:
                src_path = os.path.join(root, file)
                rel_path = os.path.relpath(src_path, source_folder)
                dest_path = os.path.join(destination_folder, rel_path)
                self.copy_file(src_path, dest_path)

        self.copy_completed.emit("Full synchronization completed.")

    def delete_folder_contents(self, folder):
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                    self.copy_completed.emit(f"Deleted file: {filename}")
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
                    self.copy_completed.emit(f"Deleted folder: {filename}")
            except Exception as e:
                self.copy_completed.emit(f"Failed to delete {filename}: {str(e)}")

    def copy_file(self, src_path, dest_path):
        try:
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            shutil.copy2(src_path, dest_path)
            self.copy_completed.emit(f"Copied {os.path.basename(src_path)}")
        except Exception as e:
            self.copy_completed.emit(f"Error copying {os.path.basename(src_path)}: {str(e)}")

    def stop(self):
        self.running = False

    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False