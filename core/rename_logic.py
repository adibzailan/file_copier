import os

class RenameLogic:
    @staticmethod
    def add_prefix_suffix(filename, prefix='', suffix=''):
        name, ext = os.path.splitext(filename)
        return f"{prefix}{name}{suffix}{ext}"

    @staticmethod
    def swap_characters(filename, old_char, new_char):
        return filename.replace(old_char, new_char)

    @staticmethod
    def rename_file(src_path, new_name):
        try:
            dir_path = os.path.dirname(src_path)
            new_path = os.path.join(dir_path, new_name)
            os.rename(src_path, new_path)
            return f"File renamed: {os.path.basename(src_path)} to {new_name}"
        except Exception as e:
            return f"Error renaming file: {str(e)}"

    @staticmethod
    def batch_rename(folder_path, rename_function, *args):
        results = []
        for filename in os.listdir(folder_path):
            if os.path.isfile(os.path.join(folder_path, filename)):
                new_name = rename_function(filename, *args)
                result = RenameLogic.rename_file(os.path.join(folder_path, filename), new_name)
                results.append(result)
        return results