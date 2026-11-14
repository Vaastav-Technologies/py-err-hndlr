# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

Date format: YYYY-MM-DD

## [0.0.0.dev8] - 2026-11-14

### Added

- Introduced initial Changelog, with the history of earlier releases.

### Changed

- Requires `vt-commons>=0.0.2.dev0`, up from `0.0.1.dev9`. On Python 3.12 this brings in `typing_extensions>=4.10`,
  which `vt-commons` now depends on.

## [0.0.0.dev7] - 2026-03-09

### Added

- `handlers` package, for handling errors in one uniform way, mainly in short-running CLIs. Its `ErrorHandler`
  interface takes each error message through `process_error_msg(errmsg)`.
- `get_error_handler(err_handlr_type, logger)` in `handlers`: returns the `ErrorHandler` for one of four modes:
  - `"pass"`: ignore the error.
  - `"log"`: log it at warning level and carry on.
  - `"pause"`: log it at error level, then wait for Enter on stdin.
  - `"bomb"`: log it at critical level, then exit with `sys.exit()`, exit code 1.

  `"log"`, `"pause"` and `"bomb"` need a `logging.Logger`. A missing logger, or an unknown mode, raises `ValueError`.
- `RegisteringErrorHandler`, `Pausable` and `Bombing` interfaces in `handlers`: handlers that record errors, and the
  steps that pause or stop the program after an error.

## [0.0.0.dev6] - 2025-11-09

### Added

- `NoAllow` argparse action in `helpers.argparse_helpers`: refuses an option outright, such as `--mirror` in a
  `git push` wrapper. Parsing fails with `argument -m/--mirror: Not allowed`, and the usage line shows the option as
  `[>-m|--mirror<]`.

## [0.0.0.dev5] - 2025-10-30

### Added

- `helpers` package, to validate paths and command-line input.
- `helpers.path_helpers`:
  - `require_file()` and `require_dir()`: check that a path is a file or a directory, and that it exists unless
    `must_exist=False`. Otherwise they raise a `VTException`, or the given subclass of it, with `ERR_INVALID_USAGE`
    or `ERR_FILE_NOT_FOUND` as the exit code.
  - `get_opened_file()`: opens a file that passes `require_file()`, and wraps permission and OS errors in a
    `VTException`.
  - `is_subpath()`, and `is_glob_like()`, which tells whether a string looks like a glob such as `a/*.py`.
  - `Directory`: validates a directory path, which must exist (or must not), and be readable and writable.
  - `DirectoryNotFoundError`, `DirectoryAlreadyExistsError` and `WrongPathStructureError`.
- `helpers.argparse_helpers`, argparse types that raise `ArgumentTypeError` on a bad value:
  - `Directory`: the `path_helpers.Directory` checks.
  - `FilePath`: a file that opens in the given mode. Returns its absolute path. `KeyFilePath` also refuses an empty
    file.
  - `NotDashFileType`: an `argparse.FileType` that refuses `-`, which would otherwise open stdin or stdout.
  - `StrNotIn`: refuses the given values, optionally after processing the string, for example with `str.strip`.

## [0.0.0.dev4] - 2025-10-28

### Changed

- Requires `vt-commons>=0.0.1.dev9`, up from `0.0.1.dev4`.

## [0.0.0.dev3] - 2025-09-30

### Changed

- Accepts any `vt-commons>=0.0.1.dev4`, instead of exactly `0.0.1.dev4`.

## [0.0.0.dev2] - 2025-09-26

### Added

- `VTCmdNotFoundError` in `error_specs.exceptions`: a `VTExitingException` for a command that cannot be found. It
  takes the `command` (a string, or a list from `shlex.split()`), the `FileNotFoundError`, or both, and its message
  names the missing command. The exit code defaults to `ERR_CMD_NOT_FOUND` (127), and `cause` returns the
  `FileNotFoundError`.
  - Giving neither raises `ValueError`, and a `file_not_found_error` that is not a `FileNotFoundError` raises
    `TypeError`.
- Classifiers for Python 3.14 and 3.15.

### Changed

- Requires exactly `vt-commons==0.0.1.dev4`. Any version was accepted before.

## [0.0.0.dev1] - 2025-07-02

First release on PyPI. A typed package (`py.typed`) for Python 3.12+, in the `vt.utils.errors` namespace.

### Added

- `error_specs`: the exit codes `EXIT_OK` and `ERR_*`, such as `ERR_GENERIC_ERR`, `ERR_INVALID_USAGE`,
  `ERR_DATA_FORMAT_ERR`, `ERR_CMD_NOT_FOUND` and `ERR_SIGINT_RECEIVED`. They follow `sysexits.h` and the shell's
  conventions where one applies.
- `error_specs`: `ErrorMsgFormer`, a ready-made `ErrorMessageFormer` that writes validation messages with
  `not_allowed_together()`, `at_least_one_required()`, `all_required()` and `errmsg_for_choices()`. `clone_with()`
  changes its Oxford comma or its conjunctions.
- `error_specs`: the `DefaultOrError`, `DefaultNoError`, `WarningWithDefault` and `StrictWarningWithDefault`
  interfaces, for a missing key that either raises or warns and falls back to a default.
- `error_specs.exceptions`: the `HasExitCode` interface, and the `VTException`, `VTExitingException` and
  `VTCmdException` hierarchy. `VTExitingException` carries an exit code. `VTCmdException` wraps a
  `CalledProcessError`, whose return code is its exit code by default.
- `error_specs.utils`: `require_type()` and `require_iterable()`, which check a value's type (and an iterable's kind,
  item type and emptiness) and raise a `VTExitingException` with `ERR_DATA_FORMAT_ERR` on a mismatch.
  `require_type(lenient=True)` accepts subclasses, so that `True` passes as an `int`.
- `warnings`: `vt_warn()`, which warns without the stack trace, the `suppress_warning_stacktrace()` context manager
  that it uses, and the `Warner` interface.
