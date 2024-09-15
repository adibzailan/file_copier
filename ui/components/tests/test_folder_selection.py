import pytest
from PyQt6.QtWidgets import QApplication
from ui.components.folder_selection import FolderSelectionWidget

@pytest.fixture
def app(qapp):
    return qapp

class TestFolderSelectionWidget:
    def test_initialization(self, app):
        folder_selection = FolderSelectionWidget("Test Label")
        assert folder_selection is not None
        assert folder_selection.label_text == "Test Label"

    def test_initial_state(self, app):
        folder_selection = FolderSelectionWidget("Test Label")
        assert folder_selection.folder_path == ""
        assert folder_selection.path_input.text() == ""
        assert folder_selection.path_input.placeholderText() == "Select a folder..."

    def test_set_path(self, app):
        folder_selection = FolderSelectionWidget("Test Label")
        test_path = "/test/path"
        folder_selection.set_path(test_path)
        assert folder_selection.folder_path == test_path
        assert folder_selection.path_input.text() == test_path

    def test_get_path(self, app):
        folder_selection = FolderSelectionWidget("Test Label")
        test_path = "/test/path"
        folder_selection.set_path(test_path)
        assert folder_selection.get_path() == test_path

    # Note: Testing the select_folder method would require mocking QFileDialog,
    # which is beyond the scope of this basic test suite.