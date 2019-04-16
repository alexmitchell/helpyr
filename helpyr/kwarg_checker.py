#!/usr/bin/env python3

def check_kwarg(kwargs, name, default=None):
    """ Simple function for checking a kwarg. Useful if you don't want to
    create a new object to check a kwarg or two. """
    return kwargs[name] if name in kwargs else default

def get_check_kwarg_fu(kwargs):
    """ Create a simple function for checking kwargs. Useful if you don't 
    need long term storage of KwargChecker and find supplying kwargs to 
    check_kwarg as an argument annoying. """

    fu = lambda name, default: \
        kwargs[name] if name in kwargs else default
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


