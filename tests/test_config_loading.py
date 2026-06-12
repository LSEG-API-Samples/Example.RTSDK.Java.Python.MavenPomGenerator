"""Tests for config loading functionality."""

import pytest
from pathlib import Path

from maven_pom_generator import load_config


def test_load_config_reads_valid_file(config_file: Path) -> None:
    """Test that load_config reads a valid YAML file."""
    config = load_config(config_file)
    assert config is not None
    assert isinstance(config, dict)


def test_load_config_contains_required_keys(config_file: Path) -> None:
    """Test that loaded config contains all required keys."""
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


def test_load_config_rtsdk_versions(config_file: Path) -> None:
    """Test that rtsdk_versions are loaded correctly."""
    config = load_config(config_file)
    versions = config['rtsdk_versions']
    assert '2.0.0' in versions
    assert versions['2.0.0'] == '3.6.0.0'
    assert '2.4.0' in versions
    assert versions['2.4.0'] == '3.10.0.1'


def test_load_config_support_jdk_jfx_versions(config_file: Path) -> None:
    """Test that support_jdk_jfx_versions are loaded correctly."""
    config = load_config(config_file)
    jdk_jfx = config['support_jdk_jfx_versions']
    assert 11 in jdk_jfx
    assert jdk_jfx[11] == '17.0.19'
    assert 17 in jdk_jfx
    assert jdk_jfx[17] == '21.0.11'
    assert 25 in jdk_jfx
    assert jdk_jfx[25] == '25.0.3'


def test_load_config_latest_version(config_file: Path) -> None:
    """Test that latest_version is loaded correctly."""
    config = load_config(config_file)
    assert config['latest_version'] == '2.4.0'


def test_load_config_namespace(config_file: Path) -> None:
    """Test that namespace is loaded correctly."""
    config = load_config(config_file)
    assert config['namespace']['refinitiv'] == 'com.refinitiv'


def test_load_config_transportapi(config_file: Path) -> None:
    """Test that transportapi is loaded correctly."""
    config = load_config(config_file)
    assert config['transportapi']['refinitiv'] == 'eta'


def test_load_config_file_not_found() -> None:
    """Test that FileNotFoundError is raised for missing file."""
    with pytest.raises(FileNotFoundError):
        load_config(Path('./nonexistent/config.yaml'))


def test_load_config_invalid_path() -> None:
    """Test that FileNotFoundError is raised for invalid path."""
    with pytest.raises((FileNotFoundError, Exception)):
        load_config(Path('/invalid/path/config.yaml'))
