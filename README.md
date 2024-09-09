# File Copier v1.1.0

## Features

- Support for multiple copy sets (source-destination pairs)
- Real-time, bidirectional synchronization for each copy set
- User-friendly GUI with dark mode
- Initial full copy when folders are first selected for each copy set
- Periodic full synchronization at user-specified intervals (global setting for all copy sets)
- Real-time monitoring and handling of file changes (create, modify, delete, rename) for each copy set
- Customizable global synchronization interval
- Add and remove copy sets dynamically
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
5. Monitor the synchronization status for all copy sets in the status area.
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

## Feedback and Contributions

Feedback and contributions are always welcome to help improve the project! Please open an issue or submit a pull request on GitHub. Enjoy using File Copier!

## Changelog

### v1.1.0
- Added support for multiple copy sets
- Implemented dynamic adding and removing of copy sets
- Updated UI to accommodate multiple copy sets
- Improved status reporting to show events for each copy set
- Global synchronization interval now applies to all copy sets

### v1.0.0
- Initial release with single copy set functionality
- Real-time, bidirectional synchronization between two folders
- User-friendly GUI with dark mode
- Initial full copy and periodic full synchronization
- Real-time monitoring and handling of file changes
