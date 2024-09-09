import time
from PyQt6.QtCore import QThread, pyqtSignal
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class FileWatcher(QThread):
    file_changed = pyqtSignal(str)

    def __init__(self, path, files):
        super().__init__()
        self.path = path
        self.files = files
        self.observer = None

    def run(self):
        event_handler = FileChangeHandler(self.files, self.file_changed)
        self.observer = Observer()
        self.observer.schedule(event_handler, self.path, recursive=False)
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
    def __init__(self, files, signal):
        self.files = files
        self.signal = signal

    def on_modified(self, event):
        if not event.is_directory and event.src_path.split(os.path.sep)[-1] in self.files:
            self.signal.emit(event.src_path)