"""Tests for SDK context building functionality.

This module validates that the SDK context (the data used to render the pom.xml)
is correctly built from config and CLI arguments. Tests cover:
- Context dictionary structure and contents
- Version resolution (valid and fallback paths)
- JDK to JavaFX version mapping for all supported JDKs
- API-specific behavior (EMA vs ETA)
- Artifact ID generation
"""

import pytest
from typing import Any

from maven_pom_generator import build_sdk_context


# ============================================================================
# Context Structure Tests
# ============================================================================

def test_build_sdk_context_returns_dict(test_config: dict[str, Any]) -> None:
    """Verify that build_sdk_context returns a dictionary."""
    context = build_sdk_context('EMA', '2.4.0', 17, test_config)
    assert isinstance(context, dict)


def test_build_sdk_context_required_keys(test_config: dict[str, Any]) -> None:
    """Verify that all required keys are present in the context.
    
    The context must include all keys needed by the Jinja2 template:
    - api, apiversion, compat_jdk_version, compat_jfx_version
    - junitscope, namespace, transportapi, artifactid
    """
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


# ============================================================================
# API Type Tests
# ============================================================================

def test_build_sdk_context_ema_api(test_config: dict[str, Any]) -> None:
    """Verify that EMA API type is correctly preserved."""
    context = build_sdk_context('EMA', '2.4.0', 17, test_config)
    assert context['api'] == 'EMA'


def test_build_sdk_context_eta_api(test_config: dict[str, Any]) -> None:
    """Verify that ETA API type is correctly preserved."""
    context = build_sdk_context('ETA', '2.4.0', 17, test_config)
    assert context['api'] == 'ETA'


# ============================================================================
# Version Resolution Tests
# ============================================================================

def test_build_sdk_context_valid_version_resolution(test_config: dict[str, Any]) -> None:
    """Verify that valid RTSDK version is correctly resolved to Maven version.
    
    RTSDK 2.4.0 should resolve to Maven version 3.10.0.1
    """
    context = build_sdk_context('EMA', '2.4.0', 17, test_config)
    assert context['apiversion'] == '3.10.0.1'


def test_build_sdk_context_invalid_version_fallback(test_config: dict[str, Any]) -> None:
    """Verify that invalid RTSDK version falls back to latest version.
    
    When user provides a version not in the config (e.g., 9.9.9),
    the system should fall back to the latest_version from config.
    """
    context = build_sdk_context('EMA', '9.9.9', 17, test_config)
    # When invalid version used, it falls back to latest_version (the RTSDK key, not the resolved Maven version)
    assert context['apiversion'] == '2.4.0'  # latest_version


# ============================================================================
# JDK Version Tests
# ============================================================================

def test_build_sdk_context_jdk_version_preserved(test_config: dict[str, Any]) -> None:
    """Verify that JDK version is correctly preserved in context.
    
    Tests all supported JDK versions: 11, 17, 21, 25
    """
    for jdk in [11, 17, 21, 25]:
        context = build_sdk_context('EMA', '2.4.0', jdk, test_config)
        assert context['compat_jdk_version'] == jdk


# ============================================================================
# JavaFX Version Mapping Tests
# ============================================================================

def test_build_sdk_context_javafx_mapping_jdk11(test_config: dict[str, Any]) -> None:
    """Verify JavaFX version mapping for JDK 11: 17.0.19"""
    context = build_sdk_context('EMA', '2.4.0', 11, test_config)
    assert context['compat_jfx_version'] == '17.0.19'


def test_build_sdk_context_javafx_mapping_jdk17(test_config: dict[str, Any]) -> None:
    """Verify JavaFX version mapping for JDK 17: 21.0.11"""
    context = build_sdk_context('EMA', '2.4.0', 17, test_config)
    assert context['compat_jfx_version'] == '21.0.11'


def test_build_sdk_context_javafx_mapping_jdk21(test_config: dict[str, Any]) -> None:
    """Verify JavaFX version mapping for JDK 21: 21.0.11"""
    context = build_sdk_context('EMA', '2.4.0', 21, test_config)
    assert context['compat_jfx_version'] == '21.0.11'


def test_build_sdk_context_javafx_mapping_jdk25(test_config: dict[str, Any]) -> None:
    """Verify JavaFX version mapping for JDK 25: 25.0.3"""
    context = build_sdk_context('EMA', '2.4.0', 25, test_config)
    assert context['compat_jfx_version'] == '25.0.3'


# ============================================================================
# API-Specific Behavior Tests
# ============================================================================

def test_build_sdk_context_junit_scope_ema(test_config: dict[str, Any]) -> None:
    """Verify that EMA API uses test-scoped JUnit.
    
    EMA tests are typically run separately from the main application,
    so JUnit should be test-scoped.
    """
    context = build_sdk_context('EMA', '2.4.0', 17, test_config)
    assert context['junitscope'] == 'test'


def test_build_sdk_context_junit_scope_eta(test_config: dict[str, Any]) -> None:
    """Verify that ETA API uses compile-scoped JUnit.
    
    ETA examples may reference JUnit classes at runtime,
    so JUnit should be compile-scoped.
    """
    context = build_sdk_context('ETA', '2.4.0', 17, test_config)
    assert context['junitscope'] == 'compile'


# ============================================================================
# Namespace and Transport Tests
# ============================================================================

def test_build_sdk_context_namespace(test_config: dict[str, Any]) -> None:
    """Verify that Maven namespace (com.refinitiv) is resolved correctly."""
    context = build_sdk_context('EMA', '2.4.0', 17, test_config)
    assert context['namespace'] == 'com.refinitiv'


def test_build_sdk_context_transportapi(test_config: dict[str, Any]) -> None:
    """Verify that transport API (eta) is resolved correctly."""
    context = build_sdk_context('EMA', '2.4.0', 17, test_config)
    assert context['transportapi'] == 'eta'


# ============================================================================
# Artifact ID Tests
# ============================================================================

def test_build_sdk_context_artifact_id_format_ema(test_config: dict[str, Any]) -> None:
    """Verify that EMA artifact ID is correctly formatted as API_VERSION.
    
    Format: EMA_3.10.0.1 (EMA for API type, 3.10.0.1 for resolved Maven version)
    """
    context = build_sdk_context('EMA', '2.4.0', 17, test_config)
    assert context['artifactid'] == 'EMA_3.10.0.1'


def test_build_sdk_context_artifact_id_format_eta(test_config: dict[str, Any]) -> None:
    """Verify that ETA artifact ID is correctly formatted as API_VERSION."""
    context = build_sdk_context('ETA', '2.1.0', 17, test_config)
    assert context['artifactid'] == 'ETA_3.7.0.0'


# ============================================================================
# Version Resolution with Different RTSDK Versions
# ============================================================================

@pytest.mark.parametrize('version,expected_apiversion', [
    ('2.0.0', '3.6.0.0'),
    ('2.1.0', '3.7.0.0'),
    ('2.4.0', '3.10.0.1'),
])
def test_build_sdk_context_various_versions(test_config: dict[str, Any], version: str, expected_apiversion: str) -> None:
    """Test version resolution for various RTSDK versions.
    
    Validates that the version mapping is consistent across different
    RTSDK version numbers.
    """
    context = build_sdk_context('EMA', version, 17, test_config)
    assert context['apiversion'] == expected_apiversion
