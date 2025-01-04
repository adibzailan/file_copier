import os
import shutil
import time
from PyQt6.QtCore import QObject, pyqtSignal

class FileCopier(QObject):
    copy_completed = pyqtSignal(str)  # Signal emitted when copy is complete
    sync_started = pyqtSignal()  # Signal emitted when sync starts
    
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.running = False
        print(f"FileCopier initialized with config: {config}")
    
    def start_sync(self):
        """Start synchronization of files"""
        if not self.running:
            self.running = True
            self.sync_started.emit()
            self._copy_files()
    
    def stop_sync(self):
        """Stop synchronization"""
        self.running = False
    
    def _copy_files(self):
        """Copy selected files from source to destination"""
        if not self.config.get('selected_files'):
            self.copy_completed.emit("No files selected for copying")
            return
            
        source = self.config.get('source_folder', '')
        dest = self.config.get('destination_folder', '')
        
        if not source or not dest:
            self.copy_completed.emit("Source or destination folder not set")
            return
            
        if not os.path.exists(source):
            self.copy_completed.emit(f"Source folder does not exist: {source}")
            return
            
        if not os.path.exists(dest):
            try:
                os.makedirs(dest)
            except Exception as e:
                self.copy_completed.emit(f"Failed to create destination folder: {str(e)}")
                return
        
        copied_files = []
        failed_files = []
        
        for file in self.config['selected_files']:
            if not self.running:
                break
                
            src_path = os.path.join(source, file)
            dst_path = os.path.join(dest, file)
            
            try:
                if os.path.exists(src_path):
                    # Create destination directory if it doesn't exist
                    os.makedirs(os.path.dirname(dst_path), exist_ok=True)
                    
                    # Copy the file
                    shutil.copy2(src_path, dst_path)
                    copied_files.append(file)
                else:
                    failed_files.append(f"{file} (not found)")
            except Exception as e:
                failed_files.append(f"{file} ({str(e)})")
        
        # Update completion status
        status_msg = []
        if copied_files:
            status_msg.append(f"Copied {len(copied_files)} files successfully")
        if failed_files:
            status_msg.append(f"Failed to copy {len(failed_files)} files")
            for fail in failed_files:
                status_msg.append(f"- {fail}")
                
        self.copy_completed.emit("\n".join(status_msg))
        self.running = False
