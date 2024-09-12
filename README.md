# File Copier v1.2.2

## Features

- Support for multiple copy sets (source-destination pairs)
- Real-time, bidirectional synchronization for each copy set
- User-friendly GUI with improved visibility and contrast
- Initial full copy when folders are first selected for each copy set
- Robust "full rebuild" feature ensuring complete synchronization at specified intervals
- Real-time monitoring and handling of file changes (create, modify, delete, rename) for each copy set
- Customizable global synchronization interval
- Add and remove copy sets dynamically
- Detailed status messages for better tracking of synchronization process
- Countdown timer displaying time until next synchronization
- Built with PyQt6 and watchdog for robust performance

## Installation

1. Download the standalone executable for your platform from the assets below.
2. Run the executable to start the File Copier application.

## Usage

1. Launch the File Copier application.
2. Click "Add New Copy Set" to create a new source-destination pair.
3. For each copy set:
   - Click "SELECT" next to "Source:" to choose the source folder.
   - Click "SELECT" next to "Destination:" to choose the destination folder.
4. Set the global copy interval using the slider or input box at the bottom.
5. Monitor the synchronization status and countdown timer for all copy sets in the status area.
6. Add or remove copy sets as needed using the "Add New Copy Set" and "Remove" buttons.

## For Developers

If you want to run the application from source or contribute to the project:

1. Clone the repository:
   ```
   git clone https://github.com/adibzailan/file-copier.git
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the application:
   ```
   python ui_main.py
   ```

4. To package the application:
   ```
   python pyinstaller_script.py
   ```
   The packaged executable will be in the 'dist' folder.

## Feedback and Contributions

Feedback and contributions are always welcome to help improve the project! Please open an issue or submit a pull request on GitHub. Enjoy using File Copier!

## Changelog

### v1.2.2
- Implemented robust "full rebuild" feature for complete synchronization
- Added countdown timer for next synchronization
- Improved reliability of file copying at specified intervals
- Enhanced status messages with more detailed synchronization information
- Fixed issues with file updates in destination folders

### v1.2.1
- Fixed PyInstaller script to create a standalone executable
- Improved status messages and UI for better synchronization tracking
- Resolved issues with file copying at specified intervals

### v1.2.0
- Improved UI visibility and contrast
- Updated status list to ensure text is clearly visible
- Refined layout for better usability
- Updated PyInstaller script for improved packaging
- Added instructions for packaging the application in the README