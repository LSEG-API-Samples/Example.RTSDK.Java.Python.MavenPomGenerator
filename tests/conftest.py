"""Pytest configuration and shared fixtures."""

import pytest
from pathlib import Path
from typing import Any

import yaml


@pytest.fixture
def config_file(tmp_path: Path) -> Path:
    """Create a minimal test config file."""
    config_data = {
        'rtsdk_versions': {
            '2.0.0': '3.6.0.0',
            '2.1.0': '3.7.0.0',
            '2.4.0': '3.10.0.1'
        },
        'latest_version': '2.4.0',
        'support_jdk_jfx_versions': {
            11: '17.0.19',
            17: '21.0.11',
            21: '21.0.11',
            25: '25.0.3'
        },
        'namespace': {
            'refinitiv': 'com.refinitiv'
        },
        'transportapi': {
            'refinitiv': 'eta'
        }
    }
    
    config_path = tmp_path / 'test_config.yaml'
    with open(config_path, 'w', encoding='utf-8') as f:
        yaml.dump(config_data, f)
    
    return config_path


@pytest.fixture
def test_config() -> dict[str, Any]:
    """Return test configuration data."""
    return {
        'rtsdk_versions': {
            '2.0.0': '3.6.0.0',
            '2.1.0': '3.7.0.0',
            '2.4.0': '3.10.0.1'
        },
        'latest_version': '2.4.0',
        'support_jdk_jfx_versions': {
            11: '17.0.19',
            17: '21.0.11',
            21: '21.0.11',
            25: '25.0.3'
        },
        'namespace': {
            'refinitiv': 'com.refinitiv'
        },
        'transportapi': {
            'refinitiv': 'eta'
        }
    }


@pytest.fixture
def output_dir(tmp_path: Path) -> Path:
    """Create a temporary output directory."""
    return tmp_path / 'output'


@pytest.fixture
def template_dir() -> Path:
    """Return path to template directory."""
    return Path('./templates')
