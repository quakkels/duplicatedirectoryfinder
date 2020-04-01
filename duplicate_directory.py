# Duplicate Directory Finder

import time
import os
import sys
from openpyxl import Workbook
import ddf

# Get the current working directory (if supplied by user)
cur_dir = ''
if len(sys.argv) > 2:
    print('Please put folder names with spaces inside of double quotes')
    sys.exit()

if len(sys.argv) == 2:
    if os.path.isdir(sys.argv[1]):
        start_directory = sys.argv[1]
    else:
        print('That was not a valid directory')
        sys.exit()
else:
    print("Please provide a valid directory.")
    sys.exit()

# Set up the Duplicate Directory Object
finder = ddf.DuplicateDirectoryFinder(start_directory)

# Set up the timestamps 
start = time.time()
dir_count, file_count, nothing = finder.find_duplicates()
end = time.time()

# Print the timestamps to the user
print('The program ran for', (end - start),' seconds.')

# Save entire array to Excel file using OpenPyXL
print('Saving Results to file')
print()
wb = Workbook()
ws = wb.active

# Set up header info in Excel file
ws['A1'] = 'Hash Value'
ws['B1'] = 'Directory Name'

# Loop through and save array
for a in range (0, len(finder.directory_hashes)):
    hash, dir_name =  finder.directory_hashes[a]
    ws['A' + str(a + 2)] = hash
    ws['B' + str(a + 2)] = dir_name

# Save the file in the current directory
wb.save('All Folder Hashes.xlsx')

# Save just the duplicate files to another to Excel file
wb = Workbook()
ws = wb.active
ws['A1'] = 'Directory 1'
ws['B1'] = 'Directory 2'
for a in range (0, len(finder.found_duplicates)):
    hash, dir_name =  finder.found_duplicates[a]
    ws['A' + str(a + 2)] = hash
    ws['B' + str(a + 2)] = dir_name
wb.save('Duplicate Folders.xlsx')

print('Results saved as All Folder Hashes.xlsx and Duplicate Folders.xlsx')
print('Total files and directories checked: ' + str(dir_count + file_count))
print('Total potential duplicates identified: ' + str(len(finder.found_duplicates)))
print()