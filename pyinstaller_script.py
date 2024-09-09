import PyInstaller.__main__

PyInstaller.__main__.run([
    'ui_main.py',
    '--onefile',
    '--windowed',
    '--name=FileCopier',
    '--add-data=config.json:.',
    '--add-data=ui:ui',
    '--hidden-import=PyQt6',
    '--hidden-import=watchdog',
])