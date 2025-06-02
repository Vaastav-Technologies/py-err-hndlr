#!/usr/bin/env python3
# coding=utf-8

"""
Utility methods for error specifications.
"""

from typing import Any, Literal


class ErrorMessageFormer:
    """
    Use ``ErrorMsgFormer`` global stateless object instead of directly instantiating this class.

    A configurable utility class for generating structured and reusable error messages for validation.

    This class supports Oxford comma usage, conjunction word changes
    (e.g., replacing "and"/"or" with localized alternatives), and suffix formatting. It is intended
    to be subclassed or cloned via `clone_with()` for further customization.

    Example::

        >>> ErrorMsgFormer.not_allowed_together('a', 'b')
        'a and b are not allowed together'

        >>> ErrorMsgFormer.clone_with(use_oxford_comma=True).all_required('a', 'b', 'c')
        'All a, b, and c are required'
    """

    def __init__(
            self,
            use_oxford_comma: bool = False,
            conjunctions: dict[str, str] | None = None
    ):
        """
        :param use_oxford_comma: Whether to use an Oxford comma before the final conjunction.
        :param conjunctions: A mapping like {'and': 'and', 'or': 'or'} to customize conjunctions.
        """
        self.use_oxford_comma = use_oxford_comma
        self.conjunctions = conjunctions or {"and": "and", "or": "or"}

    def _join_args(self, items: list[str], conj_type: Literal["and", "or"], surround_item: str = "") -> str:
        """
        Helper to join a list of arguments using the correct conjunction and comma rules.

        :param items: List of argument names.
        :param conj_type: The type of conjunction to use ('and' or 'or').
        :param surround_item: surround each item with the given string.
        :return: Formatted string of argument names joined by the conjunction.
        :raises KeyError: If the provided conjunction type is not in ``self.conjunctions``."""
        conjunction = self.conjunctions.get(conj_type, conj_type)
        if surround_item:
            items = [f"{surround_item}{item}{surround_item}" for item in items]
        if len(items) == 2:
            return f"{items[0]} {conjunction} {items[1]}"
        elif len(items) > 2:
            comma = "," if self.use_oxford_comma else ""
            return f"{', '.join(items[:-1])}{comma} {conjunction} {items[-1]}"
        else:
            return items[0]

    def not_allowed_together(self, first_arg: str, second_arg: str, *args: str,
                             prefix: str = "", suffix: str = "",
                             _prefix: str = "", _suffix: str = " are not allowed together") -> str:
        """
        Builds and returns an error message for arguments that are not to be supplied together.

        Examples::

            >>> ErrorMsgFormer.not_allowed_together('a', 'b')
            'a and b are not allowed together'

            >>> ErrorMsgFormer.not_allowed_together('a', 'b', 'c')
            'a, b and c are not allowed together'

        Append a string to formed error message, using ``suffix``::

            >>> ErrorMsgFormer.not_allowed_together('a', 'b', suffix=' when c is provided.')
            'a and b are not allowed together when c is provided.'

        Append a string to unformed error message, using ``_suffix``::

            >>> ErrorMsgFormer.not_allowed_together('a', 'b', _suffix=' together nay.')
            'a and b together nay.'

        Prepend a string to formed error message, using ``prefix``::

            >>> ErrorMsgFormer.not_allowed_together('a', 'b', 'c', prefix='Invalid: ')
            'Invalid: a, b and c are not allowed together'

        Prepend a string to unformed error message, using ``_prefix``::

            >>> ErrorMsgFormer.not_allowed_together('a', 'b', 'c', prefix='Invalid: ',  _prefix='TOGETHER-FAIL: ')
            'Invalid: TOGETHER-FAIL: a, b and c are not allowed together'

        Errmsg formation sequenceing -> ``{prefix}{_prefix}{<formed-errmsg>}{_suffix}{suffix}``

        :param first_arg: The first argument name.
        :param second_arg: The second argument name.
        :param args: Additional argument names.
        :param prefix: The string to prepend to the formed error message.
        :param suffix: The string to append to the formed error message.
        :param _prefix: The string to prepend to the internal unformed error message.
        :param _suffix: The string to append to the internal unformed error message.
        :return: Error message string.
        :raises KeyError: If 'and' conjunction is missing from configuration.
        """
        all_args = [first_arg, second_arg, *args]
        return f"{prefix}{_prefix}{self._join_args(all_args, 'and')}{_suffix}{suffix}"

    def at_least_one_required(self, first_arg: str, second_arg: str, *args: str,
                              prefix: str = "", suffix: str = "",
                              _prefix: str = "", _suffix: str = " is required") -> str:
        """
        Builds and returns an error message indicating that at least one of the arguments is required.

        Examples::

            >>> ErrorMsgFormer.at_least_one_required('a', 'b')
            'Either a or b is required'

            >>> ErrorMsgFormer.at_least_one_required('a', 'b', 'c')
            'Either a, b or c is required'

        Append a string to formed error message, using ``suffix``::

            >>> ErrorMsgFormer.at_least_one_required('a', 'b', suffix=' for compatibility.')
            'Either a or b is required for compatibility.'

        Append a string to unformed error message, using ``_suffix``::

            >>> ErrorMsgFormer.at_least_one_required('a', 'b', _suffix=' is necessary.')
            'Either a or b is necessary.'

        Prepend a string to formed error message, using ``prefix``::

            >>> ErrorMsgFormer.at_least_one_required('x', 'y', prefix='Missing: ')
            'Missing: Either x or y is required'

        Prepend a string to unformed error message, using ``_prefix``::

            >>> ErrorMsgFormer.at_least_one_required('x', 'y', 'z', _prefix='Please note: ')
            'Please note: Either x, y or z is required'

        Combine ``prefix`` and ``_prefix``::

            >>> ErrorMsgFormer.at_least_one_required('x', 'y', 'z', prefix='ALERT: ', _prefix='NOTE: ')
            'ALERT: NOTE: Either x, y or z is required'

        Combine ``_suffix`` and ``suffix``::

            >>> ErrorMsgFormer.at_least_one_required('x', 'y', _suffix=' must be set', suffix=' to continue.')
            'Either x or y must be set to continue.'

        Use all controls together::

            >>> ErrorMsgFormer.at_least_one_required('foo', 'bar', 'baz',
            ...     prefix='Required: ', _prefix='Warning! ', _suffix=' is critical', suffix=' for execution.')
            'Required: Warning! Either foo, bar or baz is critical for execution.'

        Errmsg formation sequenceing -> ``{prefix}{_prefix}Either {<joined-args>}{_suffix}{suffix}``


        :param first_arg: The first argument name.
        :param second_arg: The second argument name.
        :param args: Additional argument names.
        :param prefix: The string to prepend to the formed error message.
        :param suffix: The string to append to the formed error message.
        :param _prefix: The string to prepend to the internal unformed error message.
        :param _suffix: The string to append to the internal unformed error message.
        :return: Error message string.
        :raises KeyError: If 'or' conjunction is missing from configuration.
        """
        all_args = [first_arg, second_arg, *args]
        joined = self._join_args(all_args, "or")
        return f"{prefix}{_prefix}Either {joined}{_suffix}{suffix}"

    def all_required(self, first_arg: str, second_arg: str, *args: str,
                     prefix: str = "", suffix: str = "",
                     _prefix: str = "", _suffix: str = " are required") -> str:
        """
        Builds and returns an error message stating that all arguments must be supplied.

        Uses 'Both' for two items, 'All' for three or more.

        Examples::

            >>> ErrorMsgFormer.all_required('a', 'b')
            'Both a and b are required'

            >>> ErrorMsgFormer.all_required('a', 'b', 'c')
            'All a, b and c are required'

        Append a string to formed error message, using ``suffix``::

            >>> ErrorMsgFormer.all_required('a', 'b', suffix=' for initialization.')
            'Both a and b are required for initialization.'

            >>> ErrorMsgFormer.all_required('a', 'b', 'c', suffix=' to proceed.')
            'All a, b and c are required to proceed.'

        Append a string to unformed error message, using ``_suffix``::

            >>> ErrorMsgFormer.all_required('x', 'y', _suffix=' must be defined.')
            'Both x and y must be defined.'

            >>> ErrorMsgFormer.all_required('x', 'y', 'z', _suffix=' should be set')
            'All x, y and z should be set'

        Prepend a string to formed error message, using ``prefix``::

            >>> ErrorMsgFormer.all_required('foo', 'bar', prefix='Missing: ')
            'Missing: Both foo and bar are required'

            >>> ErrorMsgFormer.all_required('foo', 'bar', 'baz', prefix='Missing: ')
            'Missing: All foo, bar and baz are required'

        Prepend a string to unformed error message, using ``_prefix``::

            >>> ErrorMsgFormer.all_required('a', 'b', _prefix='Notice: ')
            'Notice: Both a and b are required'

            >>> ErrorMsgFormer.all_required('a', 'b', 'c', _prefix='Heads up: ')
            'Heads up: All a, b and c are required'

        Combine ``prefix`` and ``_prefix``::

            >>> ErrorMsgFormer.all_required('a', 'b', prefix='ALERT: ', _prefix='MANDATORY! ')
            'ALERT: MANDATORY! Both a and b are required'

            >>> ErrorMsgFormer.all_required('a', 'b', 'c', prefix='ALERT: ', _prefix='MANDATORY! ')
            'ALERT: MANDATORY! All a, b and c are required'

        Combine ``_suffix`` and ``suffix``::

            >>> ErrorMsgFormer.all_required('x', 'y', _suffix=' must exist', suffix=' to continue.')
            'Both x and y must exist to continue.'

            >>> ErrorMsgFormer.all_required('x', 'y', 'z', _suffix=' to be configured', suffix=' ASAP.')
            'All x, y and z to be configured ASAP.'

        Use all controls together::

            >>> ErrorMsgFormer.all_required('foo', 'bar', 'baz',
            ...     prefix='ERROR: ', _prefix='CRITICAL! ', _suffix=' are missing', suffix=' from the form.')
            'ERROR: CRITICAL! All foo, bar and baz are missing from the form.'

        Errmsg formation sequencing -> ``{prefix}{_prefix}{<formed-errmsg>}{_suffix}{suffix}``

        :param first_arg: The first argument name.
        :param second_arg: The second argument name.
        :param args: Additional argument names.
        :param prefix: The string to prepend to the formed error message.
        :param suffix: The string to append to the formed error message.
        :param _prefix: The string to prepend to the internal unformed error message.
        :param _suffix: The string to append to the internal unformed error message.
        :return: Error message string.
        :raises KeyError: If 'and' conjunction is missing from configuration.
        """
        all_args = [first_arg, second_arg, *args]
        keyword = "Both" if len(all_args) == 2 else "All"
        return f"{prefix}{_prefix}{keyword} {self._join_args(all_args, 'and')}{_suffix}{suffix}"

    def errmsg_for_choices(self, value: str = "value", emphasis: str | None = None,
                           choices: list[Any] | None = None,
                           prefix: str = "", suffix: str = "",
                           _prefix: str = "Unexpected ", _suffix: str = ".") -> str:
        """
        Builds and returns an error message providing more context when a value is unexpectedly given.

        Examples::

            >>> ErrorMsgFormer.errmsg_for_choices()
            'Unexpected value.'

            >>> ErrorMsgFormer.errmsg_for_choices(emphasis='verbosity')
            'Unexpected verbosity value.'

            >>> ErrorMsgFormer.errmsg_for_choices(choices=['low', 'high'])
            "Unexpected value. Choose from 'low' and 'high'."

            >>> ErrorMsgFormer.errmsg_for_choices(emphasis='color', choices=['red', 'green', 'blue'])
            "Unexpected color value. Choose from 'red', 'green' and 'blue'."

            >>> ErrorMsgFormer.errmsg_for_choices(emphasis='log level', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'FATAL'],
            ...     prefix="Undefined: ")
            "Undefined: Unexpected log level value. Choose from 'DEBUG', 'INFO', 'WARNING', 'ERROR' and 'FATAL'."

            >>> ErrorMsgFormer.errmsg_for_choices(value="'SUCCESS'", emphasis='log level', choices=['DEBUG', 'INFO',
            ...     'WARNING', 'ERROR', 'FATAL'], prefix="Undefined: ")
            "Undefined: Unexpected log level 'SUCCESS'. Choose from 'DEBUG', 'INFO', 'WARNING', 'ERROR' and 'FATAL'."

            >>> ErrorMsgFormer.errmsg_for_choices(value="'SUCCESS'", emphasis='log level', choices=['DEBUG', 'INFO',
            ...     'WARNING', 'ERROR', 'FATAL'], prefix="VAL-ERR: ", suffix=" Defaulting to 'WARNING'")
            "VAL-ERR: Unexpected log level 'SUCCESS'. Choose from 'DEBUG', 'INFO', 'WARNING', 'ERROR' and 'FATAL'. Defaulting to 'WARNING'"

        Append to unformed message using ``_suffix``::

            >>> ErrorMsgFormer.errmsg_for_choices(emphasis='color', choices=['red', 'green'], _suffix=' ❌')
            "Unexpected color value. Choose from 'red' and 'green' ❌"

        Prepend to unformed message using ``_prefix``::

            >>> ErrorMsgFormer.errmsg_for_choices(value='42', emphasis='mode', _prefix='INVALID! ')
            'INVALID! mode 42.'

            >>> ErrorMsgFormer.errmsg_for_choices(emphasis='log level', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'FATAL'],
            ...     prefix="Undefined ", _prefix='')
            "Undefined log level value. Choose from 'DEBUG', 'INFO', 'WARNING', 'ERROR' and 'FATAL'."

        Use all controls together::

            >>> ErrorMsgFormer.errmsg_for_choices(value='X', emphasis='log level',
            ...     choices=['DEBUG', 'INFO', 'WARNING'], prefix='ERROR: ', _prefix='[!] ',
            ...     _suffix=' ❌', suffix=' Please try again.')
            "ERROR: [!] log level X. Choose from 'DEBUG', 'INFO' and 'WARNING' ❌ Please try again."

        Errmsg formation sequencing -> ``{prefix}{_prefix}{<formed-msg>}{_suffix}{suffix}``

        :param value: The value to illustrate (e.g., user-supplied value).
        :param emphasis: A string to emphasize (e.g., 'color', 'log level').
        :param choices: Acceptable options to list.
        :param prefix: Prepended to the whole message.
        :param suffix: Appended to the whole message.
        :param _prefix: Prepended to the internal unformed error message.
        :param _suffix: Appended to the internal unformed error message.
        :return: The formed error message.
        """
        msg = f"{prefix}{_prefix}{emphasis + ' ' if emphasis else ''}{value}"
        if choices:
            msg += f". Choose from {self._join_args(choices, 'and', surround_item='\'')}"
        msg += f"{_suffix}{suffix}"
        return msg

    def clone_with(self,
                   use_oxford_comma: bool | None = None,
                   conjunctions: dict[str, str] | None = None) -> "ErrorMessageFormer":
        """
        Returns a new instance of ErrorMessageFormer with the given overrides.

        Examples::

            >>> custom = ErrorMsgFormer.clone_with(use_oxford_comma=False)
            >>> custom.not_allowed_together('a', 'b', 'c')
            'a, b and c are not allowed together'

            >>> custom = custom.clone_with(use_oxford_comma=True)
            >>> custom.not_allowed_together('a', 'b', 'c')
            'a, b, and c are not allowed together'

            >>> custom = custom.clone_with(conjunctions={'and': '--and--'})
            >>> custom.not_allowed_together('a', 'b', 'c')
            'a, b, --and-- c are not allowed together'

            Default conjuntion is picked-up if conjuntions are falsy empty-dict:

            >>> custom = custom.clone_with(conjunctions={})
            >>> custom.not_allowed_together('a', 'b', 'c')
            'a, b, --and-- c are not allowed together'
        """
        return ErrorMessageFormer(
            use_oxford_comma=use_oxford_comma if use_oxford_comma is not None else self.use_oxford_comma,
            conjunctions=conjunctions or self.conjunctions.copy()
        )

    def __repr__(self) -> str:
        return (f"<{self.__class__.__name__}("
                f"use_oxford_comma={self.use_oxford_comma}, "
                f"conjunctions={self.conjunctions})>")


ErrorMsgFormer = ErrorMessageFormer()
"""
A singleton, configurable, stateless instance for reusable validation error messages.

Import and use `ErrorMsgFormer` across your app. If you need a custom version,
use `.clone_with(...)` to generate a new instance.

Example::

    >>> from vt.utils.errors.error_specs import ErrorMsgFormer
    >>> ErrorMsgFormer.all_required('foo', 'bar')
    'Both foo and bar are required.'
"""
