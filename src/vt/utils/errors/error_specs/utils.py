#!/usr/bin/env python3
# coding=utf-8

"""
Utility methods for error specifications.
"""


import warnings
from typing import Any
import inspect

from vt.utils.errors.warnings import vt_warn


def form_errmsg_for_choices(emphasis: str | None = None, choices: list[Any] | None = None) -> str:
    """
    Create a sensible error message with more context when a value is provided unexpectedly.

    Examples::

    >>> form_errmsg_for_choices()
    'Unexpected value.'

    >>> form_errmsg_for_choices('verbosity')
    'Unexpected verbosity value.'

    >>> form_errmsg_for_choices(choices=['v', 'vv', 'vvv'])
    "Unexpected value. Choose from ['v', 'vv', 'vvv']."

    >>> form_errmsg_for_choices('quietness', ['q', 'qq', 'qqq'])
    "Unexpected quietness value. Choose from ['q', 'qq', 'qqq']."

    :param emphasis: the string which is emphasised in the returned error message. The emphasising of string is not
        done if this value is ``None`` or not provided.
    :param choices: all the acceptable choices. Choices are not included in the error message if this value is ``None``
        or not supplied.
    :return: The formed errmsg string.
    """
    if emphasis:
        errmsg = f"Unexpected {emphasis} value."
    else:
        errmsg = "Unexpected value."
    if choices:
        errmsg = f"{errmsg} Choose from {choices}."
    return errmsg


def not_allowed_together(*args: Any | None, __err: bool = True, __truthy: bool = False,
                         __fmt: str = "{category}: {message}\n",
                         **name_overrides: str | None):
    """
    Raise an error or warning if all provided positional arguments are not ``None`` or falsy.

    This utility is designed to ensure that a group of arguments *cannot* be used together.
    If all of them are provided (i.e., __truthy) or not ``None``, a ``ValueError`` or ``UserWarning`` is raised/emitted.

    :param args: The arguments to check. Only truthy arguments are considered "provided" if ``__truthy`` is ``True``
        else ``non-None`` areguments are considered "provided".
    :param __truthy: Check for arguments being truthy instead of ``None``.
    :param __err: If ``True``, raise a ``ValueError`` when all arguments are truthy (or not ``None``).
        If ``False``, emits a ``UserWarning`` instead.
    :param __fmt: format in which the warning will be raised. See ``vt_warn()`` for more details.
        Only relevant if ``__err`` is ``False``.
    :param name_overrides: Optional keyword arguments to rename argument labels in the error message.
            Provide the argument as keyword with the original name and new string name as value. e.g.
            ``not_allowed_together(a, b, b="no_b")`` will show "'a' and 'no_b'" in the message.

    :raise UserWarning: If all provided arguments are truthy (or not ``None``) and ``__err`` is ``False``.
    :raise ValueError: If all provided arguments are truthy (or not ``None``) and ``__err`` is ``True``.

    Examples
    --------
    >>> import contextlib
    >>> import sys
    >>> a = 1
    >>> b = 2
    >>> not_allowed_together(a, b)
    Traceback (most recent call last):
    ...
    ValueError: 'a' and 'b' are not allowed together

    >>> with warnings.catch_warnings():
    ...     with contextlib.redirect_stderr(sys.stdout):
    ...         not_allowed_together(a, b, b="param_b", __err=False)
    UserWarning: 'a' and 'param_b' are not allowed together

    >>> not_allowed_together(None, b) # No error

    >>> not_allowed_together(0, None) # No error

    >>> a = "A"
    >>> b = "B"
    >>> c = "C"
    >>> not_allowed_together(a, b, c)
    Traceback (most recent call last):
    ...
    ValueError: 'a', 'b', and 'c' are not allowed together

    >>> not_allowed_together(a, b, c, a="X", c="Z")
    Traceback (most recent call last):
    ...
    ValueError: 'X', 'b', and 'Z' are not allowed together

    >>> b = {}
    >>> not_allowed_together(a, {}, c, __truthy=True) # no error as not all args are truthy ({}, 2nd arg)

    >>> not_allowed_together(a, b, c) # err as b is not None and __truthy is defaulted to False.
    Traceback (most recent call last):
    ...
    ValueError: 'a', 'b', and 'c' are not allowed together
    """

    # Get argument names (best-effort using stack)
    frame = inspect.currentframe().f_back
    arg_names = [name for name, val in frame.f_locals.items() if val in args]

    # Use name overrides if provided
    for i, name in enumerate(arg_names):
        if name in name_overrides:
            arg_names[i] = name_overrides[name]

    valid = all(args) if __truthy else all(arg is not None for arg in args)
    if valid:
        # Format names nicely
        if len(arg_names) > 2:
            formatted = "', '".join(arg_names[:-1])
            msg = f"'{formatted}', and '{arg_names[-1]}' are not allowed together"
        else:
            msg = f"'{arg_names[0]}' and '{arg_names[1]}' are not allowed together"

        if __err:
            raise ValueError(msg)
        else:
            vt_warn(msg, fmt=__fmt, stack_level=3)


def at_least_one_required(*args: Any | None, __err: bool = True, __truthy: bool = False,
                          __fmt: str = "{category}: {message}\n",
                          **name_overrides: str | None):
    """
    Raise an error or warning if none of the provided arguments are present.

    This utility ensures that *at least one* of the provided arguments is given.
    Arguments are considered "provided" based on the ``__truthy`` flag:
    if ``__truthy=True``, then values like ``0``, ``''``, ``[]`` are considered missing;
    if ``__truthy=False``, only ``None`` is considered missing.

    :param args: The arguments to validate.
    :param __truthy: If ``True``, treats only truthy values as present.
                     If ``False``, any value except ``None`` is treated as present.
    :param __err: If ``True``, raises a ``ValueError`` if no arguments are provided.
                  If ``False``, emits a ``UserWarning`` instead.
    :param __fmt: Message format used in case of warning. Has no effect when ``__err=True``.
    :param name_overrides: Optional mapping of original variable names to custom display names
                           for the error/warning message.

    :raises ValueError: When no arguments are present and ``__err=True``.
    :raises UserWarning: When no arguments are present and ``__err=False``.

    Examples
    --------
    >>> a = None
    >>> b = None
    >>> at_least_one_required(a, b)
    Traceback (most recent call last):
    ...
    ValueError: At least one of 'a' or 'b' is required

    >>> a = None
    >>> b = 42
    >>> at_least_one_required(a, b)  # Valid: b is not None

    >>> a = 0
    >>> b = ""
    >>> at_least_one_required(a, b, __truthy=False)  # Valid: both are not None

    >>> at_least_one_required(a, b, __truthy=True)  # Error: both falsy
    Traceback (most recent call last):
    ...
    ValueError: At least one of 'a' or 'b' is required

    >>> a = "value"
    >>> b = ""
    >>> at_least_one_required(a, b, __truthy=True)  # Valid: a is truthy

    >>> import contextlib, sys
    >>> a = None
    >>> b = None
    >>> with warnings.catch_warnings():
    ...     with contextlib.redirect_stderr(sys.stdout):
    ...         at_least_one_required(a, b, __err=False)
    UserWarning: At least one of 'a' or 'b' is required

    >>> a = None
    >>> b = None
    >>> at_least_one_required(a, b, __err=True, a="first", b="second")
    Traceback (most recent call last):
    ...
    ValueError: At least one of 'first' or 'second' is required

    >>> a = 1
    >>> at_least_one_required(a)  # Only one argument, valid

    >>> at_least_one_required(None)  # Only one, None -> error
    Traceback (most recent call last):
    ...
    ValueError: 'a' is required

    >>> at_least_one_required(0, __truthy=False)  # Valid: not None

    >>> at_least_one_required(0, __truthy=True)  # Invalid: 0 is falsy
    Traceback (most recent call last):
    ...
    ValueError: 'a' is required
    """
    # Best-effort name detection
    frame = inspect.currentframe().f_back
    arg_names = [name for name, val in frame.f_locals.items() if val in args]

    # Apply overrides
    for i, name in enumerate(arg_names):
        if name in name_overrides:
            arg_names[i] = name_overrides[name]

    # Determine presence
    valid = any(args) if __truthy else any(arg is not None for arg in args)

    if not valid:
        # Message formatting
        if len(arg_names) > 2:
            formatted = "', '".join(arg_names[:-1])
            msg = f"At least one of '{formatted}', or '{arg_names[-1]}' is required"
        elif len(arg_names) == 2:
            msg = f"At least one of '{arg_names[0]}' or '{arg_names[1]}' is required"
        elif len(arg_names) == 1:
            msg = f"'{arg_names[0]}' is required"
        else:
            msg = "At least one required argument must be provided"

        if __err:
            raise ValueError(msg)
        else:
            vt_warn(msg, fmt=__fmt, stack_level=3)
