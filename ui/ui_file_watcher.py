import time
import os
from PyQt6.QtCore import QThread, pyqtSignal
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class FileWatcher(QThread):
    file_changed = pyqtSignal(str, str, str)  # (event_type, src_path, dest_path)

    def __init__(self, path):
        super().__init__()
        self.path = path
        self.observer = None
        self._stop_requested = False

    def run(self):
        event_handler = FileChangeHandler(self.file_changed)
        self.observer = Observer()
        self.observer.schedule(event_handler, self.path, recursive=True)
        self.observer.start()
        print(f"File watcher started for path: {self.path}")
        
        while not self._stop_requested:
            time.sleep(1)
            
        if self.observer:
            print("Stopping file watcher...")
            self.observer.stop()
            self.observer.join()
            self.observer = None
            print("File watcher stopped")

    def stop(self):
        """Safely stop the file watcher thread"""
        print("Requesting file watcher to stop...")
        self._stop_requested = True
        self.wait()  # Wait for thread to finish

class FileChangeHandler(FileSystemEventHandler):
    def __init__(self, signal):
        self.signal = signal

    def on_created(self, event):
        if not event.is_directory:
            self.signal.emit('created', event.src_path, '')

    def on_deleted(self, event):
        if not event.is_directory:
            self.signal.emit('deleted', event.src_path, '')

    def on_modified(self, event):
        if not event.is_directory:
            self.signal.emit('modified', event.src_path, '')

    def on_moved(self, event):
        if not event.is_directory:
            self.signal.emit('moved', event.src_path, event.dest_path)