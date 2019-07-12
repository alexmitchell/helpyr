#!/usr/bin/env python3

def check_kwarg(kwargs, name, default=None, required=False, pop=False):
    """ Simple function for checking a kwarg. Useful if you don't want to
    create a new object to check a kwarg or two. Pop=True will remove the 
    kwarg entry from kwargs if found. """
    if required:
        assert name in kwargs
    if name in kwargs:
        return kwargs.pop(name) if pop else kwargs[name]
    else:
        return default

def get_check_kwarg_fu(function_kwargs, pop=False):
    """ Create a simple function for checking kwargs. Useful if you don't 
    need long term storage of KwargChecker and find supplying kwargs to 
    check_kwarg as an argument annoying. Pop will pop entries out of the 
    kwargs list if found. """
    def fu(name, default=None, required=False):
        return check_kwarg(function_kwargs, name,
                default=default, required=required, pop=pop)
    return fu



def check_add_kwarg(kwargs, name, default, force=False):
    """ Simple function for checking if a name is in kwargs and adding a 
    default value if it isn't. If force is True, it will overwrite an
    existing value with default. """
    if name not in kwargs or force:
        kwargs[name] = default

def get_check_add_kwarg_fu(function_kwargs):
    """ Create a simple function for checking and adding kwargs. """
    def fu(name, default, force=False):
        return check_add_kwarg(function_kwargs, name, default, force=force)
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


