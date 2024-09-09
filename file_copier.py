import os
import shutil
import time
import json

def load_config():
    with open('config.json', 'r') as config_file:
        return json.load(config_file)

def copy_files(config):
    source_folder = config['source_folder']
    destination_folder = config['destination_folder']
    files_to_copy = config['files_to_copy']

    for file in files_to_copy:
        source_path = os.path.join(source_folder, file)
        destination_path = os.path.join(destination_folder, file)
        
        try:
            if os.path.exists(source_path):
                shutil.copy2(source_path, destination_path)
                print(f"Copied {file} to {destination_folder}")
            else:
                print(f"Source file {file} not found")
        except Exception as e:
            print(f"Error copying {file}: {str(e)}")

def main():
    config = load_config()
    delay = config.get('delay', 60)  # Default delay of 60 seconds if not specified

    print("File copier started. Press Ctrl+C to exit.")
    try:
        while True:
            copy_files(config)
            time.sleep(delay)
    except KeyboardInterrupt:
        print("File copier stopped.")

if __name__ == "__main__":
    main()