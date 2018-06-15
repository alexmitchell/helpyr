#!/usr/bin/env python


import pandas as pd
from numpy import loadtxt as np_loadtxt
import os
import pickle

import logger as logger_module
from helpyr_misc import printer
from helpyr_misc import ensure_dir_exists

class DataLoader:

    def __init__(self, source_dir, destination_dir=None, logger=None):
        self.source_dir = source_dir
        self.logger = logger
        self.logger.write(["DataLoader created",
                          f"Source dir is {self.source_dir}",
                          ])

        self.destination_dir = destination_dir
        if destination_dir is not None:
            ensure_dir_exists(self.destination_dir, self.logger)
            self.logger.write([f"Destination dir is {self.destination_dir}"])


    def format_picklepath(self, name, dir):
        return os.path.join(dir, f"{name}.pkl")

    def _get_filepath(self, name, add_path=True):
        return os.path.join(self.source_dir, name) if add_path else name

    def is_pickled(self, names, add_path=True, use_destination=True):
        # Check to see if there is a pickled-data file for the provided name(s)

        # force names to be a list
        lnames = [names] if isinstance(names, str) else names
        plural = len(lnames) > 1
        p1 = 's' if plural else ''
        p2 = ''  if plural else 's'
        p3 = ''  if plural else 'es'
        msg = f"Checking if pickle{p1} {names} exist{p2}..."
        printer(msg, logger=self.logger)

        dir = self.destination_dir if use_destination else self.source_dir
        format_pkl = lambda name: self.format_picklepath(name, dir) if add_path else name
        isfile = os.path.isfile

        exists = all([isfile(format_pkl(name)) for name in lnames])
        e1 = '' if exists else 'not '
        msg = f"Pickle{p1} do{p3} {e1}exist"
        printer(msg, logger=self.logger)
        return exists


    def load_pickle(self, name, add_path=True, use_source=True):
        # Load pickle data
        # use_source allows you to pick if the target pickle is in the 
        # source_dir or destination_dir. 
        if isinstance(name, list):
            # was given a list of names, pass it to the plural function
            return self.load_pickles(name, add_path=add_path, use_source=use_source)

        dir = self.source_dir if use_source else self.destination_dir
        pkl_path = self.format_picklepath(name, dir) if add_path else name
        try:
            return pd.read_pickle(pkl_path)
        except AttributeError:
            with open(pkl_path, mode='rb') as pkl_file:
                return pickle.load(pkl_file)

    def load_pickles(self, names, add_path=True, use_source=True):
        # Load pickle data from list of names and return in dict
        # dict is {name: data}
        output = {}
        for name in names:
            output[name] = self.load_pickle(name, add_path, use_source)
        return output

    def load_xlsx(self, filename, pd_kwargs, add_path=True):
        filepath = self._get_filepath(filename, add_path)

        data = pd.read_excel(filepath, **pd_kwargs)
        return data

    def load_txt(self, filename, kwargs, flip=False, add_path=True):
        # filename is can be the filename or filepath of a txt file
        # kwargs are passed into the panda read_csv function
        # flip is whether to vertically flip the data
        # add_path indicates whether to add a root path (if filename is just a
        #  name) or not add a root path (if filename is already a filepath)
        filepath = self._get_filepath(filename, add_path)

        # Some default parameters
        keys = kwargs.keys()
        if 'engine' not in keys:
            kwargs['engine'] = 'python'
        if 'dtype' not in keys:
            kwargs['dtype'] = None
        if 'index_col' not in keys:
            kwargs['index_col'] = 0
        if 'delimiter' not in keys:
            kwargs['delimiter'] = r'\s+' # any whitespace

        try:
            data = pd.read_csv(filepath, **kwargs)
        except:
            print(filename)
            raise

        if flip:
            return data.iloc[::-1]
        else:
            return data

    def load_txt_np(self, filename, kwargs={}, flip=False, add_path=True):
        # filename is can be the filename or filepath of a txt file
        # kwargs are passed into the panda read_csv function
        # flip is whether to vertically flip the data
        # add_path indicates whether to add a root path (if filename is just a
        #  name) or not add a root path (if filename is already a filepath)
        filepath = self._get_filepath(filename, add_path)

        try:
            data = np_loadtxt(filepath, **kwargs)
        except:
            print(filename)
            raise

        if flip:
            return data[::-1]
        else:
            return data


    def produce_pickles(self, prepickles, add_path=True, verbose=True, overwrite=False):
        # Pickle things so I don't have to keep rereading the original files
        # prepickles is a dictionary of {'pickle_name':data}
        # pickle_name will be used to create the filename
        # Returns a list of all the filepaths for the pickles produced
        #if verbose: printer("Performing pickling process...", logger=self.logger)
        destination_paths = []
        dest_dir = self.destination_dir
        target_dir = dest_dir if dest_dir is not None else self.source_dir
        for name in prepickles:
            pkl_path = self.format_picklepath(name, target_dir) if add_path else name
            pkl_filename = name if add_path else os.path.split(name)[1]

            if not overwrite and os.path.isfile(pkl_path):
                if verbose:
                    printer(f"Pickle already exists (skipping): {pkl_path}", logger=self.logger)
                continue
            if verbose:
                if overwrite and os.path.isfile(pkl_path):
                    printer(f"Overwriting {pkl_filename} at {pkl_path}", logger=self.logger)
                else:
                    printer(f"Pickling {pkl_filename} at {pkl_path}", logger=self.logger)
            try:
                prepickles[name].to_pickle(pkl_path)
            except AttributeError:
                with open(pkl_path, mode='wb') as pkl_file:
                    pickle.dump(prepickles[name], pkl_file)
            destination_paths.append(pkl_path)

        #if verbose: printer("Pickles produced!", logger=self.logger)

        return destination_paths

    def save_txt(self, data, filename, kwargs={}, is_path=False):
        filepath = self._get_filepath(filename, is_path)
        if is_path:
            ensure_dir_exists(os.path.split(filepath)[0])

        # Some default parameters
        keys = kwargs.keys()
        if 'sep' not in keys:
            kwargs['sep'] = '\t'
        if 'na_rep' not in keys:
            kwargs['na_rep'] = 'NaN'
        if 'float_format' not in keys:
            kwargs['float_format'] = "%8.3f"
        if 'index' not in keys:
            kwargs['index'] = False
        if 'header' not in keys:
            kwargs['header'] = True

        with open(filepath, mode='tw') as txt_file:
            data.to_csv(txt_file, **kwargs)
