"""Tests for config loading functionality.

This module validates that the configuration system correctly loads and parses
RTSDK version mappings from the YAML config file. Tests cover:
- Valid YAML file loading
- Required configuration keys
- Version mapping accuracy
- Error handling for missing/invalid files
"""

import pytest
from pathlib import Path

from maven_pom_generator import load_config


# ============================================================================
# Basic Config Loading Tests
# ============================================================================

def test_load_config_reads_valid_file(config_file: Path) -> None:
    """Verify that load_config can read a valid YAML file."""
    config = load_config(config_file)
    assert config is not None
    assert isinstance(config, dict)


def test_load_config_contains_required_keys(config_file: Path) -> None:
    """Ensure all required configuration keys are present in the loaded config."""
    config = load_config(config_file)
    required_keys = [
        'rtsdk_versions',
        'latest_version',
        'support_jdk_jfx_versions',
        'namespace',
        'transportapi'
    ]
    for key in required_keys:
        assert key in config, f"Missing required key: {key}"


# ============================================================================
# RTSDK Version Mapping Tests
# ============================================================================

def test_load_config_rtsdk_versions(config_file: Path) -> None:
    """Validate that RTSDK version mappings are loaded correctly.
    
    RTSDK versions map to their corresponding Maven Central versions.
    E.g., RTSDK 2.0.0 -> Maven 3.6.0.0
    """
    config = load_config(config_file)
    versions = config['rtsdk_versions']
    assert '2.0.0' in versions
    assert versions['2.0.0'] == '3.6.0.0'
    assert '2.4.0' in versions
    assert versions['2.4.0'] == '3.10.0.1'


def test_load_config_latest_version(config_file: Path) -> None:
    """Verify that the latest RTSDK version is correctly specified."""
    config = load_config(config_file)
    assert config['latest_version'] == '2.4.0'


# ============================================================================
# JDK and JavaFX Version Mapping Tests
# ============================================================================

def test_load_config_support_jdk_jfx_versions(config_file: Path) -> None:
    """Validate that JDK-to-JavaFX version mapping is loaded correctly.
    
    Each supported JDK version must map to a compatible JavaFX version.
    E.g., JDK 17 -> JavaFX 21.0.11
    """
    config = load_config(config_file)
    jdk_jfx = config['support_jdk_jfx_versions']
    assert 11 in jdk_jfx
    assert jdk_jfx[11] == '17.0.19'
    assert 17 in jdk_jfx
    assert jdk_jfx[17] == '21.0.11'
    assert 25 in jdk_jfx
    assert jdk_jfx[25] == '25.0.3'


# ============================================================================
# Namespace and Transport API Tests
# ============================================================================

def test_load_config_namespace(config_file: Path) -> None:
    """Verify that the namespace (com.refinitiv) is loaded correctly."""
    config = load_config(config_file)
    assert config['namespace']['refinitiv'] == 'com.refinitiv'


def test_load_config_transportapi(config_file: Path) -> None:
    """Verify that the transport API (eta) is loaded correctly."""
    config = load_config(config_file)
    assert config['transportapi']['refinitiv'] == 'eta'


# ============================================================================
# Error Handling Tests
# ============================================================================

def test_load_config_file_not_found() -> None:
    """Ensure FileNotFoundError is raised when config file does not exist."""
    with pytest.raises(FileNotFoundError):
        load_config(Path('./nonexistent/config.yaml'))


def test_load_config_invalid_path() -> None:
    """Ensure appropriate error is raised for invalid file paths."""
    with pytest.raises((FileNotFoundError, Exception)):
        load_config(Path('/invalid/path/config.yaml'))

