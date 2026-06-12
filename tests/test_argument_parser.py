"""Tests for CLI argument parser functionality."""

import pytest
import argparse
from typing import Any

from maven_pom_generator import setup_argument_parser


def test_setup_argument_parser_returns_parser(test_config: dict[str, Any]) -> None:
    """Test that setup_argument_parser returns an ArgumentParser."""
    parser = setup_argument_parser(test_config)
    assert isinstance(parser, argparse.ArgumentParser)


def test_api_argument_default(test_config: dict[str, Any]) -> None:
    """Test that --api defaults to EMA."""
    parser = setup_argument_parser(test_config)
    args = parser.parse_args([])
    assert args.api == 'EMA'


def test_api_argument_accepts_ema(test_config: dict[str, Any]) -> None:
    """Test that --api accepts EMA."""
    parser = setup_argument_parser(test_config)
    args = parser.parse_args(['--api', 'EMA'])
    assert args.api == 'EMA'


def test_api_argument_accepts_eta(test_config: dict[str, Any]) -> None:
    """Test that --api accepts ETA."""
    parser = setup_argument_parser(test_config)
    args = parser.parse_args(['--api', 'ETA'])
    assert args.api == 'ETA'


def test_api_argument_rejects_invalid(test_config: dict[str, Any]) -> None:
    """Test that --api rejects invalid values."""
    parser = setup_argument_parser(test_config)
    with pytest.raises(SystemExit):
        parser.parse_args(['--api', 'INVALID'])


def test_version_argument_default(test_config: dict[str, Any]) -> None:
    """Test that --version defaults to latest_version."""
    parser = setup_argument_parser(test_config)
    args = parser.parse_args([])
    assert args.version == '2.4.0'


def test_version_argument_accepts_value(test_config: dict[str, Any]) -> None:
    """Test that --version accepts a value."""
    parser = setup_argument_parser(test_config)
    args = parser.parse_args(['--version', '2.1.0'])
    assert args.version == '2.1.0'


def test_jdkversion_argument_default(test_config: dict[str, Any]) -> None:
    """Test that --jdkversion defaults to 17."""
    parser = setup_argument_parser(test_config)
    args = parser.parse_args([])
    assert args.jdkversion == 17


def test_jdkversion_argument_accepts_11(test_config: dict[str, Any]) -> None:
    """Test that --jdkversion accepts 11."""
    parser = setup_argument_parser(test_config)
    args = parser.parse_args(['--jdkversion', '11'])
    assert args.jdkversion == 11


def test_jdkversion_argument_accepts_17(test_config: dict[str, Any]) -> None:
    """Test that --jdkversion accepts 17."""
    parser = setup_argument_parser(test_config)
    args = parser.parse_args(['--jdkversion', '17'])
    assert args.jdkversion == 17


def test_jdkversion_argument_accepts_21(test_config: dict[str, Any]) -> None:
    """Test that --jdkversion accepts 21."""
    parser = setup_argument_parser(test_config)
    args = parser.parse_args(['--jdkversion', '21'])
    assert args.jdkversion == 21


def test_jdkversion_argument_accepts_25(test_config: dict[str, Any]) -> None:
    """Test that --jdkversion accepts 25."""
    parser = setup_argument_parser(test_config)
    args = parser.parse_args(['--jdkversion', '25'])
    assert args.jdkversion == 25


def test_jdkversion_argument_rejects_invalid(test_config: dict[str, Any]) -> None:
    """Test that --jdkversion rejects invalid values."""
    parser = setup_argument_parser(test_config)
    with pytest.raises(SystemExit):
        parser.parse_args(['--jdkversion', '99'])


def test_combined_arguments(test_config: dict[str, Any]) -> None:
    """Test parsing multiple arguments together."""
    parser = setup_argument_parser(test_config)
    args = parser.parse_args(['--api', 'ETA', '--version', '2.0.0', '--jdkversion', '21'])
    assert args.api == 'ETA'
    assert args.version == '2.0.0'
    assert args.jdkversion == 21


@pytest.mark.parametrize('api,version,jdk', [
    ('EMA', '2.0.0', 11),
    ('ETA', '2.1.0', 17),
    ('EMA', '2.4.0', 21),
    ('ETA', '2.4.0', 25),
])
def test_various_argument_combinations(test_config: dict[str, Any], api: str, version: str, jdk: int) -> None:
    """Test various combinations of arguments."""
    parser = setup_argument_parser(test_config)
    args = parser.parse_args(['--api', api, '--version', version, '--jdkversion', str(jdk)])
    assert args.api == api
    assert args.version == version
    assert args.jdkversion == jdk
