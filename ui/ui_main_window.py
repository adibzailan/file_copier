from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea, QApplication, QSplitter, QPushButton
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QFontDatabase, QCloseEvent
from .components.copy_set import CopySetManager
from .components.interval_settings import IntervalSettingsWidget
from .components.status_list import StatusListWidget
from .components.footer import FooterWidget
from core.app_logic import AppLogic

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

        # Title
        title_label = QLabel("File Copier")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setFont(QFont("Cerebri Sans", 32, QFont.Weight.Bold))
        left_layout.addWidget(title_label)

        # Copy Set Manager
        self.copy_set_manager = CopySetManager()
        copy_set_scroll = QScrollArea()
        copy_set_scroll.setWidgetResizable(True)
        copy_set_scroll.setWidget(self.copy_set_manager)
        left_layout.addWidget(copy_set_scroll)

        # Right panel (Settings and Status)
        right_panel = QWidget()
        right_panel.setObjectName("rightPanel")
        right_layout = QVBoxLayout()
        right_layout.setContentsMargins(16, 16, 16, 16)
        right_layout.setSpacing(16)
        right_panel.setLayout(right_layout)

        # Copy interval settings
        self.interval_settings = IntervalSettingsWidget()
        right_layout.addWidget(self.interval_settings)

        # Countdown timer
        self.countdown_label = QLabel("Next sync in: --:--")
        self.countdown_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.countdown_label.setFont(QFont("Hanken Grotesk", 16, QFont.Weight.Bold))
        right_layout.addWidget(self.countdown_label)

        # Status messages
        self.status_list = StatusListWidget()
        right_layout.addWidget(self.status_list)

        # Footer
        self.footer = FooterWidget()
        right_layout.addWidget(self.footer)

        # Add left and right panels to main layout
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setStretchFactor(0, 2)  # Left panel takes up 2/3 of the space
        splitter.setStretchFactor(1, 1)  # Right panel takes up 1/3 of the space
        main_layout.addWidget(splitter)

        self.apply_styling()

    def connect_signals(self):
        self.copy_set_manager.set_added.connect(self.app_logic.add_copy_set)
        self.copy_set_manager.set_removed.connect(self.app_logic.remove_copy_set)
        self.copy_set_manager.folders_updated.connect(self.app_logic.update_copy_set)
        self.interval_settings.interval_changed.connect(self.app_logic.set_copy_interval)
        self.app_logic.status_updated.connect(self.update_status)
        self.app_logic.countdown_updated.connect(self.update_countdown)

    def apply_styling(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #F5F5F5;
                color: #333333;
            }
            QLabel {
                color: #333333;
                font-family: 'Hanken Grotesk';
                font-size: 14px;
            }
            QPushButton {
                background-color: #FF6F61;
                color: #F5F5F5;
                border: none;
                padding: 8px 16px;
                font-family: 'Cerebri Sans';
                font-weight: bold;
                border-radius: 4px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #FF8D82;
            }
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                border: none;
                background: #F5F5F5;
                width: 10px;
                margin: 0px 0px 0px 0px;
            }
            QScrollBar::handle:vertical {
                background: #FF6F61;
                min-height: 20px;
                border-radius: 5px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
            QSplitter::handle {
                background-color: #E0E0E0;
            }
            QWidget {
                padding: 4px;
            }
            #rightPanel {
                background-color: #F5F5F5;
            }
        """)

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