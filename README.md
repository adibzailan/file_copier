# File Copier

File Copier is a robust, user-friendly application that allows you to automatically synchronize files from a source folder to a destination folder in real-time. It provides a graphical user interface for easy configuration and monitoring of the file synchronization process.

## Features

- Select source and destination folders through a graphical interface
- Real-time file synchronization:
  - Instant copying of newly added files
  - Immediate updates for modified files
  - Instant deletion of removed files
  - Real-time handling of file renaming/moving
- Periodic full synchronization at specified intervals
- Customizable synchronization interval (in minutes)
- Real-time status updates and logging
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
3. Set the synchronization interval for full syncs (real-time sync is always active)
4. Monitor the status of the synchronization process

The application will start watching the source folder for changes immediately and will perform a full sync at the specified interval.

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
- `ui/ui_main_window.py`: Contains the MainWindow class, UI setup, and event handling
- `ui/ui_file_watcher.py`: Contains FileWatcher class for real-time file monitoring
- `ui/ui_file_copier.py`: Contains the FileCopier class for file operations
- `pyinstaller_script.py`: Script for packaging the application with PyInstaller
- `config.json`: Configuration file for storing user settings

## How It Works

1. **Real-time File Watching**: The application uses the `watchdog` library to monitor the source folder for any file system events (creation, modification, deletion, moving/renaming).

2. **Event Handling**: When a file event is detected, the application immediately processes the event:
   - For new or modified files: The file is copied to the destination folder.
   - For deleted files: The corresponding file in the destination folder is removed.
   - For moved/renamed files: The file is moved/renamed in the destination folder accordingly.

3. **Periodic Full Sync**: In addition to real-time synchronization, the application performs a full synchronization at the user-specified interval. This ensures that any changes that might have been missed are accounted for.

4. **User Interface**: The GUI provides an easy way to configure the source and destination folders, set the full sync interval, and view real-time status updates of all synchronization activities.

## License

This project is open-source and available under the MIT License.