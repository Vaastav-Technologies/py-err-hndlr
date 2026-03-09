#!/usr/bin/env python3
# coding=utf-8

"""
Base classes and interfaces for error handling.
"""

import sys
from abc import abstractmethod
from typing import Protocol, override, overload

from vt.utils.errors.error_specs import ERR_GENERIC_ERR, ErrorMsgFormer


class ErrorHandler(Protocol):
    """
    Interface to handle error scenarios in standardised way.
    """

    @abstractmethod
    def process_error_msg(self, errmsg: str) -> None:
        """
        Handle (pass/register/...) error message.

        :param errmsg: The message to handle.
        """
        ...


class RegisteringErrorHandler(ErrorHandler, Protocol):
    """
    Error handlers that register errors.
    """

    pass


class NoOpErrorHandler(ErrorHandler):
    """
    Error handlers that perform no operations for error registration and reporting and simply pass.
    """

    def process_error_msg(self, errmsg: str) -> None:
        """
        No op implementation for error handling.

        :param errmsg: error message.
        """
        pass  # pragma: no cover


class Pausable(Protocol):
    """
    Flow pausers.
    """

    @abstractmethod
    def pause(self) -> None:
        """
        Pausing or blocking function.
        """
        ...


class StdinPausing(Pausable):
    def __init__(self, stdin_str: str = ""):
        """
        Pausing done by waiting on input on stdin.

        :param stdin_str: The string to print on stdout for stdin in put on error pause. e.g. ``>>`` or ``Press Enter to continue...``.
        """
        self.stdin_str = stdin_str

    @override
    def pause(self) -> None:
        """
        Wait for stdin input to pause.
        """
        input(self.stdin_str)  # pragma: no cover


class Bombing(Protocol):
    """
    Flow bombers.

    Can bomb and stop flows.
    """

    @abstractmethod
    def bomb(self) -> None:
        """
        Simply bomb and stop/exit the flow.
        """
        ...


class SysExitBomb(Bombing):
    @overload
    def __init__(self, *, exit_code: int = ERR_GENERIC_ERR): ...

    @overload
    def __init__(self, *, errmsg: str): ...

    def __init__(self, *, exit_code: int = ERR_GENERIC_ERR, errmsg: str | None = None):
        """
        Exit the whole program using ``sys.exit()``.

        Examples:

          - Both ``errmsg`` and ``exit_code`` cannot be given together.

            >>> s = SysExitBomb(errmsg="yo", exit_code=10)
            Traceback (most recent call last):
            ValueError: errmsg and exit_code are not allowed together

            >>> s = SysExitBomb(exit_code=10, errmsg="yo")
            Traceback (most recent call last):
            ValueError: errmsg and exit_code are not allowed together

          - Default makes error message as ``None`` and exit code as ``1``.

            >>> s = SysExitBomb()
            >>> assert s.exit_code == ERR_GENERIC_ERR
            >>> assert s.errmsg is None


        :param exit_code: exit code to use when exiting.
        :param errmsg: error message to print on generic error if onw is provided.
        """
        if errmsg and exit_code != ERR_GENERIC_ERR:
            raise ValueError(ErrorMsgFormer.not_allowed_together("errmsg", "exit_code"))
        self.exit_code = exit_code
        self.errmsg = errmsg

    @override
    def bomb(self) -> None:
        """
        Exit the flow with exit codes.

        >>> SysExitBomb().bomb()
        Traceback (most recent call last):
        SystemExit: 1

        >>> SysExitBomb(exit_code=22).bomb()
        Traceback (most recent call last):
        SystemExit: 22

        Exit the flow with error message.

        >>> SysExitBomb(errmsg="Yo").bomb()
        Traceback (most recent call last):
        SystemExit: Yo

        """
        if self.errmsg:
            sys.exit(self.errmsg)
        sys.exit(self.exit_code)
