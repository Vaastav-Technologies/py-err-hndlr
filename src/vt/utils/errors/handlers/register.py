#!/usr/bin/env python3
# coding=utf-8

"""
Error handlers that register errors.
"""

import logging
from abc import abstractmethod, ABC
from typing import Protocol

from typing_extensions import override

from vt.utils.errors.handlers.base import RegisteringErrorHandler, Pausable, Bombing


class StdLoggerErrHandlr(RegisteringErrorHandler, Protocol):
    """
    Interface for handlers that perform error registration by logging using std logger.
    """

    @property
    @abstractmethod
    def logger(self) -> logging.Logger:
        """
        :return: logger that is used to register errors.
        """
        ...


class AbsStdLoggerErrHandlr(StdLoggerErrHandlr, ABC):
    def __init__(
        self,
        logger: logging.Logger,
        pausable: Pausable | None = None,
        bombing: Bombing | None = None,
    ):
        """
        Perform error registration by logging into a standard logger.

        :param logger: the std logger to which error messages will be sent.
        :param pausable: pausing can be performed on error encounter/handling.
        :param bombing: bombing/exit can be performed on error encounter/handling.
        """
        self._logger = logger
        self.pausable = pausable
        self.bombing = bombing

    @override
    @property
    def logger(self) -> logging.Logger:
        return self._logger  # pragma: no cover

    @override
    def process_error_msg(self, errmsg: str) -> None:
        self.subclass_process_err_msg(errmsg)
        if self.pausable:
            self.pausable.pause()
        if self.bombing:
            self.bombing.bomb()

    @abstractmethod
    def subclass_process_err_msg(self, errmsg: str) -> None:
        """
        Error handling specific to the subclass.

        :param errmsg: error message to register.
        """
        ...


class WarnStdLoggerErrHandlr(AbsStdLoggerErrHandlr):
    """
    Error registration done by the logger at warning log level.
    """

    @override
    def subclass_process_err_msg(self, errmsg: str) -> None:
        self.logger.warning(errmsg, stacklevel=2)  # pragma: no cover


class ErrorStdLoggerErrHandlr(AbsStdLoggerErrHandlr):
    """
    Error registration done by the logger at error log level.
    """

    @override
    def subclass_process_err_msg(self, errmsg: str) -> None:
        self.logger.error(errmsg, stacklevel=2)  # pragma: no cover


class FatalStdLoggerErrHandlr(AbsStdLoggerErrHandlr):
    """
    Error registration done by the logger at fatal/Critical log level.
    """

    @override
    def subclass_process_err_msg(self, errmsg: str) -> None:
        self.logger.fatal(errmsg, stacklevel=2)  # pragma: no cover
