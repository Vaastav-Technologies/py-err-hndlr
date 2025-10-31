#!/usr/bin/env python3
# coding=utf-8

"""
Helpers related to argparse.
"""

import pathlib
from collections.abc import Callable
from typing import override
from argparse import ArgumentTypeError, FileType

import vt.utils.errors.helpers.path_helpers


class Directory(vt.utils.errors.helpers.path_helpers.Directory):
    @override
    def validate_conditions(self, dir_path: str):
        try:
            return super().validate_conditions(dir_path)
        except NotADirectoryError as e:
            raise ArgumentTypeError(
                str(e) + " A directory is required as the value for this option."
            )
        except vt.utils.errors.helpers.path_helpers.DirectoryNotFoundError as e:
            raise ArgumentTypeError(
                str(e) + " Provide a valid existing directory path."
            )
        except vt.utils.errors.helpers.path_helpers.DirectoryAlreadyExistsError as e:
            raise ArgumentTypeError(
                str(e) + " Provide a new (non-exiting) path to create directory."
            )
        except PermissionError as e:
            raise ArgumentTypeError(e)

    def __call__(self, dir_path: str) -> pathlib.Path:
        return self.validate_conditions(dir_path)


class NotDashFileType(FileType):
    """
    FileType assumes stdin or stdout if file name is '-'. Restrict that using this class.
    """

    def __call__(self, filepath):
        if filepath == "-":
            raise ArgumentTypeError("file must not be '-'")
        return super().__call__(filepath)

    @staticmethod
    def input_explain_str(filename: str) -> str:
        return (
            "Only readable files will be accepted. Since '-' as a filename opens <stdin> and because "
            f"we want to store the {filename} for later use hence '-' as a filename is not accepted. "
            "Likewise, Directories are also not accepted."
        )

    @staticmethod
    def output_explain_str(filename: str) -> str:
        return (
            "Only readable files will be accepted. Since '-' as a filename opens <stdout> and because "
            f"we want to store the {filename} for later use hence '-' as a filename is not accepted. "
            "Likewise, Directories are also not accepted."
        )


class FilePath:
    def __init__(self, mode="r", buf_size=-1, encoding=None, errors=None):
        """
        Check for the file path. Uses ``NotDashFileType`` inside.
        """
        self._open = NotDashFileType(mode, buf_size, encoding, errors)
        self.absolute_path = None
        """
        absolute path to the file to be read.
        """

    def __call__(self, file_path: str) -> pathlib.Path:
        self.absolute_path = pathlib.Path(file_path).resolve()
        assert self.absolute_path.is_absolute()
        self.check_valid_file(file_path)
        return self.absolute_path

    def check_valid_file(self, file_path: str):
        try:
            with self._open(file_path):
                # check if file can be opened as per given ctor arguments.
                pass
        except OSError as e:
            raise ArgumentTypeError(f"{e}: Provide a valid file.")

    # TODO: find a way to supply open() so that the user could directly open a file in the modes that were supplied
    #   for file verification during inception.
    #
    # def open(self):
    #     """
    #     Open the file at the ``FilePath`` with exact python's ``open`` arguments as supplied at inception.
    #     :return: open file.
    #     """
    #     try:
    #         return self._open(self.absolute_path)
    #     except Exception as e:
    #         raise EncException(*e.args, exit_code=ENC_ERR_GENERIC_ERR)

    @staticmethod
    def input_explain_str(filename: str) -> str:
        return NotDashFileType.input_explain_str(filename)

    @staticmethod
    def output_explain_str(filename: str) -> str:
        return NotDashFileType.output_explain_str(filename)


class KeyFilePath(FilePath):
    @override
    def check_valid_file(self, file_path: str):
        super().check_valid_file(file_path)
        if pathlib.Path(file_path).stat().st_size == 0:
            raise ArgumentTypeError(
                f"Supplied key file: '{file_path}' is empty. Key file must not be empty."
            )


# TODO: provide an argparse helper to disallow an option, for example, fully disallow --mirror on git push.

class StrNotIn:
    def __init__(self, *non_supported_vals, str_func: Callable[[str], str] = str):
        """
        The supplied string must not contain non-supported-values.

        :param non_supported_vals: these values will not be supported.
        :param str_func: function to perform processing on supplied str val and return the processed str. An example
            would be ``str.strip`` callable. This function is applied on the param string to obtain a processed string.
            Validation is then performed on this processed string.

        >>> StrNotIn()("ok")
        'ok'

        >>> StrNotIn("")("")
        Traceback (most recent call last):
        argparse.ArgumentTypeError: value must not be ''. ('',) values are not supported.

        - Works fine because "   " is not ""

          >>> StrNotIn("")("   ")
          '   '

        - Errs because "   " is ``str.strip``ed and then "   " equals "" after stripping

          >>> StrNotIn("", str_func=str.strip)("   ")
          Traceback (most recent call last):
          argparse.ArgumentTypeError: value must not be '   '. ('',) values are not supported.
        """
        self.non_supported_vals = non_supported_vals
        self.str_func = str_func

    def __call__(self, val: str):
        if self.str_func(val) in self.non_supported_vals:
            raise ArgumentTypeError(
                f"value must not be '{val}'. "
                f"{self.non_supported_vals} values are not supported."
            )
        return val
