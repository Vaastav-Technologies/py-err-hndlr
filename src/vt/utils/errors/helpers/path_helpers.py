#!/usr/bin/env python3
# coding=utf-8

import os
import re
from pathlib import Path
from typing import TextIO

from vt.utils.errors.error_specs.exceptions import VTException
from vt.utils.errors.error_specs.error_codes import (
    ERR_FILE_NOT_FOUND,
    ERR_INVALID_USAGE,
    ERR_CMD_EXECUTION_PERMISSION_DENIED,
    ERR_UNDERLYING_CMD_ERR,
)


class DirectoryAlreadyExistsError(FileExistsError):
    pass


class DirectoryNotFoundError(FileNotFoundError):
    pass


class WrongPathStructureError(ValueError):
    """
    Raise when the user provides and unacceptable path.
    """

    pass


class Directory:
    """
    argparse type to validate and convert a string path to a directory.
    """

    def __init__(
        self,
        allow_already_exists: bool = True,
        readable: bool = True,
        writable: bool = True,
    ):
        """
        Validate and convert a string to a path.
        :param allow_already_exists: allow existing directories
        :param readable: check permission to read
        :param writable: check permission to write
        """
        self.allow_already_exists = allow_already_exists
        self.readable = readable
        self.writable = writable

    def validate_conditions(self, dir_path: str):
        if self.allow_already_exists:
            if not os.path.exists(dir_path):
                raise DirectoryNotFoundError(f"Path '{dir_path}' does not exist.")
            else:
                self.validate_dir_props(dir_path)
        else:
            if os.path.exists(dir_path):
                self.validate_dir_props(dir_path)
                raise DirectoryAlreadyExistsError(f"Path '{dir_path}' already exists.")

        return Path(dir_path)

    def validate_dir_props(self, dir_path: str):
        if not os.path.isdir(dir_path):
            raise NotADirectoryError(f"'{dir_path}' is not a directory.")
        if self.readable and not os.access(dir_path, os.R_OK):
            raise PermissionError(f"No read permission for: '{dir_path}'.")
        if self.writable and not os.access(dir_path, os.W_OK):
            raise PermissionError(f"No write permission for: '{dir_path}'.")


def is_subpath(child, parent):
    """
    Check if child path is a sub-path of the parent

    Examples:
    For directory
    >>> import tempfile
    >>> with tempfile.TemporaryDirectory() as tmp_dir:
    ...     # tmp_dir is root dir
    ...     PARENT = Path(tmp_dir, "parent")
    ...     CHILD = Path(PARENT, "child")
    ...     is_subpath(CHILD, PARENT)
    True

    For file
    >>> with tempfile.TemporaryDirectory() as tmp_dir:
    ...     # tmp_dir is root dir
    ...     PARENT = Path(tmp_dir, "parent")
    ...     CHILD = Path(PARENT, "child.txt")
    ...     is_subpath(CHILD, PARENT)
    True

    For not child
    >>> with tempfile.TemporaryDirectory() as tmp_dir:
    ...     # tmp_dir is root dir
    ...     PARENT = Path(tmp_dir, "parent")
    ...     SIBLING = Path(tmp_dir, "sibling")
    ...     is_subpath(CHILD, SIBLING)
    False

    :param child: child directory to check
    :param parent: parent directory
    :return: True if child path is a sub-path of the parent path
    """
    # Convert to Path objects and resolve absolute paths
    child = Path(child).resolve()
    parent = Path(parent).resolve()

    # Check if the parent path is in the child's parents
    return parent in child.parents


def require_file(
    file: Path,
    emphasis_str: str,
    exception_class: type[VTException] = VTException,
    must_exist: bool = True,
) -> Path:
    """
    Require that file is a file (not a directory) and it should exist if ``must_exist`` is ``True``.

    :param file: file to check.
    :param emphasis_str: string to log.
    :param exception_class: Exception to be raised.
    :param must_exist: Do we require file to exist?
    :raises VTException: if param is a directory, or it does not exist when ``must_exist`` is ``True``.
    :returns: path to file.
    """
    if file.is_dir():
        errmsg = f"Supplied {emphasis_str} path: '{file}' must be a file."
        raise exception_class(
            errmsg, exit_code=ERR_INVALID_USAGE
        ) from IsADirectoryError(errmsg)
    if must_exist and not file.exists():
        errmsg = f"{emphasis_str} at path: '{file}' does not exist."
        raise exception_class(
            errmsg, exit_code=ERR_FILE_NOT_FOUND
        ) from FileNotFoundError(errmsg)
    return file


def require_dir(
    dir_to_check: Path,
    emphasis_str: str,
    exception_class: type[VTException] = VTException,
    must_exist: bool = True,
) -> Path:
    """
    Require that file is a file (not a directory) and it should exist if ``must_exist`` is ``True``.

    :param dir_to_check: directory to check.
    :param emphasis_str: string to log.
    :param exception_class: Exception to be raised.
    :param must_exist: Do we require directory to exist?
    :raises VTException: if param is a file, or it does not exist when ``must_exist`` is ``True``.
    :returns: path to directory.
    """
    if dir_to_check.is_file():
        errmsg = f"Supplied {emphasis_str} path: '{dir_to_check}' must be a directory."
        raise exception_class(
            errmsg, exit_code=ERR_INVALID_USAGE
        ) from NotADirectoryError(errmsg)
    if must_exist and not dir_to_check.exists():
        errmsg = f"{emphasis_str} at path: '{dir_to_check}' does not exist."
        raise exception_class(
            errmsg, exit_code=ERR_FILE_NOT_FOUND
        ) from DirectoryNotFoundError(errmsg)
    return dir_to_check


def get_opened_file(
    file: Path,
    emphasis_str: str,
    exception_class: type[VTException] = VTException,
    must_exist: bool = True,
    *args,
    **kwargs,
) -> TextIO:
    """
    Opens file and raises any exception wrapped in supplied ``exception_class``.

    :param file: file to check.
    :param emphasis_str: string to log.
    :param exception_class: Exception class to raise.
    :param must_exist: Do we require file to exist?
    :param args: arguments for the ``open()`` function.
    :param kwargs: keyword arguments for the ``open()`` function.
    :return: path to opened file stream.
    """
    file_path = require_file(file, emphasis_str, exception_class, must_exist)
    try:
        file = open(file_path, *args, **kwargs)
    except PermissionError as pe:
        errmsg = f"Insufficient permission to read the {emphasis_str}: '{file_path}'."
        raise exception_class(
            errmsg, exit_code=ERR_CMD_EXECUTION_PERMISSION_DENIED
        ) from pe
    except OSError as oe:
        oe_err_msg = f"Underlying OS Error: {oe}."
        raise exception_class(oe_err_msg, exit_code=ERR_UNDERLYING_CMD_ERR) from oe
    except Exception as e:
        exp = f"Underlying exception: {e}."
        raise exception_class(exp, exit_code=ERR_UNDERLYING_CMD_ERR) from e
    # mypy somehow assumes returned file to be a Path, although it's a TextIO.
    # TODO: fix the return type so that mypy doesn't err on return type.
    return file  # type: ignore[return-value]


def is_glob_like(possible_posix_glob: str) -> bool:
    """
    :param possible_posix_glob:
    :return: ``True`` if the supplied pattern POSIX glob like, ``False`` otherwise.

    >>> is_glob_like(".")
    False

    >>> is_glob_like("..")
    False

    >>> is_glob_like("*")
    True

    >>> is_glob_like("?")
    True

    >>> is_glob_like("_")
    False

    >>> is_glob_like("any?file")
    True

    >>> is_glob_like("any[xyz]file")
    True

    >>> is_glob_like("any*file")
    True
    """
    # A glob pattern typically contains '*', '?', or '[...]'
    return bool(re.search(r"[*?\[\]]", possible_posix_glob))
