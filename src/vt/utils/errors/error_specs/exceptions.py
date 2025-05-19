#!/usr/bin/env python3
# coding=utf-8

"""
Exceptions and exception hierarchies native to `Vaastav Technologies (OPC) Private Limited` python code.
"""
from abc import abstractmethod
from subprocess import CalledProcessError
from typing import Protocol, override
from vt.utils.commons.commons.core_py import fallback_on_none_strict
from vt.utils.errors.error_specs import ERR_GENERIC_ERR


class HasExitCode(Protocol):
    """
    Interface denoting that it stores an ``exit_code`` which can be used by applications during time of exit to denote
    an exit, error or ok condition using this error code.
    """

    @property
    @abstractmethod
    def exit_code(self) -> int:
        """
        :return: an exit code which can be used by applications during time of exit to denote
            an exit, error or ok condition using this error code.
        """
        ...


class VTException(Exception):
    """
    Exception class native to `Vaastav Technologies (OPC) Private Limited` python code.

    Encapsulates any known exception raised by known code and hence can be handled in internal projects, like CLI(s).
    """

    def __init__(self, *args, **kwargs):
        """
        Examples:

          * standalone exception raising:

            * plain class:

            >>> raise VTException
            Traceback (most recent call last):
            error_specs.exceptions.VTException

            * instance without message:

            >>> raise VTException()
            Traceback (most recent call last):
            error_specs.exceptions.VTException

            * instance with message:

            >>> raise VTException('Expected.')
            Traceback (most recent call last):
            error_specs.exceptions.VTException: Expected.

          * chain known exceptions from known code:

            * plain class:

            >>> raise VTException from ValueError
            Traceback (most recent call last):
            error_specs.exceptions.VTException: ValueError

            >>> raise VTException from ValueError()
            Traceback (most recent call last):
            error_specs.exceptions.VTException: ValueError

            >>> raise VTException from ValueError('cause message.')
            Traceback (most recent call last):
            error_specs.exceptions.VTException: ValueError: cause message.

            * plain cause class:

            >>> raise VTException() from ValueError
            Traceback (most recent call last):
            error_specs.exceptions.VTException: ValueError

            >>> raise VTException('main message') from ValueError
            Traceback (most recent call last):
            error_specs.exceptions.VTException: ValueError: main message

            * blank instance with cause class instance:

            >>> raise VTException() from ValueError()
            Traceback (most recent call last):
            error_specs.exceptions.VTException: ValueError

            * with message in cause:

            >>> raise VTException() from ValueError('cause message.')
            Traceback (most recent call last):
            error_specs.exceptions.VTException: ValueError: cause message.

            * with message in instance:

            >>> raise VTException('main message.') from ValueError
            Traceback (most recent call last):
            error_specs.exceptions.VTException: ValueError: main message.

            >>> raise VTException('main message.') from ValueError()
            Traceback (most recent call last):
            error_specs.exceptions.VTException: ValueError: main message.

          * chain known exceptions with their own message. The main instance message gets preference.

            >>> raise VTException('main message.') from ValueError('cause message.')
            Traceback (most recent call last):
            error_specs.exceptions.VTException: ValueError: main message.

          * chained exceptions are retained in ``cause`` property for further inspection and stack-trace.

            >>> try:
            ...     raise VTException('main message.') from ValueError('cause message.')
            ... except VTException as v:
            ...     v.cause
            ValueError('cause message.')

        :param args: arguments for ``Exception``.
        :param kwargs: extra keyword-args for more info storage.
        """
        super().__init__(*args)
        self.kwargs = kwargs

    @property
    def cause(self) -> BaseException | None:
        """
        :return: the ``__cause__`` of this exception, obtained when exception is raised using a ``from`` clause.
        """
        return self.__cause__

    def __str__(self) -> str:
        if not self.args and self.cause:
            if not self.cause.args:
                return f"{self.cause.__class__.__name__}"
            else:
                return f"{self.cause.__class__.__name__}: {self.cause.__str__()}"
        if self.args and not self.cause:
            return super().__str__()
        if self.args and self.cause:
            return f"{self.cause.__class__.__name__}: {super().__str__()}"
        return ''

    def to_dict(self) -> dict[str, str | None]:
        """
        :return: a structured dict version of the exception for structured logging.
        """
        return {
            "type": self.__class__.__name__,
            "message": str(self),
            "cause_type": type(self.cause).__name__ if self.cause else None,
            "cause_message": str(self.cause) if self.cause else None
        }


class VTCmdException(VTException):
    """
    A ``VTException`` that is raised for a command error and contains error code of the command error in question.
    """

    def __init__(self, *args, exit_code: int = ERR_GENERIC_ERR, **kwargs):
        """
        Examples:

          * standalone exceptions raising:

            >>> raise VTCmdException()
            Traceback (most recent call last):
            error_specs.exceptions.VTCmdException

          * standalone exceptions raising with error code:

            >>> raise VTCmdException(exit_code=30)
            Traceback (most recent call last):
            error_specs.exceptions.VTCmdException

          * standalone exceptions raising with message:

            >>> raise VTCmdException('Expected.')
            Traceback (most recent call last):
            error_specs.exceptions.VTCmdException: Expected.

          * standalone exceptions raising with message and error code:

            >>> raise VTCmdException('Expected.', exit_code=20)
            Traceback (most recent call last):
            error_specs.exceptions.VTCmdException: Expected.

          * chain known exceptions from known code:

            >>> raise VTCmdException('A relevant exception') from ValueError
            Traceback (most recent call last):
            error_specs.exceptions.VTCmdException: ValueError: A relevant exception

          * chain known exceptions from known code with error code:

            >>> raise VTCmdException('A relevant exception', exit_code=9) from ValueError
            Traceback (most recent call last):
            error_specs.exceptions.VTCmdException: ValueError: A relevant exception

          * chain known exceptions from known code:

            >>> raise VTCmdException('A relevant exception') from ValueError()
            Traceback (most recent call last):
            error_specs.exceptions.VTCmdException: ValueError: A relevant exception

          * chain known exceptions from known code with error code:

            >>> raise VTCmdException('A relevant exception', exit_code=40) from ValueError()
            Traceback (most recent call last):
            error_specs.exceptions.VTCmdException: ValueError: A relevant exception

          * chain known exceptions with their own message.

            >>> raise VTCmdException('A relevant exception') from ValueError('Unexpected value.')
            Traceback (most recent call last):
            error_specs.exceptions.VTCmdException: ValueError: A relevant exception

          * chain known exceptions with their own message with error code.

            >>> raise VTCmdException('A relevant exception', exit_code=90) from ValueError('Unexpected value.')
            Traceback (most recent call last):
            error_specs.exceptions.VTCmdException: ValueError: A relevant exception

          * chained exceptions are retained in ``cause`` property for further inspection and stact-trace.

            >>> try:
            ...     raise VTCmdException('Some exception message') from ValueError('Unexpected value.')
            ... except VTCmdException as v:
            ...     v.cause
            ValueError('Unexpected value.')

          * chained exceptions are retained in ``cause`` property for further inspection and stact-trace.

            >>> try:
            ...     raise VTCmdException('Some exception message', exit_code=10) from ValueError('Unexpected value.')
            ... except VTCmdException as v:
            ...     v.cause
            ValueError('Unexpected value.')

        :param args: arguments for ``Exception``.
        :param exit_code: exit code of the called process which err'd.
        :param kwargs: extra keyword-args for more info storage.
        """
        super().__init__(*args, exit_code=exit_code, **kwargs)
        self.exit_code = exit_code


if __name__ == '__main__':
    """
    Some test code for exception formatting check.
    """
    import logging
    import sys

    def log_sep(file=sys.stderr):
        print('='*50, file=file)
        print('|'*50, file=file)
        print('='*50, file=file)

    l = logging.getLogger()
    try:
        raise VTException from ValueError('a message.')
    except VTException as e:
        l.exception('exception')
        print('-'*50, file=sys.stderr)
        l.error(e)
    log_sep()

    try:
        raise VTException('a message.') from ValueError
    except VTException as e:
        l.exception('exception')
        print('-'*50, file=sys.stderr)
        l.error(e)
    log_sep()

    try:
        try:
            raise VTException('a message.') from ValueError('unexpected.')
        except VTException as e:
            l.exception('exception')
            print('-'*50, file=sys.stderr)
            l.error(e)
            raise VTException('Yo man') from e
    except VTException as e:
        l.exception('reraised.')
        print('-'*50, file=sys.stderr)
        l.error(e)
