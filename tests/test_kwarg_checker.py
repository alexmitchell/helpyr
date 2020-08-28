#!/usr/bin/env python3

# To get html coverage report:
# >>> pytest --cov-report html[:html_dir_name]
#            --cov[=project_name] 
#            [output_dir]

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


class TestAssertTypes:

    @pytest.mark.parametrize("val, arg_type", [
    # parameters: val arg_type
        # Check basic vars
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
        (True, 'bool'),

        # Check some lists or tuples
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
    def test__assert_types_passing(self, val, arg_type):
        """Make sure _assert_types returns empty (as opposed raising an 
        error)."""
        assert _assert_types(val, arg_type=arg_type) is None


    @pytest.mark.parametrize("val, arg_type", [
    # parameters: val, arg_type
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
        (None, 'bool'),  # Not a bool
        (1, 'bool'),     # Not a bool
        ('abc', 'bool'), # Not a bool

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
        
        # Check some type casting
        ('abc', 'float_tcast'),
        ('abc', 'int_tcast'),
        ('abc',   'int_float_tcast'),
        ])
    def test__assert_types_AssertionError(self, val, arg_type):
        with pytest.raises(AssertionError):
            _assert_types(val, arg_type=arg_type)


    @pytest.mark.parametrize("val, arg_type, error_type", [
    # parameters: val, arg_type, error_type
        (1234, 'new-type', NotImplementedError), # arbitrary type not allowed
        ])
    def test__assert_types_other_errors(self, val, arg_type, error_type):
        with pytest.raises(error_type):
            _assert_types(val, arg_type=arg_type)


    @pytest.mark.parametrize("val, arg_type, type_out", [
    # parameters: val, arg_type, type_out

        # Check some type casting
        (1, 'float_tcast', float),
        ('1.0', 'float_tcast', float),
        (1.0, 'int_tcast', int),
        ('1', 'int_tcast', int),
        (True, 'int_tcast', int),
        ('1',   'int_float_tcast', int),
        ('1.0', 'int_float_tcast', float),
        ('1',   'float_int_tcast', float),
        ('1.0', 'float_int_tcast', float),
        (1, 'str_tcast', str),
        (1, 'bool_tcast', bool),
        ((1,2,3), 'tuple-float-tcast', [float, float, float]),
        ((1.0,2.0,3.0), 'tuple-int-tcast', [int, int, int]),
        (('1','2','3.0'), 'tuple-int-float-tcast', [int, int, float]),
        ])
    def test__assert_types_casting_ouput_passing(self, val, arg_type, type_out):
        """Make sure _assert_types returns empty (as opposed raising an 
        error)."""
        out = _assert_types(val, arg_type=arg_type)
        if isinstance(out, (list, tuple)):
            for element, element_out in zip(out, type_out):
                assert element is element_out
        else:
            assert out is type_out




@pytest.fixture
def simple_input_kwargs():
    return {
            'a' : 0,
            'b' : 1,
            'c' : 'hello world!',
            'd' : None,
            'e' : float('nan'),
            }
@pytest.fixture
def tcasting_input_kwargs():
    return {
            'a': 1,
            'b': '1.0',
            'c': 1.0,
            'd': '1',
            'e': True,
            'f': '1',
            'g': '1.0',
            'h': '1',
            'i': '1.0',
            'j': 1,
            'k': 1,
            'l': (1,2,3),
            'm': (1.0,2.0,3.0),
            'n': ('1','2','3.0'),
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
        _assert_equal(
                check_kwarg(simple_input_kwargs, simple_key, pop=True),
                simple_val)
        assert simple_key not in simple_input_kwargs


    @pytest.mark.parametrize("key, val, arg_type, val_type", [
    # parameters: key, val, arg_type, val_type

        # Check some type casting
        ('a', 1.0, 'float_tcast', float),
        ('b', 1.0, 'float_tcast', float),
        ('c', 1, 'int_tcast', int),
        ('d', 1, 'int_tcast', int),
        ('e', 1, 'int_tcast', int),
        ('f', 1, 'int_float_tcast', int),
        ('g', 1.0, 'int_float_tcast', float),
        ('h', 1.0, 'float_int_tcast', float),
        ('i', 1.0, 'float_int_tcast', float),
        ('j', '1', 'str_tcast', str),
        ('k', True, 'bool_tcast', bool),
        ('l', (1.0,2.0,3.0), 'tuple-float-tcast', [float, float, float]),
        ('m', (1,2,3), 'tuple-int-tcast', [int, int, int]),
        ('n', (1,2,3.0), 'tuple-int-float-tcast', [int, int, float]),
        ])
    def test_type_casting(self, tcasting_input_kwargs, key, val, 
            arg_type, val_type):
        """Make sure check_kwarg returns the proper values and types for given 
        type castings."""

        out = check_kwarg(tcasting_input_kwargs, key, arg_type=arg_type)

        if isinstance(val_type, (list, tuple)):
            assert isinstance(out, (list, tuple))
            assert isinstance(val, (list, tuple)) # Doesn't hurt....
            for out_i, val_i, val_i_type in zip(out, val, val_type):
                _assert_equal(out_i, val_i)
                assert type(out_i) is type(val_i) is val_i_type
        else:
            _assert_equal(out, val)
            assert type(out) is type(val) is val_type



class TestCheckAddKwarg:
    """Test check_add_kwarg."""

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
                check_add_kwarg(simple_input_kwargs, simple_key),
                simple_val
                )

    @pytest.mark.parametrize(*simple_io_args)
    def test_default_provided_keys(self, simple_input_kwargs, simple_key, simple_val):
        """Check that keys in the kwargs don't use the default value if not 
        forced."""
        _assert_equal(
                check_add_kwarg(simple_input_kwargs, simple_key, 
                    default='default'),
                simple_val
                )

    @pytest.mark.parametrize(*simple_io_args)
    def test_default_forced_keys(self, simple_input_kwargs, simple_key, simple_val):
        """Check that keys in the kwargs use the default value when forced and 
        updates the kwargs."""
        _assert_equal(
                check_add_kwarg(simple_input_kwargs, simple_key, 
                    default='default', force=True),
                'default'
                )
        _assert_equal(simple_input_kwargs[simple_key], 'default')

    def test_missing_key(self, simple_input_kwargs):
        """Check that a missing key uses the default value and that the 
        missing key is added to the kwargs.
        """
        _assert_equal(
                check_add_kwarg(simple_input_kwargs, 'missing_key'),
                None
                )
        assert 'missing_key' in simple_input_kwargs

    def test_default_missing_key(self, simple_input_kwargs):
        """Check that a missing key uses the default value and that the 
        missing key is added to the kwargs.
        """
        # Redundant test? Same as test_missing_key?
        _assert_equal(
                check_add_kwarg(simple_input_kwargs, 'missing_key', 
                    default='default'),
                'default'
                )
        assert 'missing_key' in simple_input_kwargs


    @pytest.mark.parametrize("key, val, arg_type, val_type", [
    # parameters: key, val, arg_type, val_type

        # Check some type casting
        ('a', 1.0, 'float_tcast', float),
        ('b', 1.0, 'float_tcast', float),
        ('c', 1, 'int_tcast', int),
        ('d', 1, 'int_tcast', int),
        ('e', 1, 'int_tcast', int),
        ('f', 1, 'int_float_tcast', int),
        ('g', 1.0, 'int_float_tcast', float),
        ('h', 1.0, 'float_int_tcast', float),
        ('i', 1.0, 'float_int_tcast', float),
        ('j', '1', 'str_tcast', str),
        ('k', True, 'bool_tcast', bool),
        ('l', (1.0,2.0,3.0), 'tuple-float-tcast', [float, float, float]),
        ('m', (1,2,3), 'tuple-int-tcast', [int, int, int]),
        ('n', (1,2,3.0), 'tuple-int-float-tcast', [int, int, float]),
        ])
    def test_type_casting(self, tcasting_input_kwargs, key, val, 
            arg_type, val_type):
        """Make sure check_kwarg returns the proper values and types for given 
        type castings."""

        out = check_add_kwarg(tcasting_input_kwargs, key, arg_type=arg_type)

        if isinstance(val_type, (list, tuple)):
            assert isinstance(out, (list, tuple))
            assert isinstance(val, (list, tuple)) # Doesn't hurt....
            for out_i, val_i, val_i_type in zip(out, val, val_type):
                _assert_equal(out_i, val_i)
                assert type(out_i) is type(val_i) is val_i_type
        else:
            _assert_equal(out, val)
            assert type(out) is type(val) is val_type



class TestGetFus:
    """Test get_check_kwarg_fu and get_check_add_kwarg_fu.

    How to test them?? These return a function handle, which I have no idea 
    how to compare for truth.

    These functions are so simple anyway....
    """
    pass

class TestKwargChecker:
    """Test the KwargChecker class.
    I don't really use the KwargChecker class anymore... Use at your own risk, 
    or write tests for it."""

    pass
