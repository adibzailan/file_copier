from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QCloseEvent
from .components.folder_selection import FolderSelectionWidget
from .components.interval_settings import IntervalSettingsWidget
from .components.status_list import StatusListWidget
from .components.footer import FooterWidget
from core.app_logic import AppLogic

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FILE COPIER")
        self.setGeometry(100, 100, 800, 600)
        self.app_logic = AppLogic()
        self.setup_ui()
        self.connect_signals()
        self.app_logic.load_config()

    def setup_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout()
        main_widget.setLayout(layout)

        # Title
        title_label = QLabel("FILE COPIER")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        layout.addWidget(title_label)

        # Source folder selection
        self.source_folder = FolderSelectionWidget("SOURCE FOLDER:")
        layout.addWidget(self.source_folder)

        # Destination folder selection
        self.dest_folder = FolderSelectionWidget("DESTINATION FOLDER:")
        layout.addWidget(self.dest_folder)

        # Copy interval settings
        self.interval_settings = IntervalSettingsWidget()
        layout.addWidget(self.interval_settings)

        # Status messages
        self.status_list = StatusListWidget()
        layout.addWidget(self.status_list)

        # Footer
        self.footer = FooterWidget()
        layout.addWidget(self.footer)

        self.apply_styling()

    def connect_signals(self):
        self.source_folder.folder_selected.connect(self.app_logic.set_source_folder)
        self.dest_folder.folder_selected.connect(self.app_logic.set_destination_folder)
        self.interval_settings.interval_changed.connect(self.app_logic.set_copy_interval)
        self.app_logic.status_updated.connect(self.update_status)

    def apply_styling(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1E1E1E;
                color: #FFFFFF;
            }
            QLabel {
                color: #FFFFFF;
            }
            QPushButton {
                background-color: #FF4D00;
                color: #FFFFFF;
                border: none;
                padding: 5px 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #FF6E00;
            }
            QListWidget {
                background-color: #2D2D2D;
                color: #FFFFFF;
                border: 1px solid #FF4D00;
            }
            QSlider::groove:horizontal {
                border: 1px solid #999999;
                height: 8px;
                background: #2D2D2D;
                margin: 2px 0;
            }
            QSlider::handle:horizontal {
                background: #FF4D00;
                border: 1px solid #FF4D00;
                width: 18px;
                margin: -2px 0;
                border-radius: 3px;
            }
            QLineEdit {
                background-color: #2D2D2D;
                color: #FFFFFF;
                border: 1px solid #FF4D00;
                padding: 2px;
            }
        """)

    def update_status(self, message):
        self.status_list.add_status(message)

    def closeEvent(self, event: QCloseEvent) -> None:
        self.app_logic.cleanup()
        event.accept()