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
    (os.path.join(resources_dir, 'fonts'), 'resources/fonts'),
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
]

# Add data files
for src, dst in data_files:
    pyinstaller_command.extend(['--add-data', f'{src}{os.pathsep}{dst}'])

# Add hidden imports
for imp in hidden_imports:
    pyinstaller_command.extend(['--hidden-import', imp])

# Check if icon file exists and add it to the command
icon_path = os.path.join(resources_dir, 'icon.ico')
if os.path.exists(icon_path):
    pyinstaller_command.extend(['--icon', icon_path])

# Add other options
pyinstaller_command.extend([
    '--clean',
    '--noconfirm',
])

# Run PyInstaller
PyInstaller.__main__.run(pyinstaller_command)

print("PyInstaller script completed. Check the 'dist' folder for the executable.")