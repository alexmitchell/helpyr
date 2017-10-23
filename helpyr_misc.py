#!/usr/bin/env python3

import os

def ensure_dir_exists(dir_path, logger=None):
    # Creates directory if not already created
    # Return True if directory created or False if directory already 
    # exists.
    # logger is a Logger object (found in Helpyr)
    if not os.path.isdir(dir_path):
        os.makedirs(dir_path, exist_ok=True)
        if logger is not None:
            msg = "Making directory at {}.".format(dir_path)
            logger.write_log([msg])
        return True
    return False

