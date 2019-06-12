#!/usr/bin/env python3

def check_kwarg(kwargs, name, default=None, required=False):
    """ Simple function for checking a kwarg. Useful if you don't want to
    create a new object to check a kwarg or two. """
    if required:
        assert name in kwargs
    return kwargs[name] if name in kwargs else default

def get_check_kwarg_fu(function_kwargs):
    """ Create a simple function for checking kwargs. Useful if you don't 
    need long term storage of KwargChecker and find supplying kwargs to 
    check_kwarg as an argument annoying. """
    def fu(name, default=None, required=False):
        return check_kwarg(function_kwargs, name,
                default=default, required=required)
    return fu


class KwargChecker:
    """ Simple kwarg checking class. Better ones almost certainly exist 
    elsewhere, but this was easy to make and does exactly what I need."""

    def __init__(self, kwargs):
        self.kwargs = kwargs

    def kwarg_check(self, name, default=None):
        if name in self.kwargs:
            return self.kwargs[name]
        else:
            return default


