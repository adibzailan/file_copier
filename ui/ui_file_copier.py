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