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

    def run(self):
        event_handler = FileChangeHandler(self.file_changed)
        self.observer = Observer()
        self.observer.schedule(event_handler, self.path, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(1)
        except:
            self.observer.stop()
        self.observer.join()

    def stop(self):
        if self.observer:
            self.observer.stop()
            self.observer.join()

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