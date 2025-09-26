#!/usr/bin/env python3
# coding=utf-8

"""
Constants related to errors.
"""

# region explicit re-export of error codes
from vt.utils.errors.error_specs.error_codes import EXIT_OK as EXIT_OK
from vt.utils.errors.error_specs.error_codes import ERR_EXIT_OK as ERR_EXIT_OK
from vt.utils.errors.error_specs.error_codes import ERR_GENERIC_ERR as ERR_GENERIC_ERR
from vt.utils.errors.error_specs.error_codes import (
    ERR_INVALID_USAGE as ERR_INVALID_USAGE,
)
from vt.utils.errors.error_specs.error_codes import (
    ERR_STATE_ALREADY_EXISTS as ERR_STATE_ALREADY_EXISTS,
)
from vt.utils.errors.error_specs.error_codes import (
    ERR_FILE_ALREADY_EXISTS as ERR_FILE_ALREADY_EXISTS,
)
from vt.utils.errors.error_specs.error_codes import (
    ERR_DIR_ALREADY_EXISTS as ERR_DIR_ALREADY_EXISTS,
)
from vt.utils.errors.error_specs.error_codes import (
    ERR_DATA_FORMAT_ERR as ERR_DATA_FORMAT_ERR,
)
from vt.utils.errors.error_specs.error_codes import (
    ERR_UNAVAILABLE_SERVICE as ERR_UNAVAILABLE_SERVICE,
)
from vt.utils.errors.error_specs.error_codes import (
    ERR_UNSTABLE_STATE as ERR_UNSTABLE_STATE,
)
from vt.utils.errors.error_specs.error_codes import (
    ERR_UNINITIALISED as ERR_UNINITIALISED,
)
from vt.utils.errors.error_specs.error_codes import (
    ERR_CANNOT_EXECUTE_CMD as ERR_CANNOT_EXECUTE_CMD,
)
from vt.utils.errors.error_specs.error_codes import (
    ERR_CMD_EXECUTION_PERMISSION_DENIED as ERR_CMD_EXECUTION_PERMISSION_DENIED,
)
from vt.utils.errors.error_specs.error_codes import (
    ERR_CMD_NOT_FOUND as ERR_CMD_NOT_FOUND,
)
from vt.utils.errors.error_specs.error_codes import (
    ERR_FILE_NOT_FOUND as ERR_FILE_NOT_FOUND,
)
from vt.utils.errors.error_specs.error_codes import (
    ERR_DIR_NOT_FOUND as ERR_DIR_NOT_FOUND,
)
from vt.utils.errors.error_specs.error_codes import (
    ERR_UNDERLYING_CMD_ERR as ERR_UNDERLYING_CMD_ERR,
)
from vt.utils.errors.error_specs.error_codes import (
    ERR_SIGINT_RECEIVED as ERR_SIGINT_RECEIVED,
)
# endregion


import pathlib as __pathlib

type_name_map: dict[type, str] = {
    str: "a string",
    int: "an int",
    float: "a float",
    bool: "a boolean",
    __pathlib.Path: "a Path",
}
