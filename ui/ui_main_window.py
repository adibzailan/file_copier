from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea, QApplication, QSplitter, QPushButton
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QFontDatabase, QCloseEvent
from .components.copy_set import CopySetManager, CopySetWidget
from .components.interval_settings import IntervalSettingsWidget
from .components.status_list import StatusListWidget
from .components.footer import FooterWidget
from .theme import Theme
from core.app_logic import AppLogic, CopySet
import time

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("File Copier")
        self.setGeometry(100, 100, 1200, 800)
        self.app_logic = AppLogic()
        self.load_fonts()
        self.setup_ui()
        self.connect_signals()
        self.app_logic.load_config()
        self.setStyleSheet(Theme.WINDOW_STYLE)

    def load_fonts(self):
        font_dir = "resources/fonts/"
        font_files = [
            "Cerebri Sans Bold.ttf",
            "Cerebri Sans Book.ttf",
            "HankenGrotesk-Regular.ttf",
            "HankenGrotesk-Bold.ttf"
        ]
        for font_file in font_files:
            QFontDatabase.addApplicationFont(font_dir + font_file)

    def setup_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        main_widget.setLayout(main_layout)

        # Left panel (Copy Set Manager)
        left_panel = QWidget()
        left_layout = QVBoxLayout()
        left_layout.setContentsMargins(16, 16, 16, 16)
        left_layout.setSpacing(16)
        left_panel.setLayout(left_layout)

        # Copy Set Manager
        self.copy_set_manager = CopySetManager()
        copy_set_scroll = QScrollArea()
        copy_set_scroll.setWidgetResizable(True)
        copy_set_scroll.setWidget(self.copy_set_manager)
        copy_set_scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollArea > QWidget > QWidget {
                background-color: transparent;
            }
        """)
        left_layout.addWidget(copy_set_scroll)

        # Right panel
        right_panel = QWidget()
        right_layout = QVBoxLayout()
        right_layout.setContentsMargins(16, 16, 16, 16)
        right_layout.setSpacing(16)
        right_panel.setLayout(right_layout)

        # Interval Settings
        self.interval_settings = IntervalSettingsWidget()
        right_layout.addWidget(self.interval_settings)

        # Countdown timer
        self.countdown_label = QLabel("Next sync in: --:--")
        self.countdown_label.setFont(QFont("Hanken Grotesk", 16, QFont.Weight.Bold))
        self.countdown_label.setStyleSheet(f"color: {Theme.TEXT}; background-color: transparent;")
        self.countdown_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        right_layout.addWidget(self.countdown_label)

        # Status List
        self.status_list = StatusListWidget()
        self.status_list.setStyleSheet(Theme.STATUS_STYLE)
        right_layout.addWidget(self.status_list)
        right_layout.addStretch()

        # Add panels to main layout
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setStretchFactor(0, 2)
        splitter.setStretchFactor(1, 1)
        main_layout.addWidget(splitter)

        # Footer
        footer = FooterWidget(version="v2.0.0")
        footer.setStyleSheet(Theme.FOOTER_STYLE)
        self.statusBar().addWidget(footer)

    def connect_signals(self):
        self.copy_set_manager.set_added.connect(self.add_copy_set)
        self.copy_set_manager.set_removed.connect(self.remove_copy_set)
        self.copy_set_manager.folders_updated.connect(self.app_logic.update_copy_set)
        self.copy_set_manager.files_updated.connect(self.update_copy_set_files)
        self.interval_settings.interval_changed.connect(self.app_logic.set_copy_interval)
        self.app_logic.status_updated.connect(self.update_status)
        self.app_logic.countdown_updated.connect(self.update_countdown)

    def add_copy_set(self):
        print("Adding new copy set")
        new_set_id = len(self.copy_set_manager.copy_sets) + 1
        copy_set_widget = CopySetWidget(new_set_id)
        new_copy_set = CopySet(new_set_id)  # Create a new CopySet instance
        
        # Connect signals
        copy_set_widget.removed.connect(self.remove_copy_set)
        copy_set_widget.folders_selected.connect(lambda widget, folder_type, path: self.update_copy_set_folders(widget, new_copy_set, folder_type, path))
        copy_set_widget.files_selected.connect(self.app_logic.update_copy_set_files)
        copy_set_widget.sync_started.connect(lambda widget: self.app_logic.sync_all_copy_sets())
        copy_set_widget.sync_stopped.connect(lambda widget: self.app_logic.cleanup())
        
        self.copy_set_manager.add_copy_set_widget(copy_set_widget)  # Changed to add_copy_set_widget
        self.app_logic.add_copy_set(new_copy_set)  # Pass the CopySet instance

    def remove_copy_set(self, copy_set_widget):
        print(f"Removing copy set {copy_set_widget.set_id}")
        copy_set = self.app_logic.copy_sets.get(copy_set_widget.set_id)
        if copy_set:
            self.app_logic.remove_copy_set(copy_set)
        self.copy_set_manager.on_copy_set_removed(copy_set_widget)

    def update_copy_set_folders(self, widget, copy_set, folder_type, path):
        if folder_type == "source":
            copy_set.source_folder = path
        elif folder_type == "destination":
            copy_set.destination_folder = path
        
        # Update the AppLogic with the new folder paths
        self.app_logic.update_copy_set(copy_set, copy_set.source_folder, copy_set.destination_folder)

    def update_copy_set_files(self, set_id, selected_files):
        print(f"Updating files for Copy Set {set_id}")
        print(f"Selected files: {selected_files}")
        self.app_logic.update_copy_set_files(set_id, selected_files)

    def update_status(self, message):
        if "Starting synchronization" in message:
            self.status_list.add_status(message, is_important=True)
        elif "Synchronization completed" in message:
            self.status_list.add_status(message, is_important=True)
        else:
            self.status_list.add_status(message)

    def update_countdown(self, seconds_remaining):
        minutes, seconds = divmod(seconds_remaining, 60)
        self.countdown_label.setText(f"Next sync in: {minutes:02d}:{seconds:02d}")

    def closeEvent(self, event: QCloseEvent) -> None:
        self.app_logic.cleanup()
        event.accept()

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()