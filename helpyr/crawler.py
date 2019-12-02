import os
from os.path import join as pjoin
import fnmatch
from time import asctime
from time import sleep
from math import log10
import sys

from helpyr import logger as logger_module

# Crawler class traverses a directory tree to find target file types and 
# perform operations on those files. This is a base class that should be 
# expanded by inheriting class.

class Crawler:

    def __init__(self, logger=None):
        self.logger = logger# if logger is not None\
                #else logger_module.Logger(log_filepath="/dev/null")
        self._write_log(["Begin crawler output", asctime()])

        self.set_root(os.getcwd(), verbose=False)
        self.set_target_names(["*\.*"], verbose=False) # default to all files
        self.target_dirs = []
        self.file_list = []
        self.mode_dict = {'all': self.run_all}

    def end(self):
        self._write_log(["End crawler output", asctime()])


    def _write_log_section_break(self):
        if self.logger is not None:
            self.logger.write_section_break()

    def _write_log(self, messages, **kwargs):
        if self.logger is not None:
            self.logger.write(messages, **kwargs)

    def _write_log_search_marker(self):
        if self.logger is not None:
            self.logger.end_output()


    def set_root(self, root_dir, verbose=True):
        self.root = root_dir
        self._write_log(["Root dir set to " + root_dir], verbose=verbose)

    def set_target_names(self, target_names, verbose=True):
        # * or ? for wildcards
        if isinstance(target_names, str):
            target_names = [target_names]
        self.target_names = target_names
        self._write_log(["Target names set to:"], verbose=verbose)
        self._write_log(target_names, local_indent=1, verbose=verbose)

    def set_target_dirs(self, target_dirs, verbose=True):
        # * or ? for wildcards
        if isinstance(target_dirs, str):
            target_dirs = [target_dirs]
        self.target_dirs = target_dirs
        self._write_log(["Target directories set to:"], verbose=verbose)
        self._write_log(target_dirs, local_indent=1, verbose=verbose)


    def collect_names(self, verbose_file_list=True):
        # Collect the target names. Stores the list internally, does not return 
        # a value. verbose_file_list controls whether the files found should be 
        # printed out to the log file. The list can get very long and clutter 
        # up the log file or start hogging too much hard drive space.
        self.file_list = []
        n_files_target = 1
        def print_i(i, n_found):
            print(f"{i} files checked so far ({n_found} matches)", end='\r', flush=True)
            sys.stdout.flush()
            #sleep(0.1)

        self._write_log(["Collecting file names..."])

        have_dirs = bool(self.target_dirs)
        have_names = bool(self.target_names)
        for dirpath, subdirnames, filenames in os.walk(self.root):
            current_dir = os.path.split(dirpath)[1]
            if not have_dirs or (have_dirs and have_names):
                if have_dirs and current_dir not in self.target_dirs:
                    # Directory is not in the list of target directories
                    # Skip this dir
                    continue

                # Either no target directory specified (all dirs okay)
                # or current_dir matches a target directory
                for i, filename in enumerate(filenames):
                    # file in target directory or there are not target dirs
                    for target in self.target_names:
                        if fnmatch.fnmatch(filename, target):
                            # filename matches one of the target patterns
                            # record it and break out of the innermost loop
                            filepath = pjoin(dirpath, filename)
                            self.file_list.append(filepath)
                            break
                    
                    # print some updates
                    i += 1
                    if i >= n_files_target:
                        print_i(i, len(self.file_list))
                        logi = int(log10(i)) if i != 0 else 0
                        n_files_target += 10**logi

            elif current_dir in self.target_dirs:
                # Have target dirs but no target names
                # Add all non-hidden files
                filepaths = [
                        pjoin(dirpath, fname)
                        for fname in filenames
                        if fname[0] != '.' # ignore hidden files
                        ]
                self.file_list += filepaths

        if verbose_file_list:
            self._write_log(self.file_list, local_indent=1, verbose=verbose_file_list)

        n_files = len(self.file_list)
        self._write_log([f"Names collected. {n_files} files found"])


    def get_target_files(self, target_names=[], target_dirs=[], verbose_file_list=True):
        # returns the list of collected names. meant to simplify the use of the 
        # crawler when it plays a smaller role in your code.
        # * or ? for wildcards
        # target_dirs controls what directory the files should be in
        # verbose_file_list controls whether the file list will be printed out 
        # to the terminal
        self.set_target_names(target_names)
        self.set_target_dirs(target_dirs)
        self.collect_names(verbose_file_list=verbose_file_list)
        return self.file_list

    def run(self, mode='all'):
        self.mode_dict[mode]()

    def run_all(self):
        self._write_log_section_break()
        self._write_log(["Running all modes"])

        self.mode_dict.pop('all')
        for key in self.mode_dict:
            self.mode_dict[key]()

