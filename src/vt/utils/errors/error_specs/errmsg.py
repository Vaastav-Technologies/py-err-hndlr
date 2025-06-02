#!/usr/bin/env python3
# coding=utf-8

"""
Utility methods for error specifications.
"""

from typing import Any


class ErrorMessageFormer:
    """
    Use ``ErrorMsgFormer`` global stateless object instead of directly instantiating this class.

    A configurable utility class for generating structured and reusable error messages for validation.

    This class supports locale-style customization such as Oxford comma usage, conjunction word changes
    (e.g., replacing "and"/"or" with localized alternatives), and suffix formatting. It is intended
    to be subclassed or cloned via `clone_with()` for further customization.

    Example::

        >>> ErrorMsgFormer.not_allowed_together('a', 'b')
        'a and b are not allowed together.'

        >>> ErrorMsgFormer.clone_with(use_oxford_comma=True).all_required('a', 'b', 'c')
        'All a, b, and c are required.'
    """

    def __init__(
            self,
            locale: str = "en",
            use_oxford_comma: bool = False,
            conjunctions: dict[str, str] | None = None
    ):
        """
        :param locale: The locale for the message structure (currently placeholder).
        :param use_oxford_comma: Whether to use an Oxford comma before the final conjunction.
        :param conjunctions: A mapping like {'and': 'and', 'or': 'or'} to customize conjunctions.
        """
        self.locale = locale
        self.use_oxford_comma = use_oxford_comma
        self.conjunctions = conjunctions or {"and": "and", "or": "or"}

    def _join_args(self, items: list[str], conj_type: str, surround_item: str = "") -> str:
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
                             prefix: str = "", suffix: str = " are not allowed together.") -> str:
        """
        Builds and returns an error message for arguments that are not to be supplied together.

        Examples::

            >>> ErrorMsgFormer.not_allowed_together('a', 'b')
            'a and b are not allowed together.'

            >>> ErrorMsgFormer.not_allowed_together('a', 'b', 'c')
            'a, b and c are not allowed together.'

            >>> ErrorMsgFormer.not_allowed_together('a', 'b', suffix=' together nay.')
            'a and b together nay.'

            >>> ErrorMsgFormer.not_allowed_together('a', 'b', 'c', prefix='Invalid: ')
            'Invalid: a, b and c are not allowed together.'

        :param first_arg: The first argument name.
        :param second_arg: The second argument name.
        :param args: Additional argument names.
        :param prefix: The string to prepend to the error message.
        :param suffix: The string to append to the error message.
        :return: Error message string.
        :raises KeyError: If 'and' conjunction is missing from configuration.
        """
        all_args = [first_arg, second_arg, *args]
        return f"{prefix}{self._join_args(all_args, 'and')}{suffix}"

    def at_least_one_required(self, first_arg: str, second_arg: str, *args: str,
                              prefix: str = "", suffix: str = " is required.") -> str:
        """
        Builds and returns an error message indicating that at least one of the arguments is required.

        Examples::

            >>> ErrorMsgFormer.at_least_one_required('a', 'b')
            'Either a or b is required.'

            >>> ErrorMsgFormer.at_least_one_required('a', 'b', 'c')
            'Either a, b or c is required.'

            >>> ErrorMsgFormer.at_least_one_required('x', 'y', prefix='Missing: ')
            'Missing: Either x or y is required.'

        :param first_arg: The first argument name.
        :param second_arg: The second argument name.
        :param args: Additional argument names.
        :param prefix: The string to prepend to the message.
        :param suffix: The string to append to the message.
        :return: Error message string.
        :raises KeyError: If 'or' conjunction is missing from configuration.
        """
        all_args = [first_arg, second_arg, *args]
        joined = self._join_args(all_args, "or")
        return f"{prefix}Either {joined}{suffix}"

    def all_required(self, first_arg: str, second_arg: str, *args: str,
                     prefix: str = "", suffix: str = " are required.") -> str:
        """
        Builds and returns an error message stating that all arguments must be supplied.

        Uses 'Both' for two items, 'All' for three or more.

        Examples::

            >>> ErrorMsgFormer.all_required('a', 'b')
            'Both a and b are required.'

            >>> ErrorMsgFormer.all_required('a', 'b', 'c')
            'All a, b and c are required.'

            >>> ErrorMsgFormer.all_required('foo', 'bar', prefix='Missing: ')
            'Missing: Both foo and bar are required.'

        :param first_arg: The first argument name.
        :param second_arg: The second argument name.
        :param args: Additional argument names.
        :param prefix: The string to prepend to the message.
        :param suffix: The string to append to the message.
        :return: Error message string.
        :raises KeyError: If 'and' conjunction is missing from configuration.
        """
        all_args = [first_arg, second_arg, *args]
        keyword = "Both" if len(all_args) == 2 else "All"
        return f"{prefix}{keyword} {self._join_args(all_args, 'and')}{suffix}"

    def errmsg_for_choices(self, value: str= "value", emphasis: str | None = None, choices: list[Any] | None = None,
                           prefix: str = "Unexpected ", suffix: str = "") -> str:
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

            >>> ErrorMsgFormer.errmsg_for_choices(emphasis='log level', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR',
            ...     'FATAL'], prefix="Undefined ")
            "Undefined log level value. Choose from 'DEBUG', 'INFO', 'WARNING', 'ERROR' and 'FATAL'."

            >>> ErrorMsgFormer.errmsg_for_choices(value="'SUCCESS'", emphasis='log level', choices=['DEBUG', 'INFO',
            ...     'WARNING', 'ERROR', 'FATAL'], prefix="Undefined ")
            "Undefined log level 'SUCCESS'. Choose from 'DEBUG', 'INFO', 'WARNING', 'ERROR' and 'FATAL'."

            >>> ErrorMsgFormer.errmsg_for_choices(value="'SUCCESS'", emphasis='log level', choices=['DEBUG', 'INFO',
            ...     'WARNING', 'ERROR', 'FATAL'], prefix="Undefined ", suffix=" Defaulting to 'WARNING'")
            "Undefined log level 'SUCCESS'. Choose from 'DEBUG', 'INFO', 'WARNING', 'ERROR' and 'FATAL'. Defaulting to 'WARNING'"

        :param value: The value to show to illustrate the user that this maybe an invalid option.
        :param emphasis: the string which is emphasised in the returned error message. The emphasising of string is not
            done if this value is ``None`` or not provided.
        :param choices: all the acceptable choices. Choices are not included in the error message if this value
            is ``None`` or not supplied.
        :param prefix: The string to prepend to the message.
        :param suffix: The string to append to the message.
        :return: The formed errmsg string.
        """
        msg = f"{prefix}{emphasis + ' ' if emphasis else ''}{value}."
        if choices:
            msg += f" Choose from {self._join_args(choices, 'and', surround_item="'")}."
        msg += suffix
        return msg

    def clone_with(self, **kwargs) -> "ErrorMessageFormer":
        """
        Returns a new instance of ErrorMessageFormer with the given overrides.

        Examples::

            >>> custom = ErrorMsgFormer.clone_with(use_oxford_comma=False)
            >>> custom.not_allowed_together('a', 'b', 'c')
            'a, b and c are not allowed together.'
        """
        return ErrorMessageFormer(
            locale=kwargs.get("locale", self.locale),
            use_oxford_comma=kwargs.get("use_oxford_comma", self.use_oxford_comma),
            conjunctions=kwargs.get("conjunctions", self.conjunctions.copy())
        )


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
