import os
import shutil
import time
from PyQt6.QtCore import QThread, pyqtSignal

class FileCopier(QThread):
    copy_completed = pyqtSignal(str)

    def __init__(self, config):
        super().__init__()
        self.config = config

    def run(self):
        while True:
            self.copy_files()
            time.sleep(self.config.get('copy_interval', 30) * 60)  # Convert minutes to seconds

    def copy_files(self):
        source_folder = self.config['source_folder']
        destination_folder = self.config['destination_folder']
        files_to_copy = self.config['files_to_copy']

        for file in files_to_copy:
            self.copy_file(file)

    def copy_file(self, file):
        source_folder = self.config['source_folder']
        destination_folder = self.config['destination_folder']
        
        source_path = os.path.join(source_folder, file)
        destination_path = os.path.join(destination_folder, file)
        
        try:
            if os.path.exists(source_path):
                os.makedirs(os.path.dirname(destination_path), exist_ok=True)
                shutil.copy2(source_path, destination_path)
                self.copy_completed.emit(f"Copied {file} to {destination_folder}")
            else:
                self.copy_completed.emit(f"Source file {file} not found")
        except Exception as e:
            self.copy_completed.emit(f"Error copying {file}: {str(e)}")

    def delete_file(self, file):
        destination_folder = self.config['destination_folder']
        destination_path = os.path.join(destination_folder, file)
        
        try:
            if os.path.exists(destination_path):
                os.remove(destination_path)
                self.copy_completed.emit(f"Deleted {file} from {destination_folder}")
            else:
                self.copy_completed.emit(f"File {file} not found in destination folder")
        except Exception as e:
            self.copy_completed.emit(f"Error deleting {file}: {str(e)}")

    def move_file(self, src_file, dest_file):
        destination_folder = self.config['destination_folder']
        src_path = os.path.join(destination_folder, src_file)
        dest_path = os.path.join(destination_folder, dest_file)
        
        try:
            if os.path.exists(src_path):
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                shutil.move(src_path, dest_path)
                self.copy_completed.emit(f"Moved {src_file} to {dest_file} in {destination_folder}")
            else:
                self.copy_completed.emit(f"Source file {src_file} not found in destination folder")
        except Exception as e:
            self.copy_completed.emit(f"Error moving {src_file}: {str(e)}")