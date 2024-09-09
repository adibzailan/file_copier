# File Copier

File Copier is a simple, user-friendly application that allows you to automatically copy files from a source folder to a destination folder at specified intervals. It provides a graphical user interface for easy configuration and monitoring of the file copying process.

## Features

- Select source and destination folders through a graphical interface
- Specify files to be copied
- Set custom copy intervals (in minutes)
- Real-time status updates
- File change detection and immediate copying
- Dark mode interface for comfortable usage

## Requirements

- Python 3.6 or higher
- PyQt6
- watchdog

## Installation

1. Clone this repository or download the source code.

2. Install the required dependencies:

```
pip install -r requirements.txt
```

## Usage

To run the File Copier application, execute the following command in the project directory:

```
python ui_main.py
```

This will launch the graphical user interface. From here, you can:

1. Select the source folder
2. Select the destination folder
3. Specify the files to be copied
4. Set the copy interval
5. Monitor the status of the copying process

## Packaging the Application

To create a standalone executable that can be run on systems without Python installed, you can use PyInstaller. There are two methods to package the application:

### Method 1: Using the PyInstaller script

Run the following command:

```
python pyinstaller_script.py
```

### Method 2: Running PyInstaller directly

Run the following command:

```
pyinstaller --onefile --windowed ui_main.py
```

Both methods will create an executable file in the `dist` folder. You can distribute this executable to run the application on other systems without requiring Python or the dependencies to be installed.

## File Structure

- `ui_main.py`: The main entry point of the application
- `ui/ui_main_window.py`: Contains the MainWindow class and UI setup
- `ui/ui_file_watcher.py`: Contains FileWatcher and FileChangeHandler classes
- `ui/ui_file_copier.py`: Contains the FileCopier class
- `pyinstaller_script.py`: Script for packaging the application with PyInstaller
- `config.json`: Configuration file for storing user settings

## License

This project is open-source and available under the MIT License.