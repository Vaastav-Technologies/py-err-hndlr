#!/usr/bin/env python3
# coding=utf-8

"""
Interfaces and some default implementations for error specs.
"""

from abc import abstractmethod
from typing import Any, Protocol, override

from vt.utils.errors.error_specs import ErrorMsgFormer
from vt.utils.errors.warnings import Warner, vt_warn


class DefaultOrError[T](Protocol):
    """
    Handle a ``KeyError`` and decide whether to reraise it with a better context or return a default value.

        - re raises the supplied ``KeyError`` if ``raise_error`` is ``True``.
        - return a default value if ``raise_error`` is ``False``.
    """

    def handle_key_error(
        self,
        key_error: KeyError,
        default_level: T,
        emphasis: str | None = None,
        choices: list[Any] | None = None,
    ) -> T:
        """
        Subclasses will decide how to treat the supplied ``KeyError``.

        :param key_error: The raised ``KeyError``.
        :param emphasis: the string which is emphasised in the ``KeyError`` error message. The emphasising of
            string is not done if this value is ``None`` or not provided.
        :param default_level: the value to be returned if supplied ``KeyError`` is decided to not be raised further.
        :param choices: What are the valid choices for the entity that caused ``KeyError``. Choices will not be
            included in the error message if supplied ``None`` or empty.
        :return: ``default_level`` if ``self.raise_error`` is ``False``.
        :raise KeyError: a better context ``KeyError`` if it is decided to re raise the error by returning ``True``
            from ``self.raise_error``.
        """
        errmsg = ErrorMsgFormer.errmsg_for_choices(emphasis=emphasis, choices=choices)
        if self.raise_error:
            raise KeyError(f"{key_error}: {errmsg}")
        return default_level

    @property
    @abstractmethod
    def raise_error(self) -> bool:
        """
        :return: whether the supplied ``KeyError`` should be reraised.
        """
        ...  # pragma: no cover


class DefaultNoError[T](DefaultOrError[T], Protocol):
    """
    Interface to denote that it is decided that the supplied ``KeyError`` will not be reraised.
    """

    @override
    @property
    def raise_error(self) -> bool:
        """
        Decided to not reraise the supplied ``KeyError``.

        :return: ``False`` always.
        """
        return False  # pragma: no cover


class RaiseError[T](DefaultOrError[T]):
    def __init__(self, raise_error: bool = True):
        """
        Decide to reraise the supplied ``KeyError`` with a better context. Defaults to always reraise the supplied
        ``KeyError``.

        :param raise_error: whether to reraise the supplied ``KeyError``.
        """
        self._raise_error = raise_error  # pragma: no cover

    @property
    @abstractmethod
    def raise_error(self) -> bool:
        return self._raise_error  # pragma: no cover


class WarningWithDefault[T](DefaultOrError[T], Warner, Protocol):
    """
    Interface to denote that it can either be decided to reraise a supplied ``KeyError`` or warn about it with a better
    context.
    """

    @override
    def handle_key_error(
        self,
        key_error: KeyError,
        default_level: T,
        emphasis: str | None = None,
        choices: list[Any] | None = None,
    ) -> T:
        """
        Subclasses will decide how to treat the supplied ``KeyError``.

        Following flow is taken into account::

            - if warn_only is True then only warn the user of the error and return the supplied default value.

            - if warn_only is false and raise_error is True then reraise the supplied KeyError with a better context.

        :param key_error: The raised ``KeyError``.
        :param emphasis: the string which is emphasised in the ``KeyError`` error message. The emphasising of
            string is not done if this value is ``None`` or not provided.
        :param default_level: the value to be returned if supplied ``KeyError`` is decided to not be raised further.
        :param choices: What are the valid choices for the entity that caused ``KeyError``. Choices will not be
            included in the error message if supplied ``None`` or empty.
        :return: ``default_level`` if ``self.raise_error`` is ``False``.
        :raise KeyError: a better context ``KeyError`` if it is decided to re raise the error by returning ``True``
            from ``self.raise_error`` and ``self.warn_only`` is ``False``.
        """
        errmsg = ErrorMsgFormer.errmsg_for_choices(emphasis=emphasis, choices=choices)
        if self.warn_only:
            vt_warn(f"{key_error}: {errmsg}", stack_level=3)
        else:
            if self.raise_error:
                raise KeyError(f"{key_error}: {errmsg}")
        return default_level


class StrictWarningWithDefault[T](WarningWithDefault[T], DefaultNoError[T], Protocol):
    """
    Interface to denote that it is strictly decided that the supplied ``KeyError`` will not be reraised.
    """

    @override
    @property
    @abstractmethod
    def warn_only(self) -> bool:
        """
        Only warn the user of the caught ``KeyError`` if ``True``, else ignore the ``KeyError`` silently.
        """
        ...  # pragma: no cover


class SimpleWarningWithDefault[T](WarningWithDefault[T]):
    def __init__(self, warn_only: bool = True):
        """
        Simple implementation for ``WarningWithDefault``.

        Will reraise the caught ``KeyError`` if ``warn_only`` is ``False``.

        :param warn_only: only warn the user of the caught ``KeyError`` when ``True``. Reraise the caught ``KeyError``
            if supplied ``False``.
        """
        self._warn_only = warn_only  # pragma: no cover

    @override
    @property
    def warn_only(self) -> bool:
        return self._warn_only  # pragma: no cover

    @override
    @property
    def raise_error(self) -> bool:
        """
        Caught ``KeyError`` will be reraised if ``warn_only`` is ``False``.

        :return: inversion of ``warn_only``.
        """
        return not self.warn_only  # pragma: no cover


class NoErrWarningWithDefault[T](StrictWarningWithDefault[T]):
    def __init__(self, warn_only: bool = True):
        """
        Caught ``KeyError`` will not be reraised.

        :param warn_only: Only warn the user if supplied ``True``, else ignore the error silently.
        """
        self._warn_only = warn_only  # pragma: no cover

    @override
    @property
    def warn_only(self) -> bool:
        return self._warn_only  # pragma: no cover
