#!/usr/bin/env python3

import os.path

from helpyr_misc import ensure_dir_exists

class Logger:

    def __init__(self, log_filepath="./log-crawler.txt", default_verbose=False, no_log=False):
        self.verbose = default_verbose
        self.global_indent = 0
        self.indent_str = 4*' '
        self.no_log = no_log or log_filepath is None or "" == log_filepath

        if self.no_log:
            print("Logger is set to not log")

        else:
            self.log_filepath = log_filepath
            ensure_dir_exists(os.path.split(log_filepath)[0], logger=self)


    def increase_global_indent(self):
        self.global_indent += 1

    def decrease_global_indent(self):
        if self.global_indent >= 1:
            self.global_indent -= 1


    def write_section_break(self):
        self.write([80*'#', 80*' '])

    def write(self, messages, verbose=False, local_indent=0):
        # Write a message to the log file
        msg_indent = (self.global_indent + local_indent) * self.indent_str

        if isinstance(messages, str):
            # Turn messages into a list of strings
            messages = [messages]

        for message in messages:
            message = msg_indent + message
            if not self.no_log:
                with open(self.log_filepath, 'a') as lf:
                    lf.write(message + '\n')

            if self.verbose or verbose:
                print(message)

    def write_blankline(self, verbose=False):
        self.write([''], verbose=verbose)


