import os
import shutil
import time
import hashlib
from datetime import datetime

def calculate_file_hash(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as file:
        for chunk in iter(lambda: file.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def copy_with_timestamp(src, dst_dir):
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H_%M_%S")
    base, ext = os.path.splitext(src)
    dst = os.path.join(dst_dir, f"{timestamp}{ext}")
    shutil.copy(src, dst)

print("After youve got all the PSDs Go to File > Scripts > Image Processor to turn them all to PNGs. \n")
source_file = input("Enter the source file path: ")

# Extract the filename from the source file path
    # source_filename = os.path.basename(source_file)
source_filename = source_file



# Create a destination directory with a unique name (source filename + timestamp)
now = datetime.now()
timestamp = now.strftime("%Y%m%d%H%M%S")
destination_dir = f"{source_filename}_SaveHistory"
os.makedirs(destination_dir, exist_ok=True)

last_hash = None

while True:
    if os.path.exists(source_file):
        current_hash = calculate_file_hash(source_file)
        if current_hash != last_hash:
            print(f"File '{source_file}' has changed. Copying...")
            copy_with_timestamp(source_file, destination_dir)
            print(f"File '{source_file}' copied to '{destination_dir}'")
            last_hash = current_hash
    time.sleep(12)  # Check for changes every second
