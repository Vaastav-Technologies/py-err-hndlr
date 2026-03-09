#!/usr/bin/env python3
# coding=utf-8

"""
Error handlers.
"""

import logging
from typing import Literal, overload

# region re-exports interfaces
from vt.utils.errors.error_specs import ErrorMsgFormer
from vt.utils.errors.handlers.base import ErrorHandler as ErrorHandler
from vt.utils.errors.handlers.base import (
    RegisteringErrorHandler as RegisteringErrorHandler,
)
from vt.utils.errors.handlers.base import Pausable as Pausable
from vt.utils.errors.handlers.base import Bombing as Bombing

# region import implementations
from vt.utils.errors.handlers.register import (
    WarnStdLoggerErrHandlr as _WarnStdLoggerErrHandlr,
)
from vt.utils.errors.handlers.register import (
    ErrorStdLoggerErrHandlr as _ErrorStdLoggerErrHandlr,
)
from vt.utils.errors.handlers.register import (
    FatalStdLoggerErrHandlr as _FatalStdLoggerErrHandlr,
)
from vt.utils.errors.handlers.base import StdinPausing as _StdinPausing
from vt.utils.errors.handlers.base import SysExitBomb as _SysExitBomb
from vt.utils.errors.handlers.base import NoOpErrorHandler as _NoOpErrorHandler
# endregion
# endregion


@overload
def get_error_handler(err_handlr_type: Literal["pass"]) -> _NoOpErrorHandler: ...


@overload
def get_error_handler(
    err_handlr_type: Literal["log"],
    logger: logging.Logger,
) -> _WarnStdLoggerErrHandlr: ...


@overload
def get_error_handler(
    err_handlr_type: Literal["pause"],
    logger: logging.Logger,
) -> _ErrorStdLoggerErrHandlr: ...


@overload
def get_error_handler(
    err_handlr_type: Literal["bomb"],
    logger: logging.Logger,
) -> _FatalStdLoggerErrHandlr: ...


def get_error_handler(
    err_handlr_type: Literal["log", "pause", "bomb", "pass"],
    logger: logging.Logger | None = None,
) -> ErrorHandler:
    """
    Factory that returns an ``ErrorHandler`` implementation based on the
    requested behaviour.

    The function supports four handler strategies:

    - ``"pass"`` – ignore the error (no-operation handler).
    - ``"log"`` – log the error using the provided ``logging.Logger``.
    - ``"pause"`` – log the error and pause execution awaiting user input.
    - ``"bomb"`` – log the error and terminate the program.

    The ``logger`` parameter is **required** for the registering handler
    strategies (``"log"``, ``"pause"``, ``"bomb"``). It **must not** be supplied
    when ``err_handlr_type="pass"``.

    Examples
    --------
    Create a no-op handler:

    >>> h = get_error_handler("pass")
    >>> isinstance(h, _NoOpErrorHandler)
    True

    Create a logging handler:

    >>> import logging
    >>> log = logging.getLogger("demo")
    >>> h = get_error_handler("log", log)
    >>> isinstance(h, _WarnStdLoggerErrHandlr)
    True

    Pause handler:

    >>> log = logging.getLogger("demo")
    >>> h = get_error_handler("pause", log)
    >>> isinstance(h, _ErrorStdLoggerErrHandlr)
    True

    Bomb handler:

    >>> log = logging.getLogger("demo")
    >>> h = get_error_handler("bomb", log)
    >>> isinstance(h, _FatalStdLoggerErrHandlr)
    True

    Missing logger for registering handlers raises an error:

    >>> get_error_handler("log")  # type: ignore[arg-type] # need a logger but no logger provided.
    Traceback (most recent call last):
    ValueError: logger is required for a registering type error handler.

    Bogus error handler requested:

    >>> get_error_handler("bogus")  # type: ignore[arg-type] # need a logger but no logger provided.
    Traceback (most recent call last):
    ValueError: Unexpected err_handlr_type value. Choose from 'log', 'pause', 'bomb' and 'pass'.

    :param err_handlr_type: The desired error handler strategy. Must be one of
        ``"log"``, ``"pause"``, ``"bomb"``, or ``"pass"``.

    :param logger: A ``logging.Logger`` used by registering handlers
        (``"log"``, ``"pause"``, ``"bomb"``). Required for those handler types
        and must not be supplied when ``err_handlr_type="pass"``.

    :returns: An ``ErrorHandler`` instance implementing the requested behaviour.

    :raises ValueError: If ``logger`` is not provided for a registering handler type.

    :raises ValueError: If ``err_handlr_type`` is not one of the supported values.
    """

    errmsg = ErrorMsgFormer.errmsg_for_choices(
        emphasis="err_handlr_type", choices=["log", "pause", "bomb", "pass"]
    )

    if err_handlr_type == "pass":
        return _NoOpErrorHandler()

    elif err_handlr_type in {"log", "pause", "bomb"}:
        if logger is None:
            raise ValueError("logger is required for a registering type error handler.")

        if err_handlr_type == "log":
            return _WarnStdLoggerErrHandlr(logger)
        elif err_handlr_type == "pause":
            return _ErrorStdLoggerErrHandlr(
                logger, _StdinPausing("Press Enter to continue...")
            )
        else:
            # "bomb" branch
            return _FatalStdLoggerErrHandlr(logger, bombing=_SysExitBomb())

    else:
        raise ValueError(errmsg)
