#!/usr/bin/env python3
# coding=utf-8

"""
Exceptions and exception hierarchies native to `Vaastav Technologies (OPC) Private Limited` python code.
"""
from vt.utils.errors.error_specs import ERR_GENERIC_ERR


class VTException(Exception):
    """
    Exception class native to `Vaastav Technologies (OPC) Private Limited` python code.

    Encapsulates any known exception raised by known code and hence can be handled in internal projects, like CLI(s).
    """

    def __init__(self, *args, **kwargs):
        """
        Examples:

          * standalone exceptions raising:

            >>> raise VTException()
            Traceback (most recent call last):
            VTException

          * standalone exceptions raising with message:

            >>> raise VTException('Expected.')
            Traceback (most recent call last):
            VTException: Expected.

          * chain known exceptions from known code:

            >>> raise VTException('A relevant exception') from ValueError
            Traceback (most recent call last):
            VTException: ValueError: A relevant exception

          * chain known exceptions from known code:

            >>> raise VTException('A relevant exception') from ValueError()
            Traceback (most recent call last):
            VTException: ValueError: A relevant exception

          * chain known exceptions with their own message.

            >>> raise VTException('A relevant exception') from ValueError('Unexpected value.')
            Traceback (most recent call last):
            VTException: ValueError: A relevant exception

          * chained exceptions are retained in ``cause`` property for further inspection and stact-trace.

            >>> try:
            ...     raise VTException('Some exception message') from ValueError('Unexpected value.')
            ... except VTException as v:
            ...     v.cause
            ValueError('Unexpected value.')

        :param args: arguments for ``Exception``.
        :param kwargs: extra keyword-args for more info storage.
        """
        super().__init__(*args)
        self.kwargs = kwargs

    @property
    def cause(self) -> BaseException | None:
        return self.__cause__

    def __str__(self):
        return f"{self.cause.__class__.__name__}: {super().__str__()}" if self.cause else super().__str__()


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
            VTCmdException

          * standalone exceptions raising with error code:

            >>> raise VTCmdException(exit_code=30)
            Traceback (most recent call last):
            VTCmdException

          * standalone exceptions raising with message:

            >>> raise VTCmdException('Expected.')
            Traceback (most recent call last):
            VTException: Expected.

          * standalone exceptions raising with message and error code:

            >>> raise VTCmdException('Expected.', exit_code=20)
            Traceback (most recent call last):
            VTCmdException: Expected.

          * chain known exceptions from known code:

            >>> raise VTCmdException('A relevant exception') from ValueError
            Traceback (most recent call last):
            VTCmdException: ValueError: A relevant exception

          * chain known exceptions from known code with error code:

            >>> raise VTCmdException('A relevant exception', exit_code=9) from ValueError
            Traceback (most recent call last):
            VTCmdException: ValueError: A relevant exception

          * chain known exceptions from known code:

            >>> raise VTCmdException('A relevant exception') from ValueError()
            Traceback (most recent call last):
            VTCmdException: ValueError: A relevant exception

          * chain known exceptions from known code with error code:

            >>> raise VTCmdException('A relevant exception', exit_code=40) from ValueError()
            Traceback (most recent call last):
            VTCmdException: ValueError: A relevant exception

          * chain known exceptions with their own message.

            >>> raise VTCmdException('A relevant exception') from ValueError('Unexpected value.')
            Traceback (most recent call last):
            VTCmdException: ValueError: A relevant exception

          * chain known exceptions with their own message with error code.

            >>> raise VTCmdException('A relevant exception', exit_code=90) from ValueError('Unexpected value.')
            Traceback (most recent call last):
            VTCmdException: ValueError: A relevant exception

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
