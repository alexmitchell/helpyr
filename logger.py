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

    def write(self, messages, verbose=None, local_indent=0):
        # Write a message to the log file
        if messages is None:
            # don't print anything if message is None
            return

        if isinstance(messages, str):
            # Turn messages into a list of strings
            messages = [messages]

        msg_indent = (self.global_indent + local_indent) * self.indent_str
        for message in messages:
            message = msg_indent + message
            if not self.no_log:
                with open(self.log_filepath, 'a') as lf:
                    lf.write(message + '\n')

            if (verbose is None and self.verbose) or verbose:
                print(message)

    def write_blankline(self, n=1, verbose=False):
        self.write(['']*n, verbose=verbose)

    def run_indented_function(self, function, before_msg=None, after_msg=None):
        # Runs the provided function with automatically indented internal log 
        # messages.
        # Function takes no args and cannot return anything
        self.write(before_msg)
        self.increase_global_indent()
        function()
        self.decrease_global_indent()
        self.write(after_msg)
        self.write_blankline()

    def warning(self, messages):
        warning_msg = "Warning: "
        self.write(warning_msg + messages[0] + ":")
        self.write(messages[1:], local_indent=1)
