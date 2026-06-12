"""Tests for SDK context building functionality."""

import pytest
from typing import Any

from maven_pom_generator import build_sdk_context


def test_build_sdk_context_returns_dict(test_config: dict[str, Any]) -> None:
    """Test that build_sdk_context returns a dictionary."""
    context = build_sdk_context('EMA', '2.4.0', 17, test_config)
    assert isinstance(context, dict)


def test_build_sdk_context_required_keys(test_config: dict[str, Any]) -> None:
    """Test that context contains all required keys."""
    context = build_sdk_context('EMA', '2.4.0', 17, test_config)
    required_keys = [
        'api',
        'apiversion',
        'compat_jdk_version',
        'compat_jfx_version',
        'junitscope',
        'namespace',
        'transportapi',
        'artifactid'
    ]
    for key in required_keys:
        assert key in context, f"Missing key: {key}"


def test_build_sdk_context_ema_api(test_config: dict[str, Any]) -> None:
    """Test that EMA API is preserved in context."""
    context = build_sdk_context('EMA', '2.4.0', 17, test_config)
    assert context['api'] == 'EMA'


def test_build_sdk_context_eta_api(test_config: dict[str, Any]) -> None:
    """Test that ETA API is preserved in context."""
    context = build_sdk_context('ETA', '2.4.0', 17, test_config)
    assert context['api'] == 'ETA'


def test_build_sdk_context_valid_version_resolution(test_config: dict[str, Any]) -> None:
    """Test that valid version is resolved correctly."""
    context = build_sdk_context('EMA', '2.4.0', 17, test_config)
    assert context['apiversion'] == '3.10.0.1'


def test_build_sdk_context_invalid_version_fallback(test_config: dict[str, Any]) -> None:
    """Test that invalid version falls back to latest version."""
    context = build_sdk_context('EMA', '9.9.9', 17, test_config)
    # When invalid version used, it falls back to latest_version (the RTSDK key, not the resolved Maven version)
    assert context['apiversion'] == '2.4.0'  # latest_version


def test_build_sdk_context_jdk_version_preserved(test_config: dict[str, Any]) -> None:
    """Test that JDK version is preserved in context."""
    for jdk in [11, 17, 21, 25]:
        context = build_sdk_context('EMA', '2.4.0', jdk, test_config)
        assert context['compat_jdk_version'] == jdk


def test_build_sdk_context_javafx_mapping_jdk11(test_config: dict[str, Any]) -> None:
    """Test JavaFX version mapping for JDK 11."""
    context = build_sdk_context('EMA', '2.4.0', 11, test_config)
    assert context['compat_jfx_version'] == '17.0.19'


def test_build_sdk_context_javafx_mapping_jdk17(test_config: dict[str, Any]) -> None:
    """Test JavaFX version mapping for JDK 17."""
    context = build_sdk_context('EMA', '2.4.0', 17, test_config)
    assert context['compat_jfx_version'] == '21.0.11'


def test_build_sdk_context_javafx_mapping_jdk21(test_config: dict[str, Any]) -> None:
    """Test JavaFX version mapping for JDK 21."""
    context = build_sdk_context('EMA', '2.4.0', 21, test_config)
    assert context['compat_jfx_version'] == '21.0.11'


def test_build_sdk_context_javafx_mapping_jdk25(test_config: dict[str, Any]) -> None:
    """Test JavaFX version mapping for JDK 25."""
    context = build_sdk_context('EMA', '2.4.0', 25, test_config)
    assert context['compat_jfx_version'] == '25.0.3'


def test_build_sdk_context_junit_scope_ema(test_config: dict[str, Any]) -> None:
    """Test that JUnit scope is 'test' for EMA."""
    context = build_sdk_context('EMA', '2.4.0', 17, test_config)
    assert context['junitscope'] == 'test'


def test_build_sdk_context_junit_scope_eta(test_config: dict[str, Any]) -> None:
    """Test that JUnit scope is 'compile' for ETA."""
    context = build_sdk_context('ETA', '2.4.0', 17, test_config)
    assert context['junitscope'] == 'compile'


def test_build_sdk_context_namespace(test_config: dict[str, Any]) -> None:
    """Test that namespace is resolved correctly."""
    context = build_sdk_context('EMA', '2.4.0', 17, test_config)
    assert context['namespace'] == 'com.refinitiv'


def test_build_sdk_context_transportapi(test_config: dict[str, Any]) -> None:
    """Test that transportapi is resolved correctly."""
    context = build_sdk_context('EMA', '2.4.0', 17, test_config)
    assert context['transportapi'] == 'eta'


def test_build_sdk_context_artifact_id_format_ema(test_config: dict[str, Any]) -> None:
    """Test that artifact ID format is correct for EMA."""
    context = build_sdk_context('EMA', '2.4.0', 17, test_config)
    assert context['artifactid'] == 'EMA_3.10.0.1'


def test_build_sdk_context_artifact_id_format_eta(test_config: dict[str, Any]) -> None:
    """Test that artifact ID format is correct for ETA."""
    context = build_sdk_context('ETA', '2.1.0', 17, test_config)
    assert context['artifactid'] == 'ETA_3.7.0.0'


@pytest.mark.parametrize('version,expected_apiversion', [
    ('2.0.0', '3.6.0.0'),
    ('2.1.0', '3.7.0.0'),
    ('2.4.0', '3.10.0.1'),
])
def test_build_sdk_context_various_versions(test_config: dict[str, Any], version: str, expected_apiversion: str) -> None:
    """Test version resolution for various RTSDK versions."""
    context = build_sdk_context('EMA', version, 17, test_config)
    assert context['apiversion'] == expected_apiversion
