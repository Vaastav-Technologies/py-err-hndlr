#!/usr/bin/env python3
# coding=utf-8

"""
Standard POSIX error codes taken from: https://tldp.org/LDP/abs/html/exitcodes.html
Also taken from sysexit.h
"""

ENC_EXIT_OK = 0
"Everything is okay"

ENC_ERR_GENERIC_ERR = 1
"Some generic error"

ENC_ERR_INVALID_USAGE = 2
"Invalid usage command"

ENC_ERR_STATE_ALREADY_EXISTS = 4
"State already exists"

ENC_FILE_ALREADY_EXISTS = ENC_ERR_STATE_ALREADY_EXISTS
"File already exists"

ENC_DIR_ALREADY_EXISTS = ENC_ERR_STATE_ALREADY_EXISTS
"Directory already exists"

ENC_ERR_DATA_FORMAT_ERR = 65  # EX_DATAERR in sysexits.h
"Data format error, for example, while reading from a config file"

ENC_UNAVAILABLE_SERVICE_ERR = 69  # EX_UNAVAILABLE in sysexit.h
"Service unavailable"

ENC_UNSTABLE_STATE_ERR = ENC_UNAVAILABLE_SERVICE_ERR  # EX_UNAVAILABLE in sysexit.h
"Service unavailable"

ENC_UNINITIALISED_ERR = ENC_UNAVAILABLE_SERVICE_ERR  # EX_UNAVAILABLE in sysexit.h
"Service unavailable"

ENC_CANNOT_EXECUTE_CMD = 126
"Command cannot be executed"

ENC_CMD_EXECUTION_PERMISSION_DENIED = 126
"Operation unauthorized"

ENC_ERR_CMD_NOT_FOUND = 127
"Command not found"

ENC_ERR_FILE_NOT_FOUND = ENC_ERR_CMD_NOT_FOUND
"File not found"

ENC_ERR_DIR_NOT_FOUND = ENC_ERR_CMD_NOT_FOUND
"Directory not found"

ENC_ERR_UNDERLYING_CMD_ERR = 128
"Underlying command execution error"

ENC_ERR_SIGINT_RECEIVED = 130  # Ctrl-C
"Interrupt signal received"
