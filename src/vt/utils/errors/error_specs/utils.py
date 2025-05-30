#!/usr/bin/env python3
# coding=utf-8

"""
Utility functions for error handling.
"""

from collections.abc import Sequence
from typing import overload

from vt.utils.errors.error_specs import ERR_DATA_FORMAT_ERR
from vt.utils.errors.error_specs.exceptions import VTExitingException

import inspect
import types


@overload
def require_type(
        val_to_check: int,
        var_name: str,
        val_type: type[int],
        exception_to_raise: type[VTExitingException] = VTExitingException,
        exit_code: int = ERR_DATA_FORMAT_ERR,
        *,
        prefix: str = '',
        suffix: str = '',
        raise_from_caller: bool = True
) -> None: ...

@overload
def require_type(
        val_to_check: bool,
        var_name: str,
        val_type: type[bool],
        exception_to_raise: type[VTExitingException] = VTExitingException,
        exit_code: int = ERR_DATA_FORMAT_ERR,
        *,
        prefix: str = '',
        suffix: str = '',
        raise_from_caller: bool = True
) -> None: ...

@overload
def require_type(
        val_to_check: float,
        var_name: str,
        val_type: type[float],
        exception_to_raise: type[VTExitingException] = VTExitingException,
        exit_code: int = ERR_DATA_FORMAT_ERR,
        *,
        prefix: str = '',
        suffix: str = '',
        raise_from_caller: bool = True
) -> None: ...

@overload
def require_type(
        val_to_check: str,
        var_name: str,
        val_type: type[str],
        exception_to_raise: type[VTExitingException] = VTExitingException,
        exit_code: int = ERR_DATA_FORMAT_ERR,
        *,
        prefix: str = '',
        suffix: str = '',
        raise_from_caller: bool = True
) -> None: ...

@overload
def require_type[T](
        val_to_check: list[T],
        var_name: str,
        val_type: type[list[T]],
        exception_to_raise: type[VTExitingException] = VTExitingException,
        exit_code: int = ERR_DATA_FORMAT_ERR,
        *,
        prefix: str = '',
        suffix: str = '',
        raise_from_caller: bool = True
) -> None: ...

@overload
def require_type[T](
        val_to_check: set[T],
        var_name: str,
        val_type: type[set[T]],
        exception_to_raise: type[VTExitingException] = VTExitingException,
        exit_code: int = ERR_DATA_FORMAT_ERR,
        *,
        prefix: str = '',
        suffix: str = '',
        raise_from_caller: bool = True
) -> None: ...

@overload
def require_type[T](
        val_to_check: tuple[T],
        var_name: str,
        val_type: type[tuple[T]],
        exception_to_raise: type[VTExitingException] = VTExitingException,
        exit_code: int = ERR_DATA_FORMAT_ERR,
        *,
        prefix: str = '',
        suffix: str = '',
        raise_from_caller: bool = True
) -> None: ...

@overload
def require_type[T](
        val_to_check: Sequence[T],
        var_name: str,
        val_type: type[Sequence[T]],
        exception_to_raise: type[VTExitingException] = VTExitingException,
        exit_code: int = ERR_DATA_FORMAT_ERR,
        *,
        prefix: str = '',
        suffix: str = '',
        raise_from_caller: bool = True
) -> None: ...

@overload
def require_type[K, V](
        val_to_check: dict[K, V],
        var_name: str,
        val_type: type[dict[K, V]],
        exception_to_raise: type[VTExitingException] = VTExitingException,
        exit_code: int = ERR_DATA_FORMAT_ERR,
        *,
        prefix: str = '',
        suffix: str = '',
        raise_from_caller: bool = True
) -> None: ...

def require_type[T](
        val_to_check: T,
        var_name: str,
        val_type: type[T],
        exception_to_raise: type[VTExitingException] = VTExitingException,
        exit_code: int = ERR_DATA_FORMAT_ERR,
        *,
        prefix: str = '',
        suffix: str = '',
        raise_from_caller: bool = True
) -> None:
    """
    Validates that the provided value matches the specified type. If it does not,
    raises a configurable exception, optionally spoofing the traceback to appear from
    the caller site.

    :param val_to_check: The value to validate.
    :type val_to_check: T
    :param var_name: Name of the variable being validated. Used in error messages.
    :type var_name: str
    :param val_type: The expected type the value must conform to.
    :type val_type: type[T]
    :param exception_to_raise: Exception type to raise. Must derive from ``VTExitingException``.
    :type exception_to_raise: type[VTExitingException]
    :param exit_code: Exit code to assign to the raised exception.
    :type exit_code: int
    :param prefix: Optional prefix for error messages.
    :type prefix: str
    :param suffix: Optional suffix for error messages.
    :type suffix: str
    :param raise_from_caller: Whether to fake traceback so the exception appears raised from the caller.
    :type raise_from_caller: bool

    :raises exception_to_raise: If the value is not an instance of ``val_type``.

    :return: None

    :example:

    >>> require_type(123, "count", int)
    >>> require_type("abc", "name", str)
    >>> require_type([1, 2, 3], "items", list)

    >>> require_type(123, "flag", bool)
    Traceback (most recent call last):
        ...
    VTExitingException: 'flag' must be of type bool

    >>> require_type("xyz", "count", int, prefix="ConfigError: ", suffix=" Refer to docs.")
    Traceback (most recent call last):
        ...
    VTExitingException: ConfigError: 'count' must be of type int Refer to docs.

    >>> class MyTypedException(VTExitingException): pass

    >>> require_type(None, "is_ready", bool, exception_to_raise=MyTypedException, exit_code=99)
    Traceback (most recent call last):
        ...
    MyTypedException: 'is_ready' must be of type bool

    >>> try:
    ...     require_type({}, "conf", str, raise_from_caller=False)
    ... except VTExitingException as ex:
    ...     isinstance(ex.__cause__, TypeError)
    True

    >>> try:
    ...     def outer():
    ...         require_type([], "thing", tuple, raise_from_caller=True)
    ...     outer()
    ... except VTExitingException as ex:
    ...     "thing" in str(ex)
    True
    """
    if not isinstance(val_to_check, val_type):
        typename = val_type.__name__
        errmsg = f"{prefix}'{var_name}' must be of type {typename}{suffix}"
        cause = TypeError(errmsg)
        exc = exception_to_raise(errmsg, exit_code=exit_code)
        exc.__cause__ = cause

        if raise_from_caller:
            frame = inspect.currentframe()
            caller_frame = frame.f_back if frame else None
            if caller_frame:
                fake_tb = types.TracebackType(
                    tb_next=None,
                    tb_frame=caller_frame,
                    tb_lasti=caller_frame.f_lasti,
                    tb_lineno=caller_frame.f_lineno
                )
                raise exc.with_traceback(fake_tb)
        raise exc from cause
