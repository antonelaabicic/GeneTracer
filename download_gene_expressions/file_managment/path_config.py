import os

def base_path(*paths):
    return os.path.join(os.path.dirname(os.path.abspath("main.py")), *paths)

def user_path(*paths):
    return os.path.join(os.path.expanduser("~"), *paths)

def create_directory(path):
    os.makedirs(path, exist_ok=True)

def setup_paths():
    driver_path = base_path('drivers', 'chromedriver.exe')

    gz_folder = user_path('Downloads', 'gz_files')
    unzipped_folder = user_path('Downloads', 'unzipped_files')

    create_directory(gz_folder)
    create_directory(unzipped_folder)

    return driver_path, gz_folder, unzipped_folder
