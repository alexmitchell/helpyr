#!/usr/bin/env python


import pandas as pd
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
                          f"Data dir is {self.source_dir}",
                          ])

        if destination_dir is not None:
            self.destination_dir = destination_dir
            self.destination_path = os.path.join(destination_dir, '{}.pkl')
            ensure_dir_exists(self.destination_dir, self.logger)
            self.logger.write([f"Pickle dir is {self.destination_dir}"])


    def is_pickled(self, *names):
        # Check to see if there is a pickled-data file

        # force names to be a list
        names = [names] if isinstance(names, str) else names
        plural = ["s", ""] if len(names) > 1 else ["","s"]
        msg = f"Checking if pickle{plural[0]} {names} exist{plural[1]}..."
        printer(msg, logger=self.logger)

        path = self.destination_path
        isfile = os.path.isfile
        return all([isfile(path.format(name)) for name in names])

    def load_pickle(self, name, add_path=True):
        # Load pickle data
        pkl_path = self.destination_path.format(name) if add_path else name
        try:
            return pd.read_pickle(pkl_path)
        else AttributeError:
            with open(pkl_path, mode='rb') as pkl_file:
                return pickle.load(pkl_file)

    def load_pickles(self, names, add_path=True):
        # Load pickle data store in dict
        output = {}
        for name in names:
            output[name] = self.load_pickle(name, add_path)
        return output

    def _get_filepath(self, name, is_path=False):
        return name if is_path else os.path.join(self.source_dir, name)

    def load_xlsx(self, filename, pd_kwargs, is_path=False):
        filepath = self._get_filepath(filename, is_path)

        data = pd.read_excel(filepath, **pd_kwargs)
        return data

    def load_txt(self, filename, kwargs, flip=False, is_path=False):
    #def load_txt(self, filename, skiprows, skipfooter, flip=False, delimiter='\s*'):
        filepath = self._get_filepath(filename, is_path)

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

        data = pd.read_csv(filepath, **kwargs)

        if flip:
            return data.iloc[::-1]
        else:
            return data

    def produce_pickles(self, prepickles):
        # Pickle things so I don't have to keep rereading the original files
        # prepickles is a dictionary of {'filename':data}
        # Returns a list of all the filepaths for the pickles produced
        printer("Performing pickling process...", logger=self.logger)
        destination_paths = []
        for name in prepickles:
            pkl_path = self.destination_path.format(name)
            printer(f"Making pickle {name} at {pkl_path}",logger=self.logger)
            try:
                prepickles[name].to_pickle(pkl_path)
            except AttributeError:
                with open(pkl_path, mode='wb') as pkl_file:
                    pickle.dump(prepickles[name], pkl_file)
            destination_paths.append(pkl_path)

        printer("Pickles produced!", logger=self.logger)

        return destination_paths

