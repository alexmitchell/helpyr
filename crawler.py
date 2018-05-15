import os
import fnmatch
from time import asctime

import logger as logger_module

# Crawler class traverses a directory tree to find target file types and 
# perform operations on those files. This is a base class that should be 
# expanded by inheriting class.

class Crawler:

    def __init__(self, logger=None):
        self.logger = logger# if logger is not None\
                #else logger_module.Logger(log_filepath="/dev/null")
        self._write_log(["Begin crawler output", asctime()])

        self.set_root("./", verbose=False)
        self.set_target_names(["*\.*"], verbose=False) # default to all files
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


    def collect_names(self, verbose_file_list=True):
        # Collect the target names. Stores the list internally, does not return 
        # a value. verbose_file_list controls whether the files found should be 
        # printed out to the log file. 
        self.file_list = []

        self._write_log(["Collecting file names..."])

        for dirpath, subdirnames, filenames in os.walk(self.root):
            for filename in filenames:
                for target in self.target_names:
                    if fnmatch.fnmatch(filename, target):
                        filepath = os.path.join(dirpath, filename)
                        self.file_list.append(filepath)
        n_files = len(self.file_list)
        self._write_log(self.file_list, local_indent=1, verbose=verbose_file_list)
        self._write_log([f"Names collected. {n_files} files found"])

    def get_target_files(self, target, verbose_file_list=True):
        # returns the list of collected names. meant to simplify the use of the 
        # crawler when it plays a smaller role in your code.
        # * or ? for wildcards
        self.set_target_names(target)
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

