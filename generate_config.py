#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import json
import xxhash
import argparse
from tqdm import tqdm
from concurrent.futures import ProcessPoolExecutor, as_completed

extensions = []

# The two folders with the same files with different filenames
folder_1 = r""
folder_2 = r""

def parse_args():
    parser = argparse.ArgumentParser(description="Compare two files.")
     # Using --nohash to disable hashing, default is True
    parser.add_argument('--partialhash', dest='partial_hash', action='store_true', help=r"Only does 10% hashing comparison when enabled. Makes code run faster but might be less accurate", default=False)
    return parser.parse_args()

class all_files_config:
    def __init__(self):
        self.files = []

class file_info:
    def __init__(self, filename, filesize, xhash):
        self.filename = filename
        self.filesize = filesize
        self.xhash = xhash

def get_filesize_kb(file_path):
    return os.path.getsize(file_path) / 1024

# Function to get partial hash (10% of the file)
def get_partial_hash(file_path, percent=10):
    #print(f"10% Hashing {file_path}")
    with open(file_path, 'rb') as f:
        file_size = os.path.getsize(file_path)
        bytes_to_read = int(file_size * (percent / 100))
        
        # Read the first 10% of the file
        first_part = f.read(bytes_to_read)
        
        # Read the last 10% of the file
        f.seek(file_size - bytes_to_read)
        last_part = f.read(bytes_to_read)
        
        combined = first_part + last_part
        
        # Calculate and return the hash
        hasher = xxhash.xxh3_128()
        hasher.update(combined)
        return hasher.hexdigest(), file_path


def get_xhash(file_path):
    #print(f"Hashing {file_path}")
    hasher = xxhash.xxh3_128()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b""):
            hasher.update(chunk)
    return hasher.hexdigest(), file_path

def generate_map_hash(directory, partial_hash=False):
    start_time = time.time()
    if partial_hash:
        hash_function = get_partial_hash
        print(f"Generating Hash Map using 10% of File Hashes")
    else:
        hash_function = get_xhash
        print(f"Generating Hash Map using Complete File Hashes")

    m = {}
    # Collect all file paths that match the extensions in the directory
    file_paths = [os.path.join(directory, f) for f in os.listdir(directory)
                  if any(f.endswith(ext) for ext in extensions)]
    
    # Initialize the progress bar with the total number of files
    with tqdm(total=len(file_paths), desc="Hashing Files") as progress_bar:
        with ProcessPoolExecutor() as executor:
            # Submit all file paths to the pool
            future_to_file = {executor.submit(hash_function, path): path for path in file_paths}
            
            for future in as_completed(future_to_file):
                xhash, file_path = future.result()
                if xhash not in m:
                    filename = os.path.basename(file_path)
                    m[xhash] = filename
                else:
                    print(f"Hash: {xhash} for Filename: {filename} matches Filename: {m[key].filename}")
                progress_bar.update(1)  # Update the progress bar after each file is processed

    print(f"Total Time to Generate Hash Map: {((time.time() - start_time) / 60):.2f} Minutes")

    return m

def main():
    """ Main program """

    # Parse command-line arguments
    args = parse_args()

    # if --partialhash CLI flag is used, then it's set to True and it only checks 10% of each files hash
    new_map = generate_map_hash(folder_2, args.partial_hash)
    original_map = generate_map_hash(folder_1, args.partial_hash)

    output_data = []  # List to store all file information
    count = 0
    for key in original_map.keys():
        if key in new_map.keys():
            count += 1
            original_file = original_map[key]
            new_file = new_map[key]
            print(f"File matches, Original File: {original_file} New File: {new_file}")
            # Add the information to the output data list
            output_data.append({
                "originalFileName": original_file,
                "newFileName": new_file,
                "xhash": key
            })
    print(f"Total Matching Files {count}")

    # Write the output data to a JSON file
    output_json_path = os.path.join(os.getcwd(), "file_mappings.json")
    with open(output_json_path, "w", encoding="utf-8") as json_file:
        json.dump(output_data, json_file, indent=4)

    print(f"File mappings saved to {output_json_path}")
    return 0

if __name__ == "__main__":
    main()
