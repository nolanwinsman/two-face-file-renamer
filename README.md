# two-face-file-renamer

Two Python scripts to handle a unique problem I had with wanting to keep two versions of filenames for one file. I now know this could probably be achieved with hard links or sym links but this was a fun project to tackle. 

A more detailed description of my usecase is in [example](docs/example.md) section


## [How This Script Works Example](docs/example.md)

## Getting Started

Modify the values of `folder_1` `folder_2` in `generate_config.py` to point to the two folders you want to create the config json for

Run `generate_config.py`

If you are trying to run this script on larger files, I highly recommend you add the `--partialhash` flag as it will only calculate 10% of the hash and runs much faster as a majority of the time a complete hash value isn't needed for the files.

```sh
python generate_config.py --partialhash
```

this will create the file `file_mappings.json`

Now that `file_mappings.json` is created, you can run `rename_files.py` whenever you want to rename the files. Make sure to change the value of `TOGGLE` in the script to switch from renaming the `originalFileNames` to `newFileName` and vice versa

```sh
python rename_files.py
```

## Installation

1. Clone the repo

```sh
git clone https://github.com/nolanwinsman/two-face-file-renamer.git
```

# Contact

Nolan Winsman - [@Github](https://github.com/nolanwinsman) - nolanwinsman@gmail.com

Project Link: [https://github.com/nolanwinsman/two-face-file-renamer.git](https://github.com/nolanwinsman/two-face-file-renamer.git)

# Contributers

- nolanwinsman

## Files

* generate_config.py : generates the file_mappings.json file by comparing hash values of files between two directories to determine if they're the same file
* rename_files.py : renames the files based off of file_mappings.json
* docs/ : documents folder for more markdown files
    * example.md : 
* README.md : this file
