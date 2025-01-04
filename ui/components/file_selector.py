from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QTreeWidget, QTreeWidgetItem, 
                            QPushButton, QLabel, QHBoxLayout, QTreeWidgetItemIterator)
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QFont, QColor
from ..theme import Theme
import os

class FileSelector(QWidget):
    files_selected = pyqtSignal(list)  # Emits list of selected file paths

    def __init__(self):
        super().__init__()
        self.folder_path = None
        self.selected_files = set()  # Keep track of selected files
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Header
        header_layout = QHBoxLayout()
        header_label = QLabel("Select Files to Sync")
        header_label.setFont(QFont("Cerebri Sans", 12, QFont.Weight.Bold))
        header_label.setStyleSheet(f"color: {Theme.TEXT}; background-color: transparent;")
        header_layout.addWidget(header_label)
        layout.addLayout(header_layout)

        # Create and setup the tree widget
        self.file_tree = QTreeWidget()
        self.file_tree.setHeaderLabel("Files")
        self.file_tree.itemChanged.connect(self.on_item_changed)
        layout.addWidget(self.file_tree)

        # Style the tree widget
        self.file_tree.setStyleSheet(f"""
            QTreeWidget {{
                background-color: {Theme.SURFACE};
                border: 1px solid {Theme.BORDER};
                border-radius: 4px;
                color: {Theme.TEXT};
            }}
            QTreeWidget::item {{
                color: {Theme.TEXT};
                padding: 4px;
            }}
            QTreeWidget::item:hover {{
                background-color: {Theme.BACKGROUND};
            }}
            QTreeWidget::item:selected {{
                background-color: {Theme.PRIMARY}33;
            }}
            QTreeWidget::branch {{
                background-color: transparent;
                color: {Theme.TEXT};
            }}
            QHeaderView::section {{
                background-color: {Theme.SURFACE};
                color: {Theme.TEXT};
                padding: 4px;
                border: none;
            }}
        """)

        # Buttons
        button_layout = QHBoxLayout()
        select_all_btn = QPushButton("Select All")
        select_all_btn.clicked.connect(self.select_all)
        deselect_all_btn = QPushButton("Deselect All")
        deselect_all_btn.clicked.connect(self.deselect_all)
        button_layout.addWidget(select_all_btn)
        button_layout.addWidget(deselect_all_btn)
        layout.addLayout(button_layout)

        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {Theme.PRIMARY};
                color: {Theme.TEXT};
                border: none;
                padding: 4px 12px;
                border-radius: 4px;
                font-family: 'Cerebri Sans';
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {Theme.PRIMARY}DD;
            }}
        """)

    def get_selected_files(self):
        selected = []
        iterator = QTreeWidgetItemIterator(self.file_tree)
        while iterator.value():
            item = iterator.value()
            if item.checkState(0) == Qt.CheckState.Checked:
                selected.append(item.text(0))
            iterator += 1
        print(f"get_selected_files returning: {selected}")
        return selected

    def on_item_changed(self, item, column):
        if column == 0:  # Only handle checkbox changes
            file_path = item.text(0)
            checked = item.checkState(0) == Qt.CheckState.Checked
            print(f"Item changed: {file_path} -> {'checked' if checked else 'unchecked'}")
            
            if checked:
                self.selected_files.add(file_path)
            else:
                self.selected_files.discard(file_path)
            
            # Get all currently selected files
            selected = self.get_selected_files()
            print(f"Currently selected files: {selected}")
            self.files_selected.emit(selected)

    def update_folder(self, folder_type, folder_path):
        if folder_type == "source":  # Only update for source folder
            # Convert to Windows path format
            self.folder_path = folder_path.replace('/', '\\')
            print(f"Updating file selector with folder: {self.folder_path}")
            self.refresh_files()

    def refresh_files(self):
        print(f"Refreshing files from: {self.folder_path}")
        # Store the current selection state
        current_selection = self.selected_files.copy()
        
        self.file_tree.clear()
        if not self.folder_path or not os.path.exists(self.folder_path):
            print(f"Folder does not exist: {self.folder_path}")
            return

        try:
            # Walk through all directories recursively
            for root, dirs, files in os.walk(self.folder_path):
                # Get the relative path from the source folder
                rel_path = os.path.relpath(root, self.folder_path)
                if rel_path == '.':
                    parent = self.file_tree
                else:
                    # Create parent directory items
                    path_parts = rel_path.split('\\')
                    parent = self.file_tree
                    current_path = []
                    for part in path_parts:
                        current_path.append(part)
                        # Find or create the tree item for this path part
                        found = False
                        for i in range(parent.topLevelItemCount()):
                            if parent.topLevelItem(i).text(0) == part:
                                parent = parent.topLevelItem(i)
                                found = True
                                break
                        if not found:
                            item = QTreeWidgetItem(parent)
                            item.setText(0, part)
                            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
                            item.setCheckState(0, Qt.CheckState.Checked if '\\'.join(current_path) in current_selection else Qt.CheckState.Unchecked)
                            parent = item

                # Add files
                for file in sorted(files):
                    item = QTreeWidgetItem(parent)
                    item.setText(0, file)
                    item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
                    rel_file_path = os.path.join(rel_path, file).replace('/', '\\')
                    if rel_file_path == '.':
                        rel_file_path = file
                    item.setCheckState(0, Qt.CheckState.Checked if rel_file_path in current_selection else Qt.CheckState.Unchecked)

            # Restore selection state
            self.selected_files = current_selection

            # Expand all items
            self.file_tree.expandAll()
            print(f"File tree refreshed with {len(self.selected_files)} selected files")
        except Exception as e:
            print(f"Error refreshing files: {e}")

    def select_all(self):
        print("Selecting all files")
        iterator = QTreeWidgetItemIterator(self.file_tree)
        while iterator.value():
            item = iterator.value()
            item.setCheckState(0, Qt.CheckState.Checked)
            iterator += 1
        selected = self.get_selected_files()
        print(f"Selected all files: {selected}")
        self.files_selected.emit(selected)

    def deselect_all(self):
        print("Deselecting all files")
        iterator = QTreeWidgetItemIterator(self.file_tree)
        while iterator.value():
            item = iterator.value()
            item.setCheckState(0, Qt.CheckState.Unchecked)
            iterator += 1
        self.selected_files.clear()
        self.files_selected.emit([])
