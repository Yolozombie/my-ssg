import os
import shutil

def copy_files_recursive(source, destination):
    for item in os.listdir(source):
        from_path = os.path.join(source, item)
        to_path = os.path.join(destination, item)
        
        if os.path.isfile(from_path):
            # copy file
            shutil.copy(from_path, to_path)
            print(f"copy: {from_path} -> {to_path}")
        else:
            # it's a map
            # 1. make the map of destination (os.mkdir)
            os.mkdir(to_path)
            # 2. call the function with the interieur of the map
            copy_files_recursive(from_path, to_path)

            



