#!/usr/bin/env python3
# coding=utf-8

"""
Inclusive library for error handling.
"""

# region re-export constants
from vt.utils.errors.error_specs.__constants__ import EXIT_OK as EXIT_OK
from vt.utils.errors.error_specs.__constants__ import ERR_EXIT_OK as ERR_EXIT_OK
from vt.utils.errors.error_specs.__constants__ import ERR_GENERIC_ERR as ERR_GENERIC_ERR
from vt.utils.errors.error_specs.__constants__ import ERR_INVALID_USAGE as ERR_INVALID_USAGE
from vt.utils.errors.error_specs.__constants__ import ERR_STATE_ALREADY_EXISTS as ERR_STATE_ALREADY_EXISTS
from vt.utils.errors.error_specs.__constants__ import ERR_FILE_ALREADY_EXISTS as ERR_FILE_ALREADY_EXISTS
from vt.utils.errors.error_specs.__constants__ import ERR_DIR_ALREADY_EXISTS as ERR_DIR_ALREADY_EXISTS
from vt.utils.errors.error_specs.__constants__ import ERR_DATA_FORMAT_ERR as ERR_DATA_FORMAT_ERR
from vt.utils.errors.error_specs.__constants__ import ERR_UNAVAILABLE_SERVICE as ERR_UNAVAILABLE_SERVICE
from vt.utils.errors.error_specs.__constants__ import ERR_UNSTABLE_STATE as ERR_UNSTABLE_STATE
from vt.utils.errors.error_specs.__constants__ import ERR_UNINITIALISED as ERR_UNINITIALISED
from vt.utils.errors.error_specs.__constants__ import ERR_CANNOT_EXECUTE_CMD as ERR_CANNOT_EXECUTE_CMD
from vt.utils.errors.error_specs.__constants__ import ERR_CMD_EXECUTION_PERMISSION_DENIED as ERR_CMD_EXECUTION_PERMISSION_DENIED
from vt.utils.errors.error_specs.__constants__ import ERR_CMD_NOT_FOUND as ERR_CMD_NOT_FOUND
from vt.utils.errors.error_specs.__constants__ import ERR_FILE_NOT_FOUND as ERR_FILE_NOT_FOUND
from vt.utils.errors.error_specs.__constants__ import ERR_DIR_NOT_FOUND as ERR_DIR_NOT_FOUND
from vt.utils.errors.error_specs.__constants__ import ERR_UNDERLYING_CMD_ERR as ERR_UNDERLYING_CMD_ERR
from vt.utils.errors.error_specs.__constants__ import ERR_SIGINT_RECEIVED as ERR_SIGINT_RECEIVED
from vt.utils.errors.error_specs.__constants__ import type_name_map as type_name_map
# endregion


# region re-export error message helpers/classes/interfaces
from vt.utils.errors.error_specs.errmsg import ErrorMsgFormer as ErrorMsgFormer
from vt.utils.errors.error_specs.errmsg import ErrorMessageFormer as ErrorMessageFormer
# endregion

# region re-export error categorisation
from vt.utils.errors.error_specs.base import DefaultOrError as DefaultOrError
from vt.utils.errors.error_specs.base import DefaultNoError as DefaultNoError
from vt.utils.errors.error_specs.base import WarningWithDefault as WarningWithDefault
from vt.utils.errors.error_specs.base import StrictWarningWithDefault as StrictWarningWithDefault
# endregion
