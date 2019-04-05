#!/usr/bin/env python3


class KwargChecker:
    """ Simple kwarg checking class. Better ones almost certainly exist 
    elsewhere, but this was easy to make and does exactly what I need."""

    def __init__(self, kwargs):
        self.kwargs = kwargs

    def kwarg_check(self, name, default):
        if name in self.kwargs:
            return self.kwargs[name]
        else:
            return default


