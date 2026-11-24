#!/usr/bin/env python3
# coding=utf-8

"""
Utility functions for error handling.
"""

from collections import deque
from collections.abc import Iterable
from typing import overload, TypeGuard

from vt.utils.errors.error_specs import (
    ERR_DATA_FORMAT_ERR,
    type_name_map,
    type_truthy_map,
)
from vt.utils.errors.error_specs.exceptions import VTExitingException


# region require_type() and optional_type() and their overloads
def _require_type[T](
    val_to_check: T,
    var_name: str,
    val_type: type[T],
    exception_to_raise: type[VTExitingException] = VTExitingException,
    exit_code: int = ERR_DATA_FORMAT_ERR,
    *,
    prefix: str = "",
    suffix: str = "",
    lenient: bool = False,
    truthy: bool = True,
    type_name_mapping: dict[type, str] | None = None,
    type_truthy_mapping: dict[type, str] | None = None,
) -> TypeGuard[T]:
    actual_type = type(val_to_check)
    if (not lenient and actual_type is not val_type) or (
        lenient and not isinstance(val_to_check, val_type)
    ):
        type_name_mapping = type_name_mapping or type_name_map
        typename = type_name_mapping.get(
            val_type, f"an instance of {getattr(val_type, '__name__', str(val_type))}"
        )
        errmsg = f"{prefix}'{var_name}' must be {typename}{suffix}"
        raise exception_to_raise(errmsg, exit_code=exit_code) from TypeError(errmsg)
    if truthy and val_type is not bool and not val_to_check:
        type_truthy_mapping = type_truthy_mapping or type_truthy_map
        phrase = type_truthy_mapping.get(val_type, "truthy")
        errmsg = f"{prefix}'{var_name}' must be {phrase}{suffix}"
        raise exception_to_raise(errmsg, exit_code=exit_code) from ValueError(errmsg)
    return True


# region require_type() and its overloads
@overload
def require_type(
    val_to_check: bool,
    var_name: str,
    val_type: type[bool],
    exception_to_raise: type[VTExitingException] = VTExitingException,
    exit_code: int = ERR_DATA_FORMAT_ERR,
    *,
    prefix: str = "",
    suffix: str = "",
    lenient: bool = False,
    type_name_mapping: dict[type, str] | None = None,
) -> TypeGuard[bool]: ...


@overload
def require_type(
    val_to_check: int,
    var_name: str,
    val_type: type[int],
    exception_to_raise: type[VTExitingException] = VTExitingException,
    exit_code: int = ERR_DATA_FORMAT_ERR,
    *,
    prefix: str = "",
    suffix: str = "",
    lenient: bool = False,
    truthy: bool = True,
    type_name_mapping: dict[type, str] | None = None,
    type_truthy_mapping: dict[type, str] | None = None,
) -> TypeGuard[int]: ...


@overload
def require_type(
    val_to_check: float,
    var_name: str,
    val_type: type[float],
    exception_to_raise: type[VTExitingException] = VTExitingException,
    exit_code: int = ERR_DATA_FORMAT_ERR,
    *,
    prefix: str = "",
    suffix: str = "",
    lenient: bool = False,
    truthy: bool = True,
    type_name_mapping: dict[type, str] | None = None,
    type_truthy_mapping: dict[type, str] | None = None,
) -> TypeGuard[float]: ...


@overload
def require_type(
    val_to_check: str,
    var_name: str,
    val_type: type[str],
    exception_to_raise: type[VTExitingException] = VTExitingException,
    exit_code: int = ERR_DATA_FORMAT_ERR,
    *,
    prefix: str = "",
    suffix: str = "",
    lenient: bool = False,
    truthy: bool = True,
    type_name_mapping: dict[type, str] | None = None,
    type_truthy_mapping: dict[type, str] | None = None,
) -> TypeGuard[str]: ...


def require_type[T](
    val_to_check: T,
    var_name: str,
    val_type: type[T],
    exception_to_raise: type[VTExitingException] = VTExitingException,
    exit_code: int = ERR_DATA_FORMAT_ERR,
    *,
    prefix: str = "",
    suffix: str = "",
    lenient: bool = False,
    truthy: bool = True,
    type_name_mapping: dict[type, str] | None = None,
    type_truthy_mapping: dict[type, str] | None = None,
) -> TypeGuard[T]:
    """
    Validates that the provided value matches the specified type. If it does not,
    raises a configurable exception.

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
    :param lenient: If True, uses `isinstance()` for validation (subclasses allowed, e.g. ``bool`` is an ``int`` if
        this options is ``True``). If False, uses strict `type(...) is ...`, i.e., ``bool`` is no longer considered an
        ``int``.
    :type lenient: bool
    :param truthy: If True (the default), reject falsy values after the type check:
        ``""``, ``0``, and ``0.0``. Ignored when ``val_type`` is ``bool`` (``False`` is a
        valid boolean). Pass ``truthy=False`` when ``0`` is a valid value. Use
        ``require_iterable`` for lists, sets, tuples, and deques.
    :type truthy: bool
    :param type_name_mapping: name mapping between types, like str -> string.
    :param type_truthy_mapping: phrases used when ``truthy`` rejects a value, like
        str -> ``a non-empty string``, int -> ``a non-zero int``.

    :raises exception_to_raise: If the value is not an instance of ``val_type``, or is
        falsy when ``truthy`` is True and ``val_type`` is not ``bool``.

    :return: True when validation succeeds.

    Examples:

    >>> require_type(123, "count", int)
    True

    >>> require_type("abc", "name", str)
    True

    >>> require_type(True, "count", int)
    Traceback (most recent call last):
    vt.utils.errors.error_specs.exceptions.VTExitingException: TypeError: 'count' must be an int

    Lenient checks pass ``True`` or ``bool`` as a type of ``int``:

    >>> require_type(True, "count", int, lenient=True)
    True

    >>> require_type(123, "flag", bool)
    Traceback (most recent call last):
    vt.utils.errors.error_specs.exceptions.VTExitingException: TypeError: 'flag' must be a boolean

    >>> require_type("xyz", "count", int, prefix="ConfigError: ", suffix=". Refer to docs.") # type: ignore[arg-type] expected int, provided str
    Traceback (most recent call last):
    vt.utils.errors.error_specs.exceptions.VTExitingException: TypeError: ConfigError: 'count' must be an int. Refer to docs.

    >>> class MyTypedException(VTExitingException): pass

    >>> try:
    ...     require_type(None, "is_ready", bool, exception_to_raise=MyTypedException, exit_code=99)
    ... except MyTypedException as e:
    ...     print(f"{type(e).__name__}: {e}")
    MyTypedException: TypeError: 'is_ready' must be a boolean

    >>> require_type(False, "quiet", bool)
    True

    >>> require_type("", "branch", str)
    Traceback (most recent call last):
    vt.utils.errors.error_specs.exceptions.VTExitingException: ValueError: 'branch' must be a non-empty string

    >>> require_type("", "branch", str, truthy=False)
    True

    ``0`` and ``0.0`` are also rejected unless ``truthy=False``:

    >>> require_type(0, "count", int)
    Traceback (most recent call last):
    vt.utils.errors.error_specs.exceptions.VTExitingException: ValueError: 'count' must be a non-zero int

    >>> require_type(0, "count", int, truthy=False)
    True
    """
    return _require_type(
        val_to_check,
        var_name,
        val_type,
        exception_to_raise,
        exit_code,
        prefix=prefix,
        suffix=suffix,
        lenient=lenient,
        truthy=truthy,
        type_name_mapping=type_name_mapping,
        type_truthy_mapping=type_truthy_mapping,
    )


# endregion


# region optional_type() and its overloads
@overload
def optional_type(
    val_to_check: bool | None,
    var_name: str,
    val_type: type[bool],
    exception_to_raise: type[VTExitingException] = VTExitingException,
    exit_code: int = ERR_DATA_FORMAT_ERR,
    *,
    prefix: str = "",
    suffix: str = "",
    lenient: bool = False,
    type_name_mapping: dict[type, str] | None = None,
) -> TypeGuard[bool | None]: ...


@overload
def optional_type(
    val_to_check: int | None,
    var_name: str,
    val_type: type[int],
    exception_to_raise: type[VTExitingException] = VTExitingException,
    exit_code: int = ERR_DATA_FORMAT_ERR,
    *,
    prefix: str = "",
    suffix: str = "",
    lenient: bool = False,
    truthy: bool = True,
    type_name_mapping: dict[type, str] | None = None,
    type_truthy_mapping: dict[type, str] | None = None,
) -> TypeGuard[int | None]: ...


@overload
def optional_type(
    val_to_check: float | None,
    var_name: str,
    val_type: type[float],
    exception_to_raise: type[VTExitingException] = VTExitingException,
    exit_code: int = ERR_DATA_FORMAT_ERR,
    *,
    prefix: str = "",
    suffix: str = "",
    lenient: bool = False,
    truthy: bool = True,
    type_name_mapping: dict[type, str] | None = None,
    type_truthy_mapping: dict[type, str] | None = None,
) -> TypeGuard[float | None]: ...


@overload
def optional_type(
    val_to_check: str | None,
    var_name: str,
    val_type: type[str],
    exception_to_raise: type[VTExitingException] = VTExitingException,
    exit_code: int = ERR_DATA_FORMAT_ERR,
    *,
    prefix: str = "",
    suffix: str = "",
    lenient: bool = False,
    truthy: bool = True,
    type_name_mapping: dict[type, str] | None = None,
    type_truthy_mapping: dict[type, str] | None = None,
) -> TypeGuard[str | None]: ...


def optional_type[T](
    val_to_check: T | None,
    var_name: str,
    val_type: type[T],
    exception_to_raise: type[VTExitingException] = VTExitingException,
    exit_code: int = ERR_DATA_FORMAT_ERR,
    *,
    prefix: str = "",
    suffix: str = "",
    lenient: bool = False,
    truthy: bool = True,
    type_name_mapping: dict[type, str] | None = None,
    type_truthy_mapping: dict[type, str] | None = None,
) -> TypeGuard[T | None]:
    """
    Like ``require_type``, but ``None`` is allowed and skips the check.

    Non-``None`` values use the same ``truthy`` default as ``require_type``:
    ``""``, ``0``, and ``0.0`` are rejected. ``False`` is still accepted for ``bool``.

    :param val_to_check: The value to validate, or ``None`` to skip the check.
    :type val_to_check: T | None
    :param var_name: Name of the variable being validated. Used in error messages.
    :type var_name: str
    :param val_type: The expected type the value must conform to when it is not ``None``.
    :type val_type: type[T]
    :param exception_to_raise: Exception type to raise. Must derive from ``VTExitingException``.
    :type exception_to_raise: type[VTExitingException]
    :param exit_code: Exit code to assign to the raised exception.
    :type exit_code: int
    :param prefix: Optional prefix for error messages.
    :type prefix: str
    :param suffix: Optional suffix for error messages.
    :type suffix: str
    :param lenient: If True, uses `isinstance()` for validation (subclasses allowed, e.g. ``bool`` is an ``int`` if
        this options is ``True``). If False, uses strict `type(...) is ...`, i.e., ``bool`` is no longer considered an
        ``int``.
    :type lenient: bool
    :param truthy: If True (the default), reject falsy non-``None`` values after the type check:
        ``""``, ``0``, and ``0.0``. Ignored when ``val_type`` is ``bool``. Use
        ``optional_iterable`` for lists, sets, tuples, and deques.
    :type truthy: bool
    :param type_name_mapping: name mapping between types, like str -> string.
    :param type_truthy_mapping: phrases used when ``truthy`` rejects a value, like
        str -> ``a non-empty string``, int -> ``a non-zero int``.

    :raises exception_to_raise: If a non-``None`` value is not an instance of ``val_type``, or is
        falsy when ``truthy`` is True and ``val_type`` is not ``bool``.

    :return: True when validation succeeds.

    >>> optional_type(None, "guess", bool)
    True
    >>> optional_type(False, "guess", bool)
    True
    >>> optional_type("master", "branch", str)
    True
    >>> optional_type("", "branch", str)
    Traceback (most recent call last):
    vt.utils.errors.error_specs.exceptions.VTExitingException: ValueError: 'branch' must be a non-empty string
    >>> optional_type("yes", "guess", bool)  # type: ignore[arg-type]
    Traceback (most recent call last):
    vt.utils.errors.error_specs.exceptions.VTExitingException: TypeError: 'guess' must be a boolean
    >>> optional_type(None, "count", int)
    True
    >>> optional_type(3, "count", int)
    True
    >>> optional_type(0, "count", int)
    Traceback (most recent call last):
    vt.utils.errors.error_specs.exceptions.VTExitingException: ValueError: 'count' must be a non-zero int
    >>> optional_type(0, "count", int, truthy=False)
    True
    >>> optional_type(None, "ratio", float)
    True
    >>> optional_type(1.5, "ratio", float)
    True
    >>> optional_type(0.0, "ratio", float)
    Traceback (most recent call last):
    vt.utils.errors.error_specs.exceptions.VTExitingException: ValueError: 'ratio' must be a non-zero float
    """
    if val_to_check is None:
        return True
    return _require_type(
        val_to_check,
        var_name,
        val_type,
        exception_to_raise,
        exit_code,
        prefix=prefix,
        suffix=suffix,
        lenient=lenient,
        truthy=truthy,
        type_name_mapping=type_name_mapping,
        type_truthy_mapping=type_truthy_mapping,
    )


# endregion
# endregion


# region require_iterable() and optional_iterable() and their overloads
def _require_iterable[T](
    val_to_check: Iterable[T],
    var_name: str,
    item_type: type[T] | None = None,
    enforce: type[list]
    | type[set]
    | type[tuple]
    | type[deque]
    | type[range]
    | None = None,
    exception_to_raise: type[VTExitingException] = VTExitingException,
    exit_code: int = ERR_DATA_FORMAT_ERR,
    *,
    prefix: str = "",
    suffix: str = "",
    empty: bool | None = None,
) -> TypeGuard[Iterable[T]]:
    if isinstance(val_to_check, str) or not isinstance(val_to_check, Iterable):
        errmsg = f"{prefix}'{var_name}' must be a non-str iterable{suffix}"
        raise exception_to_raise(errmsg, exit_code=exit_code) from TypeError(errmsg)

    iterable_type_str = "iterable"
    if enforce is not None:
        iterable_type_str = getattr(enforce, "__name__", str(enforce))
        if not isinstance(val_to_check, enforce):
            errmsg = f"{prefix}'{var_name}' must be of type {enforce.__name__}{suffix}"
            raise exception_to_raise(errmsg, exit_code=exit_code) from TypeError(errmsg)

    if empty is True and any(True for _ in val_to_check):
        errmsg = f"{prefix}'{var_name}' must be empty{suffix}"
        raise exception_to_raise(errmsg, exit_code=exit_code) from ValueError(errmsg)
    if empty is False and not any(True for _ in val_to_check):
        errmsg = f"{prefix}'{var_name}' must not be empty{suffix}"
        raise exception_to_raise(errmsg, exit_code=exit_code) from ValueError(errmsg)

    if item_type is not None:
        for v in val_to_check:
            if not isinstance(v, item_type):
                errmsg = f"{prefix}'{var_name}' must be a {iterable_type_str} of {item_type.__name__}s{suffix}"
                raise exception_to_raise(errmsg, exit_code=exit_code) from TypeError(
                    errmsg
                )
    return True


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
) -> TypeGuard[range]: ...


def require_iterable[T](
    val_to_check: Iterable[T],
    var_name: str,
    item_type: type[T] | None = None,
    enforce: type[list]
    | type[set]
    | type[tuple]
    | type[deque]
    | type[range]
    | None = None,
    exception_to_raise: type[VTExitingException] = VTExitingException,
    exit_code: int = ERR_DATA_FORMAT_ERR,
    *,
    prefix: str = "",
    suffix: str = "",
    empty: bool | None = None,
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
        vt.utils.errors.error_specs.exceptions.VTExitingException: TypeError: 'bad_list' must be a iterable of ints

        Enforcing wrong container type::

        >>> _ = require_iterable({1, 2}, "expect_list", item_type=int, enforce=list) # type: ignore[arg-type] # expected list, provided set
        Traceback (most recent call last):
        vt.utils.errors.error_specs.exceptions.VTExitingException: TypeError: 'expect_list' must be of type list

        Rejecting non-iterable input::

        >>> _ = require_iterable(123, "not_iter") # type: ignore[arg-type] # expects iterable, provided int
        Traceback (most recent call last):
        vt.utils.errors.error_specs.exceptions.VTExitingException: TypeError: 'not_iter' must be a non-str iterable

        Rejecting string even though it is iterable::

        >>> require_iterable("abc", "str_input") # type: ignore[arg-type] # expects non-str iterable, provided str
        Traceback (most recent call last):
        vt.utils.errors.error_specs.exceptions.VTExitingException: TypeError: 'str_input' must be a non-str iterable

        Rejecting non-empty constraint::

        >>> _ = require_iterable([], "should_be_nonempty", empty=False)
        Traceback (most recent call last):
        vt.utils.errors.error_specs.exceptions.VTExitingException: ValueError: 'should_be_nonempty' must not be empty

        Rejecting empty constraint::

        >>> _ = require_iterable([1], "should_be_empty", empty=True)
        Traceback (most recent call last):
        vt.utils.errors.error_specs.exceptions.VTExitingException: ValueError: 'should_be_empty' must be empty
    """
    return _require_iterable(
        val_to_check,
        var_name,
        item_type,
        enforce,
        exception_to_raise,
        exit_code,
        prefix=prefix,
        suffix=suffix,
        empty=empty,
    )


# endregion


# region optional_iterable() and its overloads
@overload
def optional_iterable[T](
    val_to_check: list[T] | None,
    var_name: str,
    item_type: type[T] | None = ...,
    enforce: type[list] = ...,
    exception_to_raise: type[VTExitingException] = ...,
    exit_code: int = ...,
    *,
    prefix: str = ...,
    suffix: str = ...,
    empty: bool | None = ...,
) -> TypeGuard[list[T] | None]: ...


@overload
def optional_iterable[T](
    val_to_check: tuple[T, ...] | None,
    var_name: str,
    item_type: type[T] | None = ...,
    enforce: type[tuple] = ...,
    exception_to_raise: type[VTExitingException] = ...,
    exit_code: int = ...,
    *,
    prefix: str = ...,
    suffix: str = ...,
    empty: bool | None = ...,
) -> TypeGuard[tuple[T, ...] | None]: ...


@overload
def optional_iterable[T](
    val_to_check: set[T] | None,
    var_name: str,
    item_type: type[T] | None = ...,
    enforce: type[set] = ...,
    exception_to_raise: type[VTExitingException] = ...,
    exit_code: int = ...,
    *,
    prefix: str = ...,
    suffix: str = ...,
    empty: bool | None = ...,
) -> TypeGuard[set[T] | None]: ...


@overload
def optional_iterable[T](
    val_to_check: deque[T] | None,
    var_name: str,
    item_type: type[T] | None = ...,
    enforce: type[deque] = ...,
    exception_to_raise: type[VTExitingException] = ...,
    exit_code: int = ...,
    *,
    prefix: str = ...,
    suffix: str = ...,
    empty: bool | None = ...,
) -> TypeGuard[deque[T] | None]: ...


@overload
def optional_iterable(
    val_to_check: range | None,
    var_name: str,
    item_type: type[int] | None = ...,
    enforce: type[range] = ...,
    exception_to_raise: type[VTExitingException] = ...,
    exit_code: int = ...,
    *,
    prefix: str = ...,
    suffix: str = ...,
    empty: bool | None = ...,
) -> TypeGuard[range | None]: ...


def optional_iterable[T](
    val_to_check: Iterable[T] | None,
    var_name: str,
    item_type: type[T] | None = None,
    enforce: type[list]
    | type[set]
    | type[tuple]
    | type[deque]
    | type[range]
    | None = None,
    exception_to_raise: type[VTExitingException] = VTExitingException,
    exit_code: int = ERR_DATA_FORMAT_ERR,
    *,
    prefix: str = "",
    suffix: str = "",
    empty: bool | None = None,
) -> TypeGuard[Iterable[T] | None]:
    """
    Like ``require_iterable``, but ``None`` is allowed and skips the check.

    Collections stay here; do not pass lists, sets, tuples, or deques to
    ``optional_type``.

    >>> optional_iterable(None, "items")
    True
    >>> optional_iterable([1, 2, 3], "items")
    True
    >>> optional_iterable([], "items", empty=True)
    True
    >>> optional_iterable([], "items", empty=False)
    Traceback (most recent call last):
    vt.utils.errors.error_specs.exceptions.VTExitingException: ValueError: 'items' must not be empty
    """
    if val_to_check is None:
        return True
    return _require_iterable(
        val_to_check,
        var_name,
        item_type,
        enforce,
        exception_to_raise,
        exit_code,
        prefix=prefix,
        suffix=suffix,
        empty=empty,
    )


# endregion
# endregion
