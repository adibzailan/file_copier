import PyInstaller.__main__
import os

# Get the absolute path of the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

PyInstaller.__main__.run([
    'ui_main.py',  # Your main script
    '--name=FileCopier',  # Name of the executable
    '--onefile',  # Create a single executable file
    '--windowed',  # Use the windowed subsystem (no console)
    '--icon=resources/icon.ico',  # Icon for the executable (create this if you want)
    '--add-data=ui;ui',  # Include the ui package
    '--add-data=core;core',  # Include the core package
    '--clean',  # Clean PyInstaller cache and remove temporary files
    '--noconfirm',  # Replace output directory without asking for confirmation
    f'--distpath={os.path.join(current_dir, "dist")}',  # Output directory for the final executable
    f'--workpath={os.path.join(current_dir, "build")}',  # Directory for temporary files
    f'--specpath={os.path.join(current_dir, "build")}',  # Directory for the spec file
])
