# Duplicate Directory Finder
import hashlib
import time
import os

class DuplicateDirectoryFinder:

    start_directory = ""
    directory_total = 0
    directory_hashes = []
    found_duplicates = []

    def __init__(self, start_directory):
        self.start_directory = start_directory
    
    def find_duplicates(self):
        self.directory_total = self.__get_directory_total()
        stuff = self.__traverse(self.start_directory)
        self.__print_progress_bar(len(self.directory_hashes), self.directory_total, 
            prefix="Crawling",
            suffix="\t| " + str(len(self.directory_hashes)) +" of "+ str(self.directory_total) +" directories",
            length=40)
        return stuff
    
    def __get_directory_total(self):
        directories = [x[0] for x in os.walk(self.start_directory)]
        return len(directories)

    def __traverse(self, directory):
        self.__print_progress_bar(len(self.directory_hashes), self.directory_total, 
            prefix="Crawling",
            suffix="\t| " + str(len(self.directory_hashes)) +" of "+ str(self.directory_total) +" directories",
            length=40)
        
        files_count = 0
        directories_count = 0
        hash_me = ""
        files = self.__retry_oserror(self.__get_files, directory)
        for file in files:
            files_count += 1
            hash_me += str(self.__retry_oserror(os.path.getmtime, file))
            hash_me += str(self.__retry_oserror(os.path.getsize, file))

        sub_directories = self.__retry_oserror(self.__get_sub_directories, directory)
        for sub_directory in sub_directories:
            directories_count += 1
            (sub_directories_count, sub_files_count, hash
                ) = self.__traverse(sub_directory)
            directories_count += sub_directories_count
            files_count += sub_files_count
            hash_me += str(hash)

        directory_hash = self.__hash_string(hash_me)
        duplicate = self.__find_duplicate(directory_hash)
        if duplicate is not None:
            self.found_duplicates.append((duplicate, directory))

        self.directory_hashes.append((directory_hash, directory))
        return (
            directories_count, 
            files_count,
            directory_hash
        )
    
    def __find_duplicate(self, hash):
        for saved_hash, directory in self.directory_hashes:
            if saved_hash == hash:
                return directory
        return None

    def __hash_string(self, str):
        str_bytes = str.encode('utf-8')
        hasher = hashlib.sha1(str_bytes)
        return hasher.hexdigest()

    def __get_sub_directories(self, directory):
        return [os.path.join(directory, o) 
            for o in os.listdir(directory) 
                if os.path.isdir(os.path.join(directory,o))]

    def __get_files(self, directory):
        return [os.path.join(directory, o) 
            for o in os.listdir(directory) 
                if os.path.isfile(os.path.join(directory,o))]

    def __retry_oserror(self, func, *args):
        retry_count = 10
        for i in range(0, 10):
            try:
                result = func(*args)
                break
            except OSError as error:            
                if i >= retry_count:
                    print("Unable to recover from OSError[", 
                    error.strerror, "] while using [", 
                    func, "] with [", 
                    args, "] after [", 
                    retry_count, "] retry attempts.")
                    raise error
        return result

    def __print_progress_bar(self, iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█'):
        """
        Call in a loop to create terminal progress bar
        @params:
            iteration   - Required  : current iteration (Int)
            total       - Required  : total iterations (Int)
            prefix      - Optional  : prefix string (Str)
            suffix      - Optional  : suffix string (Str)
            decimals    - Optional  : positive number of decimals in percent complete (Int)
            length      - Optional  : character length of bar (Int)
            fill        - Optional  : bar fill character (Str)
        """

        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + '-' * (length - filledLength)
        print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')
        # Print New Line on Complete
        if iteration >= total: 
            print("")

if __name__ == "__main__":
    start_directory = "C:\\Users\\quakkels\\Pictures"
    start_directory = "C:\\Users\\quakkels\\books"

    ddf = DuplicateDirectoryFinder(start_directory)

    start = time.time()
    dir_count, file_count, nothing = ddf.find_duplicates()
    end = time.time()