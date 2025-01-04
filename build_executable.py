import PyInstaller.__main__
import os
import shutil

def build_executable():
    # Clean previous build artifacts
    for dir_name in ['build', 'dist']:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
    
    # PyInstaller options
    options = [
        'ui_main.py',  # Main script
        '--name=FileCopier',  # Output name
        '--onefile',  # Create a single executable
        '--windowed',  # Don't show console window
        '--add-data=ui;ui',  # Include UI package
        '--add-data=core;core',  # Include core package
        '--clean',  # Clean PyInstaller cache
        '--noconfirm',  # Replace output directory without confirmation
    ]
    
    # Run PyInstaller
    PyInstaller.__main__.run(options)
    
    print("Build completed! Executable is in the dist directory.")

if __name__ == '__main__':
    build_executable()
