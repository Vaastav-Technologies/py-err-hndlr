#!/usr/bin/env python3
# coding=utf-8

"""
Utility functions for error handling.
"""

import inspect
import types
from collections import deque
from collections.abc import Iterable
from inspect import currentframe
from typing import overload, TypeGuard

from vt.utils.errors.error_specs import ERR_DATA_FORMAT_ERR
from vt.utils.errors.error_specs.exceptions import VTExitingException


# region require_type() and its overloads
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

    >>> require_type(123, "flag", bool)
    Traceback (most recent call last):
        ...
    vt.utils.errors.error_specs.exceptions.VTExitingException: TypeError: 'flag' must be of type bool

    >>> require_type("xyz", "count", int, prefix="ConfigError: ", suffix=" Refer to docs.") # type: ignore[arg-type] expected int, provided str
    Traceback (most recent call last):
    vt.utils.errors.error_specs.exceptions.VTExitingException: TypeError: ConfigError: 'count' must be of type int Refer to docs.

    >>> class MyTypedException(VTExitingException): pass

    >>> require_type(None, "is_ready", bool, exception_to_raise=MyTypedException, exit_code=99) # type: ignore[arg-type] expected boo, provided None
    Traceback (most recent call last):
    error_specs.utils.MyTypedException: TypeError: 'is_ready' must be of type bool
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
# endregion


# region require_iterable() and its overloads
@overload
def require_iterable[T](
    val_to_check: list[T],
    var_name: str,
    item_type: type[T] | None = ...,
    enforce: type[list] = ...,
    exception_to_raise: type[VTExitingException] = ...,
    exit_code: int = ...,
    *,
    prefix: str = ...,
    suffix: str = ...,
    empty: bool | None = ...,
    raise_from_caller: bool = ...
) -> TypeGuard[list[T]]: ...

@overload
def require_iterable[T](
    val_to_check: tuple[T, ...],
    var_name: str,
    item_type: type[T] | None = ...,
    enforce: type[tuple] = ...,
    exception_to_raise: type[VTExitingException] = ...,
    exit_code: int = ...,
    *,
    prefix: str = ...,
    suffix: str = ...,
    empty: bool | None = ...,
    raise_from_caller: bool = ...
) -> TypeGuard[tuple[T, ...]]: ...

@overload
def require_iterable[T](
    val_to_check: set[T],
    var_name: str,
    item_type: type[T] | None = ...,
    enforce: type[set] = ...,
    exception_to_raise: type[VTExitingException] = ...,
    exit_code: int = ...,
    *,
    prefix: str = ...,
    suffix: str = ...,
    empty: bool | None = ...,
    raise_from_caller: bool = ...
) -> TypeGuard[set[T]]: ...

@overload
def require_iterable[T](
    val_to_check: deque[T],
    var_name: str,
    item_type: type[T] | None = ...,
    enforce: type[deque] = ...,
    exception_to_raise: type[VTExitingException] = ...,
    exit_code: int = ...,
    *,
    prefix: str = ...,
    suffix: str = ...,
    empty: bool | None = ...,
    raise_from_caller: bool = ...
) -> TypeGuard[deque[T]]: ...

@overload
def require_iterable(
    val_to_check: range,
    var_name: str,
    item_type: type[int] | None = ...,
    enforce: type[range] = ...,
    exception_to_raise: type[VTExitingException] = ...,
    exit_code: int = ...,
    *,
    prefix: str = ...,
    suffix: str = ...,
    empty: bool | None = ...,
    raise_from_caller: bool = ...
) -> TypeGuard[range]: ...

def require_iterable[T](
    val_to_check: Iterable[T],
    var_name: str,
    item_type: type[T] | None = None,
    enforce: type[list] | type[set] | type[tuple] | type[deque] | type[range] | None = None,
    exception_to_raise: type[VTExitingException] = VTExitingException,
    exit_code: int = ERR_DATA_FORMAT_ERR,
    *,
    prefix: str = '',
    suffix: str = '',
    empty: bool | None = None,
    raise_from_caller: bool = True
) -> TypeGuard[Iterable[T]]:
    """
    Validate that the input is an iterable (excluding ``str``). Optionally enforce a specific iterable type
    such as ``list``, ``set``, or ``tuple``, and check element types via ``item_type``. Also allows empty/non-empty checks.

    :param val_to_check: The value to validate as an iterable
    :param var_name: The name of the variable for error messages
    :param item_type: If given, checks that all elements are of this type
    :param enforce: Optional concrete iterable type to enforce (e.g. list, set, tuple, deque, range)
    :param exception_to_raise: Exception class to raise
    :param exit_code: Error code
    :param prefix: Prefix to prepend to error message
    :param suffix: Suffix to append to error message
    :param empty: If set to True, ensures the iterable is empty; if False, ensures it is not
    :param raise_from_caller: Whether to spoof traceback from the caller

    :raises: exception_to_raise

    Examples::

        >>> _ = require_iterable([1, 2, 3], "my_list")
        >>> _ = require_iterable(("a", "b"), "my_tuple", item_type=str)
        >>> _ = require_iterable({1, 2, 3}, "my_set", item_type=int, enforce=set)
        >>> _ = require_iterable([], "empty", empty=True)

        Enforcing non-empty list::

        >>> _ = require_iterable([42], "nonempty", item_type=int, enforce=list, empty=False)

        Type mismatch in values::

        >>> _ = require_iterable([1, "two"], "bad_list", item_type=int)
        Traceback (most recent call last):
        vt.utils.errors.error_specs.exceptions.VTExitingException: TypeError: 'bad_list' must be a iterable of int

        Enforcing wrong container type::

        >>> _ = require_iterable({1, 2}, "expect_list", item_type=int, enforce=list) # type: ignore[arg-type] # expected list, provided set
        Traceback (most recent call last):
        vt.utils.errors.error_specs.exceptions.VTExitingException: TypeError: 'expect_list' must be of type list

        Rejecting non-iterable input::

        >>> _ = require_iterable(123, "not_iter") # type: ignore[arg-type] # expects iterable, provided int
        Traceback (most recent call last):
        vt.utils.errors.error_specs.exceptions.VTExitingException: TypeError: 'not_iter' must be an iterable (not a string)

        Rejecting string even though it is iterable::

        >>> require_iterable("abc", "str_input") # type: ignore[arg-type] # expects non-str iterable, provided str
        Traceback (most recent call last):
        vt.utils.errors.error_specs.exceptions.VTExitingException: TypeError: 'str_input' must be an iterable (not a string)

        Rejecting non-empty constraint::

        >>> _ = require_iterable([], "should_be_nonempty", empty=False)
        Traceback (most recent call last):
        vt.utils.errors.error_specs.exceptions.VTExitingException: TypeError: 'should_be_nonempty' must not be empty

        Rejecting empty constraint::

        >>> _ = require_iterable([1], "should_be_empty", empty=True)
        Traceback (most recent call last):
        vt.utils.errors.error_specs.exceptions.VTExitingException: TypeError: 'should_be_empty' must be empty
    """
    def raise_error(msg: str):
        cause = TypeError(msg)
        exc = exception_to_raise(msg, exit_code=exit_code)
        exc.__cause__ = cause
        if raise_from_caller:
            frame = currentframe()
            if frame and (caller := frame.f_back):
                tb = types.TracebackType(
                    tb_next=None,
                    tb_frame=caller,
                    tb_lasti=caller.f_lasti,
                    tb_lineno=caller.f_lineno
                )
                raise exc.with_traceback(tb)
        raise exc from cause

    if isinstance(val_to_check, str) or not isinstance(val_to_check, Iterable):
        raise_error(f"{prefix}'{var_name}' must be an iterable (not a string){suffix}")

    iterable_type_str = 'iterable'
    if enforce is not None:
        iterable_type_str = getattr(enforce, '__name__', str(enforce))
        if not isinstance(val_to_check, enforce):
            raise_error(f"{prefix}'{var_name}' must be of type {enforce.__name__}{suffix}")

    if empty is True and any(True for _ in val_to_check):
        raise_error(f"{prefix}'{var_name}' must be empty{suffix}")
    if empty is False and not any(True for _ in val_to_check):
        raise_error(f"{prefix}'{var_name}' must not be empty{suffix}")

    if item_type is not None:
        for v in val_to_check:
            if not isinstance(v, item_type):
                raise_error(f"{prefix}'{var_name}' must be a {iterable_type_str} of {item_type.__name__}{suffix}")
    return True
# endregion
