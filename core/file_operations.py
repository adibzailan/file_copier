import os
import shutil

class FileOperations:
    @staticmethod
    def copy_file(src_path, dest_path):
        try:
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            shutil.copy2(src_path, dest_path)
            return f"File copied: {os.path.basename(src_path)}"
        except Exception as e:
            return f"Error copying file: {str(e)}"

    @staticmethod
    def delete_file(dest_path):
        try:
            if os.path.exists(dest_path):
                os.remove(dest_path)
                return f"File deleted: {os.path.basename(dest_path)}"
            return f"File not found: {os.path.basename(dest_path)}"
        except Exception as e:
            return f"Error deleting file: {str(e)}"

    @staticmethod
    def move_file(src_path, dest_path):
        try:
            if os.path.exists(src_path):
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                shutil.move(src_path, dest_path)
                return f"File moved: {os.path.basename(src_path)} to {os.path.basename(dest_path)}"
            return f"Source file not found: {os.path.basename(src_path)}"
        except Exception as e:
            return f"Error moving file: {str(e)}"

    @staticmethod
    def initial_full_copy(source_folder, dest_folder):
        try:
            for root, dirs, files in os.walk(source_folder):
                for file in files:
                    src_path = os.path.join(root, file)
                    rel_path = os.path.relpath(src_path, source_folder)
                    dest_path = os.path.join(dest_folder, rel_path)
                    FileOperations.copy_file(src_path, dest_path)
            return "Initial full copy completed."
        except Exception as e:
            return f"Error during initial full copy: {str(e)}"