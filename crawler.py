import os
import fnmatch
from time import asctime

# Crawler class traverses a directory tree to find target file types and 
# perform operations on those files. This is a base class that should be 
# expanded by inheriting class.

class Crawler:

    def __init__(self, log_filepath="./log-crawler.txt"):
        self.log_indent = 0
        self.log_filepath = log_filepath
        self.ensure_dir_exists(os.path.split(log_filepath)[0])
        self.write_log_section_break()
        self.write_log(["Begin crawler output", asctime()], verbose=True)

        self.set_root("./")
        self.set_target_names(["*\.*"])
        self.file_list = []
        self.mode_dict = {'all': self.run_all}

    
    def write_log_section_break(self):
        self.write_log([80*'#', 80*' '])

    def write_log(self, messages, verbose=False, indent=0):
        # Write a message to the log file
        indent_str = 4*' '
        msg_indent = (self.log_indent + indent) * indent_str
        with open(self.log_filepath, 'a') as lf:
            for message in messages:
                message = msg_indent + message
                lf.write(message + '\n')
                if verbose:
                    print(message)

    def write_log_blankline(self, verbose=False):
        self.write_log([''], verbose=verbose)

    def increase_log_indent(self):
        self.log_indent += 1

    def decrease_log_indent(self):
        if self.log_indent >= 1:
            self.log_indent -= 1


    def end(self):
        self.write_log(["End crawler output", asctime()], verbose=True)


    def set_root(self, root_dir):
        self.root = root_dir
        self.write_log(["Root dir set to " + root_dir])

    def set_target_names(self, target_names):
        self.target_names = target_names
        self.write_log(["Target names set to:"])
        self.write_log(target_names, indent=1)


    def ensure_dir_exists(self, dir_path):
        # Creates directory if not already created
        # Return True if directory created or False if directory already 
        # exists.
        if not os.path.isdir(dir_path):
            os.makedirs(dir_path, exist_ok=True)
            msg = "Making directory at {}.".format(dir_path)
            self.write_log([msg], True)
            return True
        return False

    def collect_names(self):
        self.file_list = []

        self.write_log(["Collecting file names..."])

        for dirpath, subdirnames, filenames in os.walk(self.root):
            for filename in filenames:
                for target in self.target_names:
                    if fnmatch.fnmatch(filename, target):
                        filepath = os.path.join(dirpath, filename)
                        self.file_list.append(filepath)
        self.write_log(self.file_list, verbose=True, indent=1)
        self.write_log(["Names collected."])

    def run(self, mode='all'):
        self.mode_dict[mode]()

    def run_all(self):
        self.write_log_section_break()
        self.write_log(["Running all modes"], verbose=True)
        self.mode_dict.pop('all')
        for key in self.mode_dict:
            self.mode_dict[key]()

