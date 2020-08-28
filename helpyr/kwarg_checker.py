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

    type_handle = _assert_types(out, name=name, arg_type=arg_type)
    if type_handle is None:
        # No type casting
        return out
    elif isinstance(type_handle, (list, tuple)):
        # Type casting elements in a list
        return [th(element) for th, element in zip(type_handle, out)]
    else:
        # Type casting a single output variable
        return type_handle(out)

def get_check_kwarg_fu(function_kwargs, pop=False):
    """ Create a simple function for checking kwargs. Useful if you don't 
    need long term storage of KwargChecker and find supplying kwargs to 
    check_kwarg as an argument annoying. Pop will pop entries out of the 
    kwargs list if found. """
    def fu(name, default=None, arg_type=None, required=False):
        return check_kwarg(function_kwargs, name,
                default=default, arg_type=arg_type, 
                required=required, pop=pop)
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
    
    out = kwargs[name]
    type_handle = _assert_types(out, name=name, arg_type=arg_type)
    if type_handle is None:
        # No type casting
        return out
    elif isinstance(type_handle, (list, tuple)):
        # Type casting elements in a list
        return [th(element) for th, element in zip(type_handle, out)]
    else:
        # Type casting a single output variable
        return type_handle(out)

def get_check_add_kwarg_fu(function_kwargs):
    """ Create a simple function for checking and adding kwargs. """
    def fu(name, default=None, arg_type=None, force=False):
        return check_add_kwarg(function_kwargs, name, 
                default=default, arg_type=arg_type, force=force)
    return fu



def _generic_assert_type(arg, arg_name, type_handle, type_name, type_casting_ok):
    """Assert if the arg is of type(s) type_handle or, if type_casting_ok is 
    True, assert if the arg can be cast to any of type_handle.

    Parameters
    ----------
    arg : 
        The variable being checked.
    arg_name : string
        The name of the variable used for the error message.
    type_handle : 
        The handle for the variable type desired. Can be a single handle (e.g. 
        type_handle=int) or a sequence of handles (e.g. type_handle=(int, 
        float)).
    type_name : 
        The name of the type(s) for the error message. (e.g. 'int or float')
    type_casting_ok:
        Indicates whether type casting is allowed. However, the function only 
        checks that it is possible. **The function does not actually recast the 
        variable.** 

    Returns
    -------
    type_handle :
        The returned type handle will be the same as the input type_handle 
        unless type_casting_ok is True and there are multiple accepted types. 
        If so, the return handle will be the first successful type to cast the 
        variable.
    """
    error_message = f"{arg_name} ({type(arg)}) must be of type {type_name}"
    output_type_handle = type_handle
    try:
        # See if arg is of type(s) type_handle
        assert isinstance(arg, type_handle), error_message

    except AssertionError as wrong_type_error:
        # arg is not of type type_handle
       
        # If type casting is not allowed, re-raise the failure
        if not type_casting_ok:
            raise wrong_type_error

        # Type casting is allowed, see if arg can be casted to type(s) 
        # type_handle
        if isinstance(type_handle, (tuple, list)):
            # Multiple accepted types, see if arg can be cast to any
            # RETURNS the first type handle that is successful
            for th in type_handle:
                try:
                    assert isinstance(th(arg), th)
                    output_type_handle = th
                    break
                except:
                    pass
            else:
                # Failed to find a valid casting type
                raise wrong_type_error
        else:
            # Single accepted type, see if arg can be cast to it
            try:
                assert isinstance(type_handle(arg), type_handle)
            except (AssertionError, ValueError, TypeError):
                raise wrong_type_error

    # Assertions all passed
    return output_type_handle

def _assert_types(arg, name='arg', arg_type=None):
    """Assert that arg is the correct type, if applicable.

    Parameters
    ----------
    arg :
        The variable to be checked.

    name :
        The name of the arg to be used for error messages.

    arg_type :
        A string representing the accepted type or types for the variable. 
        Currently handles the basic types: 'list', 'tuple', 'int', 'float', 
        'str', and 'bool').  Can specify extra qualifiers too. Multiple 
        types and qualifiers can be present in the string. Order only matters 
        if checking casting between both int and float(e.g. 'int-float' vs. 
        'float-int'), where the first ones are given preference.

        Extra qualifiers:
        'none' = Allows the arg to be None even if something else was specified
        'tcast' = 
            If the var does not match the provided type(s), allows the program 
            to check if the variable can be cast to the desired type(s). 'pos', 
            'whole', 'neg' = Asserts an 'int' or 'float' variable is >0, >=0, 
            or <0, respectively.

        Examples:
        '' or None = No type specifications, check will unconditionally pass.
        'float-none' = Check if the variable is a float or None.
        'float-int-pos' = Check if variable is a positive (>0) float or int.
        'int-whole-tcast' =
            Check if variable is or can be cast to a whole (>=0) int.

    Returns
    -------
    If type casting is allowed, returns the successful casting type. (First one 
    if there are multiple accepted types) If type casting is not allowed, the 
    return variable is not useful.
    """

    # No type requirements
    if arg_type is None or arg_type == '':
        return
     
    # Check that None is allowed if the arg is still None
    elif arg is None:
        assert 'none' in arg_type, f"{name} cannot be None"
        return # arg is okay, no further checking needed

    type_casting_ok = 'tcast' in arg_type
    output_type_handle = None
    is_sequence = False

    # Check list types
    if 'list' in arg_type or 'tuple' in arg_type:
        is_sequence = True
        # For either lists or tuples, assert that all elements are a valid type

        assert isinstance(arg, (list, tuple))
        if isinstance(arg, list):
            assert 'list' in arg_type
        elif isinstance(arg, tuple):
            assert 'tuple' in arg_type

        output_type_handle = []
        sequence_arg_type = \
                arg_type.replace('list','').replace('tuple', '').strip('_- ')
        for element in arg:
            # Check each element
            output_type_handle.append(
                    _assert_types(
                        element, name=name, arg_type=sequence_arg_type)
                    )

    # Check numeric types
    elif 'int' in arg_type and 'float' in arg_type:
        # int or float allowed
        # The order is set by which one comes first
        int_idx = arg_type.index('int')
        float_idx = arg_type.index('float')
        handles = (int, float) if int_idx < float_idx else (float, int)
        output_type_handle = _generic_assert_type(
                arg, name, handles, 'float or int', type_casting_ok)
    elif 'int' in arg_type:
        output_type_handle = _generic_assert_type(
                arg, name, int, 'int', type_casting_ok)
    elif 'float' in arg_type:
        output_type_handle = _generic_assert_type(
                arg, name, float, 'float', type_casting_ok)
    
    # Check other types
    elif 'str' in arg_type:
        output_type_handle = _generic_assert_type(
                arg, name, str, 'string', type_casting_ok)
    elif 'bool' in arg_type:
        output_type_handle = _generic_assert_type(
                arg, name, bool, 'boolean', type_casting_ok)

    # Unknown type requirement
    else:
        print(f"Unknown arg type!")
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

    # Assertions all passed. Return the output type handle.
    # This will be useful only if type casting is allowed.
    return output_type_handle if type_casting_ok else None


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


    def check_add_kwarg(self, name, default=None, arg_type=None, force=False):
        return check_add_kwarg(self.kwargs, name, 
                default=default, arg_type=arg_type, force=force)


    def check_kwarg(self, name, default=None, arg_type=None, required=False, pop=False):
        return check_kwarg(self.kwargs, name,
                default=default, arg_type=arg_type, 
                required=required, pop=pop)


