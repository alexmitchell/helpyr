#!/usr/bin/env python3

import pytest
from numpy import ndarray
from helpyr.kwarg_checker import check_kwarg
from helpyr.kwarg_checker import get_check_kwarg_fu
from helpyr.kwarg_checker import check_add_kwarg
from helpyr.kwarg_checker import get_check_add_kwarg_fu
from helpyr.kwarg_checker import KwargChecker
from helpyr.kwarg_checker import _assert_types

def _assert_equal(a, b):
    """Check if two arbitrary variables are equal.

    This turns out to be a more difficult problem than anticipated. Therefore, 
    the current version only does basic equality test. It does not handle lists 
    with nans or numpy ndarrays. This will need more work.
    """

    #if all([isinstance(var, (list, tuple, ndarray)) for var in [a,b]]):
    #    # Both variables are array_like
    
    # Check normal conditions
    # 'a == b' handles most things (ints, floats, strings, lists without nans, 
    # dicts, etc.)
    # 'is' checks if ids are equal (None)
    # 'a != a and b != b' check if they are nans
    #normal_isequal = \
    #           (a == b)           \
    #        or (a is b)           \
    #        or (a != a and b != b)
    #if not normal_isequal:
    #    # Either a mismatch or maybe a numpy 
    #try:
    #    # Try numpy equality in case it is a list of some sort
    #    # Handles NaNs
    #    np_allclose(a,b, equal_nan=True)
    #        or np_

    # 'a == b' handles most things (ints, floats, strings, lists without nans, 
    # dicts, etc.)
    # 'is' checks if ids are equal (None)
    # 'a != a and b != b' check if they are nans
    assert (a == b) or (a is b) or (a != a and b != b)

@pytest.mark.parametrize("val, arg_type", [
    ('anything', None), # No type requirements
    (None, 'int_none'), # numeric type and None allowed
    (None, 'float_none'), #  numeric type and None allowed
    (None, 'int_float_none'), # numeric type and None allowed
    (None, 'str_none'), # string type and None allowed
    (None, 'arbitrary_none'), # arbitrary type and None allowed
    (1, 'int'),
    (1.0, 'float'),
    (1, 'int_float'), # can be an int or float
    (1.0, 'int_float'), # can be an int or float
    (1, 'int_pos'),
    (0, 'int_whole'),
    (-1, 'int_neg'),
    (1.0, 'float_pos'),
    (0.0, 'float_whole'),
    (-1.0, 'float_neg'),
    ('abc', 'str'),
    ([], 'list'),
    ([1,2,3], 'list'),
    ([1,2,3], 'list-int'),
    ([1.0,2.0,3.0], 'list-float'),
    (list('abc'), 'list'),
    (list('abc'), 'list-str'),
    ((1,2,3), 'tuple'),
    ((1,2,3), 'tuple-int'),
    ((1.0,2.0,3.0), 'tuple-float'),
    (tuple('abc'), 'tuple'),
    (tuple('abc'), 'tuple-str'),
    ])
def test__assert_types_passing(val, arg_type):
    """Make sure _assert_types returns empty (as opposed raising an error)."""
    assert _assert_types(val, arg_type=arg_type) is None

@pytest.mark.parametrize("val, arg_type", [
    (None, 'int'),       # Can't be None
    (None, 'float'),     # Can't be None
    (None, 'int_float'), # Can't be None
    (None, 'str'),       # Can't be None
    (None, 'arbitrary'), # Can't be None
    (1.0, 'int'), # Must be a int
    (1, 'float'), # Must be a float
    ([], 'int_float'),    # Must be a int or float
    ('abc', 'int_float'), # Must be a int or float
    (0, 'int_pos'),        # Wrong sign
    (-1, 'int_whole'),     # Wrong sign
    (1, 'int_neg'),        # Wrong sign
    (0.0, 'float_pos'),    # Wrong sign
    (-1.0, 'float_whole'), # Wrong sign
    (1.0, 'float_neg'),    # Wrong sign
    (1, 'str'), # Not a string
    (123, 'list'),    # Not a list
    ('abc', 'list'),  # Not a list
    ((), 'list'),     # Not a list
    (123, 'tuple'),   # Not a tuple
    ('abc', 'tuple'), # Not a tuple
    ([], 'tuple'),    # Not a tuple
    ([1,2,3], 'list-float'),     # Wrong element type
    ([1.0,2.0,3.0], 'list-int'), # Wrong element type
    ((1,2,3), 'tuple-float'),     # Wrong element type
    ((1.0,2.0,3.0), 'tuple-int'), # Wrong element type
    ])
def test__assert_types_AssertionError(val, arg_type):
    with pytest.raises(AssertionError):
        _assert_types(val, arg_type=arg_type)

@pytest.mark.parametrize("val, arg_type, error_type", [
    (1234, 'new-type', NotImplementedError), # arbitrary type not allowed
    ])
def test__assert_types_other_errors(val, arg_type, error_type):
    with pytest.raises(error_type):
        _assert_types(val, arg_type=arg_type)


@pytest.fixture
def simple_input_kwargs():
    return {
            'a' : 0,
            'b' : 1,
            'c' : 'hello world!',
            'd' : None,
            'e' : float('nan'),
            }
class TestCheckKwarg:
    """Test check_kwarg."""

    simple_io_args = ("simple_key, simple_val", [
        ('a', 0),
        ('b', 1),
        ('c', 'hello world!'),
        ('d', None),
        ('e', float('nan')),
        ])

    @pytest.mark.parametrize(*simple_io_args)
    def test_simple(self, simple_input_kwargs, simple_key, simple_val):
        """Check that keys in kwargs return the values."""
        _assert_equal(
                check_kwarg(simple_input_kwargs, simple_key),
                simple_val
                )

    @pytest.mark.parametrize(*simple_io_args)
    def test_default_provided_keys(self, simple_input_kwargs, simple_key, simple_val):
        """Check that keys in the kwargs don't use the default value."""
        _assert_equal(
                check_kwarg(simple_input_kwargs, simple_key, 
                    default='default'),
                simple_val
                )

    def test_default_missing_keys(self, simple_input_kwargs):
        """Check that missing keys do use the default value."""
        _assert_equal(
                check_kwarg(simple_input_kwargs, 'missing_key', 
                    default='default'),
                'default'
                )

    def test_default_missing_keys(self, simple_input_kwargs):
        """Check that missing keys do use the default value."""
        _assert_equal(
                check_kwarg(simple_input_kwargs, 'missing_key', 
                    default='default'),
                'default'
                )

    def test_required(self, simple_input_kwargs):
        """Check that a required missing keys raise an AssertionError."""
        with pytest.raises(AssertionError):
            check_kwarg(simple_input_kwargs, 'missing_key',
                    required=True)

    @pytest.mark.parametrize(*simple_io_args)
    def test_pop(self, simple_input_kwargs, simple_key, simple_val):
        """Check that pop actually removes and returns kwarg."""
        val = check_kwarg(simple_input_kwargs, simple_key, pop=True)
        _assert_equal(val, simple_val)
        assert simple_key not in simple_input_kwargs


class TestCheckAddKwarg:
    """Test check_add_kwarg."""
    simple_io_args = ("simple_key, simple_val", [
        ('a', 0),
        ('b', 1),
        ('c', 'hello world!'),
        ('d', None),
        ('e', float('nan')),
        ])

    #def test_

class TestGetFus:
    """Test get_check_kwarg_fu and get_check_add_kwarg_fu."""
    pass

class TestKwargChecker:
    """Test the KwargChecker class."""
    pass
