#!/usr/bin/env python3
# coding=utf-8

"""
Constants related to errors.
"""

from vt.utils.errors.error_specs.error_codes import *

type_name_map: dict[type, str] = {
    str: 'a string',
    int: 'an int',
    float: 'a float',
    bool: 'a boolean'
}
