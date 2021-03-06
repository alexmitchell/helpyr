#!/usr/bin/env python3

import os

def print_entire_df(df):
    from pandas import option_context
    # Print all rows in a dataframe
    with option_context('display.max_rows', None):
        print(df)

def nsplit(path, n, fsplit=os.path.split, fargs=None):
    # Recursively splits 'path' 'n' times. Returns a n+1 length list. Could 
    # *not* find a way to condense into a one liner.... :/ (updated since then 
    # so a one liner would be impractical)
    # fsplit allows user to choose splitting function and provide args in fargs
    head, tail = fsplit(path, *fargs) if fargs is not None else fsplit(path)
    return  nsplit(head, n-1) + [tail] if n and tail else [path]

def ensure_dir_exists(dir_path, logger=None):
    # Creates directory if not already created
    # Return True if directory created or False if directory already 
    # exists.
    # logger is a Logger object (found in Helpyr)
    if not os.path.isdir(dir_path):
        os.makedirs(dir_path, exist_ok=True)
        msg = "Making directory at {}.".format(dir_path)
        if logger is None:
            print(msg)
        else:
            logger.write([msg])
        return True
    return False

def printer(msg='', n=1, verbose=True, logger=None):
    msgs = msg*n
    if logger is None:
        if verbose:
            for msg in msgs:
                print(msg)
    else:
        logger.write(msgs)

def isnumeric(obj):
    # Test whether an object is numeric or not.
    # Code is from some stack exchange answer.
    try:
        float(obj)
        return True
    except ValueError:
        return False

def exclude_df_cols(dataframe, exclude):
    # Return a list of target columns from a dataframe with some excluded.
    # Assumes a panda dataframe
    # exclude should be a list of column labels
    return [col for col in dataframe.columns.values if col not in exclude]

