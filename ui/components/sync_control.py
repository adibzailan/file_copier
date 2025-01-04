from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLabel
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QFont
from ..theme import Theme

class SyncControl(QWidget):
    sync_started = pyqtSignal()
    sync_stopped = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.is_syncing = False
        self.setup_ui()

    def setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Start/Stop Sync button
        self.sync_button = QPushButton("Start Sync")
        self.sync_button.clicked.connect(self.toggle_sync)
        self.sync_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
        """)
        layout.addWidget(self.sync_button)

    def toggle_sync(self):
        self.is_syncing = not self.is_syncing
        if self.is_syncing:
            self.sync_button.setText("Stop Sync")
            self.sync_button.setStyleSheet("""
                QPushButton {
                    background-color: #f44336;
                    color: white;
                    border: none;
                    padding: 8px 16px;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background-color: #e53935;
                }
                QPushButton:pressed {
                    background-color: #d32f2f;
                }
            """)
            self.sync_started.emit()
        else:
            self.sync_button.setText("Start Sync")
            self.sync_button.setStyleSheet("""
                QPushButton {
                    background-color: #4CAF50;
                    color: white;
                    border: none;
                    padding: 8px 16px;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background-color: #45a049;
                }
                QPushButton:pressed {
                    background-color: #3d8b40;
                }
            """)
            self.sync_stopped.emit()
