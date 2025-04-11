#!/usr/bin/env python3
# coding=utf-8

"""
Utility methods for error specifications.
"""


from typing import Any


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
