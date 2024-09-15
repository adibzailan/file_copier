import sys
import os

# Get the absolute path of the project root
project_root = os.path.abspath(os.path.dirname(__file__))

# Add the project root to the Python path
sys.path.insert(0, project_root)

# Now try to import the modules
try:
    from ui.components.copy_set import CopySetWidget, CopySetManager
    from ui.components.folder_selection import FolderSelectionWidget
    from ui.components.footer import FooterWidget
    from ui.components.interval_settings import IntervalSettingsWidget
    from ui.components.status_list import StatusListWidget
    print("All imports successful!")
except ImportError as e:
    print(f"Import error: {e}")

# Print the sys.path to see where Python is looking for modules
print("\nPython path:")
for path in sys.path:
    print(path)