"""Tests for CLI argument parser functionality.

This module validates the command-line interface, ensuring all arguments
(--api, --version, --jdkversion) are correctly defined, validated, and
default to appropriate values. Tests cover:
- Parser creation and configuration
- All CLI options with valid inputs
- Invalid input rejection
- Default value behavior
- Combined argument parsing
"""

import pytest
import argparse
from typing import Any

from maven_pom_generator import setup_argument_parser


# ============================================================================
# Parser Setup Tests
# ============================================================================

def test_setup_argument_parser_returns_parser(test_config: dict[str, Any]) -> None:
    """Verify that setup_argument_parser creates an ArgumentParser instance."""
    parser = setup_argument_parser(test_config)
    assert isinstance(parser, argparse.ArgumentParser)


# ============================================================================
# --api Argument Tests
# ============================================================================

def test_api_argument_default(test_config: dict[str, Any]) -> None:
    """Verify that --api defaults to 'EMA' when not specified."""
    parser = setup_argument_parser(test_config)
    args = parser.parse_args([])
    assert args.api == 'EMA'


def test_api_argument_accepts_ema(test_config: dict[str, Any]) -> None:
    """Verify that --api accepts and correctly sets 'EMA'."""
    parser = setup_argument_parser(test_config)
    args = parser.parse_args(['--api', 'EMA'])
    assert args.api == 'EMA'


def test_api_argument_accepts_eta(test_config: dict[str, Any]) -> None:
    """Verify that --api accepts and correctly sets 'ETA'."""
    parser = setup_argument_parser(test_config)
    args = parser.parse_args(['--api', 'ETA'])
    assert args.api == 'ETA'


def test_api_argument_rejects_invalid(test_config: dict[str, Any]) -> None:
    """Verify that --api rejects invalid API types (e.g., 'INVALID')."""
    parser = setup_argument_parser(test_config)
    with pytest.raises(SystemExit):
        # argparse calls sys.exit() on invalid choice
        parser.parse_args(['--api', 'INVALID'])


# ============================================================================
# --version Argument Tests
# ============================================================================

def test_version_argument_default(test_config: dict[str, Any]) -> None:
    """Verify that --version defaults to the latest version from config."""
    parser = setup_argument_parser(test_config)
    args = parser.parse_args([])
    assert args.version == '2.4.0'


def test_version_argument_accepts_value(test_config: dict[str, Any]) -> None:
    """Verify that --version accepts arbitrary version strings.
    
    Note: The parser accepts any version string; validation happens
    in build_sdk_context() which falls back to latest if not found.
    """
    parser = setup_argument_parser(test_config)
    args = parser.parse_args(['--version', '2.1.0'])
    assert args.version == '2.1.0'


# ============================================================================
# --jdkversion Argument Tests
# ============================================================================

def test_jdkversion_argument_default(test_config: dict[str, Any]) -> None:
    """Verify that --jdkversion defaults to 17 when not specified."""
    parser = setup_argument_parser(test_config)
    args = parser.parse_args([])
    assert args.jdkversion == 17


def test_jdkversion_argument_accepts_11(test_config: dict[str, Any]) -> None:
    """Verify that --jdkversion accepts JDK 11."""
    parser = setup_argument_parser(test_config)
    args = parser.parse_args(['--jdkversion', '11'])
    assert args.jdkversion == 11


def test_jdkversion_argument_accepts_17(test_config: dict[str, Any]) -> None:
    """Verify that --jdkversion accepts JDK 17."""
    parser = setup_argument_parser(test_config)
    args = parser.parse_args(['--jdkversion', '17'])
    assert args.jdkversion == 17


def test_jdkversion_argument_accepts_21(test_config: dict[str, Any]) -> None:
    """Verify that --jdkversion accepts JDK 21."""
    parser = setup_argument_parser(test_config)
    args = parser.parse_args(['--jdkversion', '21'])
    assert args.jdkversion == 21


def test_jdkversion_argument_accepts_25(test_config: dict[str, Any]) -> None:
    """Verify that --jdkversion accepts JDK 25."""
    parser = setup_argument_parser(test_config)
    args = parser.parse_args(['--jdkversion', '25'])
    assert args.jdkversion == 25


def test_jdkversion_argument_rejects_invalid(test_config: dict[str, Any]) -> None:
    """Verify that --jdkversion rejects unsupported JDK versions (e.g., 99)."""
    parser = setup_argument_parser(test_config)
    with pytest.raises(SystemExit):
        # argparse calls sys.exit() on invalid choice
        parser.parse_args(['--jdkversion', '99'])


# ============================================================================
# Combined Arguments Tests
# ============================================================================

def test_combined_arguments(test_config: dict[str, Any]) -> None:
    """Verify that multiple arguments can be combined correctly.
    
    Example: --api ETA --version 2.0.0 --jdkversion 21
    """
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
    """Test various valid combinations of all three arguments.
    
    This parametrized test ensures the parser handles different combinations
    of API types, versions, and JDK versions without issues.
    """
    parser = setup_argument_parser(test_config)
    args = parser.parse_args(['--api', api, '--version', version, '--jdkversion', str(jdk)])
    assert args.api == api
    assert args.version == version
    assert args.jdkversion == jdk

