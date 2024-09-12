import PyInstaller.__main__
import os

# Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Specify the path to your main script
main_script = os.path.join(current_dir, 'ui_main.py')

# Specify the path to your resources folder
resources_dir = os.path.join(current_dir, 'resources')

# Create a list of data files to include
data_files = [
    (os.path.join(resources_dir, 'fonts', '*.ttf'), 'resources/fonts'),
    # Add any other resource files or folders here
]

# Create a list of hidden imports
hidden_imports = [
    'PyQt6.QtCore',
    'PyQt6.QtGui',
    'PyQt6.QtWidgets',
    # Add any other hidden imports here
]

# Create the PyInstaller command
pyinstaller_command = [
    main_script,
    '--name=FileCopier',
    '--onefile',
    '--windowed',
    f'--add-data={os.path.pathsep}'.join([f"{src}{os.pathsep}{dst}" for src, dst in data_files]),
    f'--hidden-import={",".join(hidden_imports)}',
    '--icon=resources/icon.ico',  # Make sure you have an icon file
    '--clean',
    '--noconfirm',
]

# Run PyInstaller
PyInstaller.__main__.run(pyinstaller_command)

print("PyInstaller script completed. Check the 'dist' folder for the executable.")