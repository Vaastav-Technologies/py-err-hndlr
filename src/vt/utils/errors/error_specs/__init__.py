#!/usr/bin/env python3
# coding=utf-8

"""
Inclusive library for error handling.
"""

from vt.utils.errors.error_specs.__constants__ import *
from vt.utils.errors.error_specs.errmsg import ErrorMsgFormer, ErrorMessageFormer
from vt.utils.errors.error_specs.base import DefaultOrError, DefaultNoError, WarningWithDefault, \
    StrictWarningWithDefault
