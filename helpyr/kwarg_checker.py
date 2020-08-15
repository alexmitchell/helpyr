#!/usr/bin/env python3

def check_kwarg(kwargs, name, default=None, arg_type=None, required=False, pop=False):
    """ Simple function for checking a kwarg. Useful if you don't want to
    create a new object to check a kwarg or two. Pop=True will remove the 
    kwarg entry from kwargs if found. """
    if required:
        assert name in kwargs, "\n".join([
            "", 40*"#",
            f"## {name} not in kwargs",
            f"## kwargs has {kwargs.keys()}",
            40*"#", ""])
    out = default
    if name in kwargs:
        out = kwargs.pop(name) if pop else kwargs[name]

    _assert_types(out, name=name, arg_type=arg_type)
    return out

def get_check_kwarg_fu(function_kwargs, pop=False):
    """ Create a simple function for checking kwargs. Useful if you don't 
    need long term storage of KwargChecker and find supplying kwargs to 
    check_kwarg as an argument annoying. Pop will pop entries out of the 
    kwargs list if found. """
    def fu(name, default=None, required=False):
        return check_kwarg(function_kwargs, name,
                default=default, required=required, pop=pop)
    return fu



def check_add_kwarg(kwargs, name, default=None, arg_type=None, force=False):
    """ Simple function for checking if a name is in kwargs and adding a 
    default value if it isn't. If force is True, it will overwrite an
    existing value with default. It will also return the existing or default 
    value.
    """
    
    # Add or set the default if applicable
    if name not in kwargs or force:
        kwargs[name] = default
    
    _assert_types(kwargs[name], name=name, arg_type=arg_type)

    return kwargs[name]

def get_check_add_kwarg_fu(function_kwargs):
    """ Create a simple function for checking and adding kwargs. """
    def fu(name, default=None, arg_type=None, force=False):
        return check_add_kwarg(function_kwargs, name, 
                default=default, arg_type=arg_type, force=force)
    return fu




def _assert_types(arg, name='arg', arg_type=None):
    """Check types."""

    # Assert that it is the correct type, if applicable
    if arg_type is None or arg_type == '':
        return # No type requirements
     
    # Check that None is allowed if the arg is still None
    elif arg is None:
        assert 'none' in arg_type, f"{name} cannot be None"
        return # arg is okay, no further checking needed

    arg_type_str = f"({arg} is type {type(arg)})"

    # Check list types
    if 'list' in arg_type or 'tuple' in arg_type:
        assert isinstance(arg, (list, tuple))

        if isinstance(arg, list):
            assert 'list' in arg_type
            for element in arg:
                # Check each element
                _assert_types(element, name=name, 
                        arg_type=arg_type.replace('list','').strip('_- '))

        elif isinstance(arg, tuple):
            assert 'tuple' in arg_type
            for element in arg:
                # Check each element
                _assert_types(element, name=name, 
                        arg_type=arg_type.replace('tuple','').strip('_- '))

    # Check numeric types
    elif 'int' in arg_type and 'float' in arg_type:
        # int or float allowed
        assert isinstance(arg, (int, float)), \
                f"{name} must be a float or int {arg_type_str}"
    elif 'int' in arg_type:
        assert isinstance(arg, int), \
                f"{name} must be a int {arg_type_str}"
    elif 'float' in arg_type:
        assert isinstance(arg, float), \
                f"{name} must be a float {arg_type_str}"
    
    # Check string types
    elif 'str' in arg_type:
        assert isinstance(arg, str), \
                f"{name} must be a string {arg_type_str}"

    # Unknown type requirement
    else:
        print(f"arg={arg}, name={name}, arg_type={arg_type}")
        raise NotImplementedError

    # Check numeric sign
    if 'int' in arg_type or 'float' in arg_type:
        # Check sign
        if 'pos' in arg_type or 'counting' in arg_type:
            assert arg > 0, f"{name} must be greater than zero ({arg})"
        elif 'whole' in arg_type:
            assert arg >= 0, f"{name} must be greater or equal to zero ({arg})"
        elif 'neg' in arg_type:
            assert arg < 0, f"{name} must be less than zero ({arg})"
        else:
            pass # No sign requirements



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


