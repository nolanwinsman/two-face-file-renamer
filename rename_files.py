#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json

# when True, will attempt to rename originalFileName to newFilename
# when False, will attempt to rename newFilename to originalFileName
TOGGLE = True

def generate_maps():
    m = {}
    k = "originalFileName" if TOGGLE else "newFileName"
    new_filename = "originalFileName" if not TOGGLE else "newFileName"

    with open(r"file_mappings.json", 'r') as f:
        data = json.load(f)
        for thing in data:
            m[thing[k]] = thing[new_filename]
    return m

def main():

    m = generate_maps()
    
    # change string to point to directory you want to rename files
    directory = r""

    file_paths = [os.path.join(directory, f) for f in os.listdir(directory)]
    for file in file_paths:
        bs = os.path.basename(file)
        if bs in m:
            dir_path = os.path.dirname(os.path.realpath(file))
            new_file = os.path.join(dir_path, m[bs])
            print(f"Renaming {file} to {new_file}")
            os.rename(file, new_file)    

    return 0

if __name__ == "__main__":
    main()
