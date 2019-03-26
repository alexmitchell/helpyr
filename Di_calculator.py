#!/usr/bin/env python3
import numpy as np
import pandas as pd

def calc_Di(data, target_Di=50):
    # Calculate the Di values for a dataframe of sieve masses
    # data should be a dataframe of raw masses per size class (size sorted 
    # smallest to largest)
    # target_Di is an integer between 0 and 100 (string like 'D50' okay too)
    # 
    # returns series

    if isinstance(target_Di, str):
        target_Di = int(target_Di[1:])

    assert(0 < target_Di < 100)
    target = target_Di/100
    name = f"D{target_Di}"

    notnull_idx = data.notnull().all(axis=1)
    raw_data = data
    data = data.loc[notnull_idx, :]
    # Calculate cumulative curve and normalize
    cumsum = data.cumsum(axis=1)
    notnull_fractional = cumsum.divide(cumsum.iloc[:, -1], axis=0)

    # Make sure the target falls between datapoints on the distribution
    fines_okay = (notnull_fractional < target).any(axis=1)
    coarse_okay = (notnull_fractional > target).any(axis=1)
    okay_rows = fines_okay & coarse_okay
    fractional = notnull_fractional.loc[okay_rows, :]

    # interpolate the percentile
    # I CANNOT find a cleaner way to do this... Definitely not in Pandas.
    np_frac = fractional.values
    np_cols = fractional.columns.values

    np_equal = np_frac == target

    np_lesser = np_frac < target
    np_rlesser = np.roll(np_lesser, -1, axis=1)
    np_lower = np_lesser & ~np_rlesser # find True w/ False to right

    np_greater = np_frac > target
    np_rgreater = np.roll(np_greater, 1, axis=1)
    np_upper = np_greater & ~np_rgreater # find True w/ False to left

    lower_frac = np_frac[np_lower]
    upper_frac = np_frac[np_upper]
    lower = np_cols[np.argmax(np_lower, axis=1)] # lower size classes
    upper = np_cols[np.argmax(np_upper, axis=1)] # upper size classes
    equal = np_cols[np.argmax(np_equal, axis=1)] # equal size class
    equal_rows = np_equal.any(axis=1)

    lower_psi = np.log2(lower)
    upper_psi = np.log2(upper)

    Di_psi = lower_psi + (target - lower_frac) * (upper_psi - lower_psi) /\
                        (upper_frac - lower_frac)
    Di = 2**Di_psi
    Di[equal_rows] = equal[equal_rows]

    # Add the null values back in to make the array the same size
    notnull_fractional.loc[okay_rows, name] = Di
    out = pd.Series(index=raw_data.index, name=name)
    out.loc[notnull_idx] = notnull_fractional[name]

    return out

