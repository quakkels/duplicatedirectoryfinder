# Duplicate Directory Finder

## What is this program?
Duplicate Directory Finder will scan all of the subdirectories of in a particular folder on your computer, create a hash for each subdirectory, and then save Excel files on your computer that indicate whether some of those subdirectories are duplicates or not.

### Does it work with NAS devices?

Yes, as long as the NAS is mounted as a drive letter on your computer. It can take a while if you have a particularly large NAS, however.

### Where are these Excel files saved? What are they called?

They are saved in the same directory as where you ran the program from. They will be called “Duplicate Folders {timestamp}.xlsx” and “Folder Hashes {timestamp}.xlsx”

### What about empty directories?

Because they would generate a ton of false positives, directories with zero files in them are ignored for the duplicate analysis.



I recommend using a Virtual Environment (venv) when running this project locally using Python version 3.6.5 or above.

## Installation
1. Clone this repository
1. Activate your venv
1. Execute `pip install -r requirements.txt`

## Usage
```
> python duplicate_directory.py C:\path\to\directory\to\crawl
```