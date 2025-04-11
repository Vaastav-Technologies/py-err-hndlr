#!/usr/bin/env python3
# coding=utf-8

"""
Standard POSIX error codes taken from: https://tldp.org/LDP/abs/html/exitcodes.html
Also taken from sysexit.h
"""

EXIT_OK = 0
"Everything is okay"

ERR_EXIT_OK = EXIT_OK
"Everything is okay"

ERR_GENERIC_ERR = 1
"Some generic error"

ERR_INVALID_USAGE = 2
"Invalid usage command"

ERR_STATE_ALREADY_EXISTS = 4
"State already exists"

ERR_FILE_ALREADY_EXISTS = ERR_STATE_ALREADY_EXISTS
"File already exists"

ERR_DIR_ALREADY_EXISTS = ERR_STATE_ALREADY_EXISTS
"Directory already exists"

ERR_DATA_FORMAT_ERR = 65  # EX_DATAERR in sysexits.h
"Data format error, for example, while reading from a config file"

ERR_UNAVAILABLE_SERVICE = 69  # EX_UNAVAILABLE in sysexit.h
"Service unavailable"

ERR_UNSTABLE_STATE = ERR_UNAVAILABLE_SERVICE  # EX_UNAVAILABLE in sysexit.h
"Service unavailable"

ERR_UNINITIALISED = ERR_UNAVAILABLE_SERVICE  # EX_UNAVAILABLE in sysexit.h
"Service unavailable"

ERR_CANNOT_EXECUTE_CMD = 126
"Command cannot be executed"

ERR_CMD_EXECUTION_PERMISSION_DENIED = 126
"Operation unauthorized"

ERR_CMD_NOT_FOUND = 127
"Command not found"

ERR_FILE_NOT_FOUND = ERR_CMD_NOT_FOUND
"File not found"

ERR_DIR_NOT_FOUND = ERR_CMD_NOT_FOUND
"Directory not found"

ERR_UNDERLYING_CMD_ERR = 128
"Underlying command execution error"

ERR_SIGINT_RECEIVED = 130  # Ctrl-C
"Interrupt signal received"
