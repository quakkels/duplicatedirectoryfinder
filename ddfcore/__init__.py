import hashlib
import time
import os
import sys

class DuplicateDirectoryFinder:

    start_directory = ""
    directory_hashes = []
    found_duplicates = []

    def __init__(self, start_directory):
        self.start_directory = start_directory
    
    def find_duplicates(self):
        stuff = self.__traverse(self.start_directory)
        return stuff

    def __traverse(self, directory):
        self.__print_progress_update(directory)

        files_count = 0
        directories_count = 0
        folder_size = 0
        hash_me = ""
        files = self.__retry_oserror(self.__get_files, directory)
        for file in files:
            files_count += 1
            size = self.__retry_oserror(os.path.getsize, file)
            folder_size += size
            hash_me += str(self.__retry_oserror(os.path.getmtime, file))
            hash_me += str(size)

        sub_directories = self.__retry_oserror(self.__get_sub_directories, directory)
        for sub_directory in sub_directories:
            directories_count += 1
            (sub_directories_count, sub_files_count, sub_folder_size, hash
                ) = self.__traverse(sub_directory)
            directories_count += sub_directories_count
            files_count += sub_files_count
            folder_size += sub_folder_size
            hash_me += str(hash)

        directory_hash = self.__hash_string(hash_me)
        duplicate = self.__find_duplicate(directory_hash)
        if duplicate is not None:
            self.found_duplicates.append((duplicate, directory, directories_count, files_count, folder_size))

        self.directory_hashes.append((directory_hash, directory, directories_count, files_count, folder_size))
        return (
            directories_count, 
            files_count,
            folder_size,
            directory_hash
        )
    
    def __find_duplicate(self, hash):
        for saved_hash, directory, dir_count, files_count, folder_size in self.directory_hashes:
            if saved_hash == hash:
                return directory
        return None

    def __hash_string(self, str):
        str_bytes = str.encode('utf-8')
        hasher = hashlib.sha1(str_bytes)
        return hasher.hexdigest()

    def __get_sub_directories(self, directory):
        sub_dirs = [] 
        for o in os.listdir(directory): 
            if os.path.isdir(directory):
                sub_dirs.append(os.path.join(directory,o))
        return sub_dirs

    def __get_files(self, directory):
        return [os.path.join(directory, o) 
            for o in os.listdir(directory) 
                if os.path.isfile(os.path.join(directory,o))]

    def __retry_oserror(self, func, *args):
        retry_count = 10
        for i in range(0, 10):
            try:
                result = func(*args)
                return result
            except OSError as error:
                if i >= retry_count:
                    print("Unable to recover from OSError[", 
                    error.strerror, "] while using [", 
                    func, "] with [", 
                    args, "] after [", 
                    retry_count, "] retry attempts.")
                    raise error
        
        return []

    def __print_progress_update(self, current_directory):
        print('Crawling:', current_directory)

if __name__ == "__main__":
    start_directory = sys.argv[1]
    ddf = DuplicateDirectoryFinder(start_directory)
    start = time.time()
    directories_count, files_count, folder_size, directory_hash = ddf.find_duplicates()
    print(f"Directories Count: {directories_count}")
    print(f"Files Count: {files_count}")
    print(f"Folder Size: {folder_size}")
    print(f"Directory Hash: {directory_hash}")

    # todo: fix showing files as duplicate directories.
    for item in ddf.found_duplicates:
        print(item)

    end = time.time()