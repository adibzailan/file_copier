import sys
import os
import pytest
from PyQt6.QtWidgets import QApplication

print("Executing conftest.py")

# Get the absolute path of the project root
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
print(f"Project root: {project_root}")

# Add the project root to the Python path
sys.path.insert(0, project_root)
print(f"Added {project_root} to sys.path")

@pytest.fixture(scope="session")
def qapp():
    """Create a QApplication instance for the entire test session."""
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    yield app

@pytest.fixture(scope="function", autouse=True)
def setup_function(qapp):
    """Setup for each test function."""
    yield
    # Add any cleanup code here if needed

@pytest.fixture(scope="session", autouse=True)
def add_project_root_to_path():
    # This fixture will run once before all tests
    print(f"Fixture: Added {project_root} to Python path")
    print("Current Python path:")
    for path in sys.path:
        print(path)

    # Try to import the modules here
    try:
        from ui.components.copy_set import CopySetWidget, CopySetManager
        from ui.components.folder_selection import FolderSelectionWidget
        from ui.components.footer import FooterWidget
        from ui.components.interval_settings import IntervalSettingsWidget
        from ui.components.status_list import StatusListWidget
        print("All imports successful in conftest.py!")
    except ImportError as e:
        print(f"Import error in conftest.py: {e}")

# Now you can import from ui without issues in your test files