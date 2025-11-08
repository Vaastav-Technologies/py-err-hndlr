#!/usr/bin/env python3
# coding=utf-8


"""
Tests related to argparse helpers.
"""

import argparse

import pytest

from vt.utils.errors.helpers.argparse_helpers import NoAllow


@pytest.fixture(scope="session")
def no_allow_mirror_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser("test-parser")
    parser.add_argument("-m", "--mirror", action=NoAllow)
    parser.add_argument("--oops", action="store_true")
    parser.add_argument("--yo")
    return parser


@pytest.mark.parametrize(
    "args",
    [
        ["--mirror"],
        ["a", "b", "8", "-m", "--oops"],
        ["a", "b", "8", "-m", "90"],
        ["a", "b", "8", "--mirror", "90"],
        ["a", "-m", "8", "--mirror", "90"],
        ["a", "-m", "8", "--mirror"],
        ["a", "--mirror", "8", "--yo", "10"],
    ],
)
def test_no_allow(args: list[str], no_allow_mirror_parser, capsys):
    with pytest.raises(SystemExit):
        no_allow_mirror_parser.parse_known_args(args)
    assert "argument -m/--mirror: Not allowed" in capsys.readouterr().err
