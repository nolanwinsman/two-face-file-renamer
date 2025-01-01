# Example

My specific use case was that I had a bunch of ripped Playstation 2 roms on my hard drive. I liked to keep them named a certain way, but when I transferred them to my Playstation 2 console I had to change the filenames. 

For example I had `Kingdom Hearts (USA).iso` and `SLUS_203.70.Kingdom Hearts.iso` in two seperate folders even though they're the exact same file.

I didn't want to keep two folders of all the roms since each folder was 700+ GB so I wrote this script to quickly rename the files back and forth. 

The script uses [xhash](https://github.com/Cyan4973/xxHash) values to determine if the two files are the same file just different filenames.

Since `.iso` files are typically very large, I used the `--partialhash` flag to only calculate 10% of the hash value of each file.

An example section of my `file_mappings.json` after running my script on my two folders is below

```json
{
    "originalFileName": "Kingdom Hearts (USA).iso",
    "newFileName": "SLUS_203.70.Kingdom Hearts.iso",
    "xhash": "21610e9eaade0f55fdeb680c3dc86772"
},
```

So based on the value of `TOGGLE` in `rename_files.py` I can change the filename of `Kingdom Hearts (USA).iso` to `SLUS_203.70.Kingdom Hearts.iso` and vice versa very quickly