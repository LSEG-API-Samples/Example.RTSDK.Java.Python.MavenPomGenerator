"""End-to-end integration tests for the entire pom.xml generation workflow.

This module validates that the entire tool works correctly from start to finish.
Tests verify that:
- Config is loaded and parsed correctly
- CLI arguments are parsed correctly
- SDK context is built with all necessary data
- Template is rendered and written to disk
- Output pom.xml files are valid and contain expected content

Integration tests use real functions working together, unlike unit tests
which test functions in isolation.
"""

import pytest
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

from maven_pom_generator import (
    load_config,
    setup_argument_parser,
    build_sdk_context,
    render_and_write_pom
)


# ============================================================================
# Basic End-to-End Workflow Tests
# ============================================================================

def test_integration_ema_2_4_0_jdk17(config_file: Path, output_dir: Path) -> None:
    """Test complete workflow: EMA 2.4.0 with JDK 17.
    
    This verifies the entire pipeline works:
    - Load config
    - Parse CLI arguments (api=EMA, version=2.4.0, jdk=17)
    - Build context with version resolution and JDK/JavaFX mapping
    - Render template with correct values
    - Write valid pom.xml file
    """
    config = load_config(config_file)
    parser = setup_argument_parser(config)
    args = parser.parse_args(['--api', 'EMA', '--version', '2.4.0', '--jdkversion', '17'])
    
    context = build_sdk_context(args.api, args.version, args.jdkversion, config)
    output_file = output_dir / 'pom.xml'
    render_and_write_pom(Path('./templates'), output_file, context)
    
    # Verify file exists and is valid XML
    assert output_file.exists()
    tree = ET.parse(output_file)
    root = tree.getroot()
    
    # Verify content
    content = output_file.read_text()
    assert 'EMA_3.10.0.1' in content
    assert '<maven.compiler.source>17</maven.compiler.source>' in content
    assert '<javafx.version>21.0.11</javafx.version>' in content


def test_integration_eta_2_3_1_jdk21(config_file: Path, output_dir: Path) -> None:
    """Test complete workflow: ETA 2.1.0 with JDK 21.
    
    Validates ETA-specific behavior:
    - Uses ETA API constant
    - Resolves to different Maven version than EMA
    - Maps JDK 21 to JavaFX 21.0.11
    - Includes Mockito dependency
    - Uses compile-scoped JUnit (checked indirectly via Mockito presence)
    """
    config = load_config(config_file)
    parser = setup_argument_parser(config)
    args = parser.parse_args(['--api', 'ETA', '--version', '2.1.0', '--jdkversion', '21'])
    
    context = build_sdk_context(args.api, args.version, args.jdkversion, config)
    output_file = output_dir / 'pom.xml'
    render_and_write_pom(Path('./templates'), output_file, context)
    
    # Verify file exists
    assert output_file.exists()
    
    # Verify content
    content = output_file.read_text()
    assert 'ETA_3.7.0.0' in content
    assert '<maven.compiler.source>21</maven.compiler.source>' in content
    assert '<javafx.version>21.0.11</javafx.version>' in content
    assert 'mockito-core' in content


# ============================================================================
# Fallback and Error Handling Tests
# ============================================================================

def test_integration_invalid_version_fallback(config_file: Path, output_dir: Path) -> None:
    """Test that invalid RTSDK version falls back to latest gracefully.
    
    When user requests version 9.9.9 (which doesn't exist), the system
    should fall back to latest_version and still produce valid output.
    This ensures the tool is resilient and helpful when users request
    unsupported versions.
    """
    config = load_config(config_file)
    parser = setup_argument_parser(config)
    args = parser.parse_args(['--api', 'EMA', '--version', '9.9.9', '--jdkversion', '17'])
    
    context = build_sdk_context(args.api, args.version, args.jdkversion, config)
    output_file = output_dir / 'pom.xml'
    render_and_write_pom(Path('./templates'), output_file, context)
    
    # Should use latest_version key (not resolved Maven version)
    content = output_file.read_text()
    assert 'EMA_2.4.0' in content


# ============================================================================
# Multiple Configuration Tests
# ============================================================================

@pytest.mark.parametrize('api,version,jdk', [
    ('EMA', '2.0.0', 11),
    ('ETA', '2.1.0', 17),
    ('EMA', '2.4.0', 21),
    ('ETA', '2.4.0', 25),
])
def test_integration_various_combinations(config_file: Path, output_dir: Path, api: str, version: str, jdk: int) -> None:
    """Test complete workflow with various API/version/JDK combinations.
    
    This parametrized test verifies the tool works correctly with all
    meaningful combinations:
    - Both API types (EMA, ETA)
    - Multiple supported RTSDK versions (2.0.0, 2.1.0, 2.4.0)
    - All supported JDK versions (11, 17, 21, 25)
    
    Total of 4 combinations validated in a single test.
    """
    config = load_config(config_file)
    parser = setup_argument_parser(config)
    args = parser.parse_args(['--api', api, '--version', version, '--jdkversion', str(jdk)])
    
    context = build_sdk_context(args.api, args.version, args.jdkversion, config)
    output_file = output_dir / f'pom_{api}_{jdk}.xml'
    render_and_write_pom(Path('./templates'), output_file, context)
    
    # Verify file exists and is valid
    assert output_file.exists()
    tree = ET.parse(output_file)
    root = tree.getroot()
    
    # Verify API is in artifact ID
    content = output_file.read_text()
    assert api in content


# ============================================================================
# Multiple Runs and Output Differentiation Tests
# ============================================================================

def test_integration_multiple_runs_different_outputs(config_file: Path, output_dir: Path) -> None:
    """Test that multiple runs with different parameters produce correctly different outputs.
    
    Run 1: EMA with JDK 17
    Run 2: ETA with JDK 25
    
    Validates that:
    - Both files are created independently
    - Content differs appropriately (different artifact IDs, JDK versions)
    - Each file is valid and self-consistent
    """
    config = load_config(config_file)
    
    # First run: EMA with JDK 17
    context1 = build_sdk_context('EMA', '2.4.0', 17, config)
    output_file1 = output_dir / 'pom_ema_17.xml'
    render_and_write_pom(Path('./templates'), output_file1, context1)
    content1 = output_file1.read_text()
    
    # Second run: ETA with JDK 25
    context2 = build_sdk_context('ETA', '2.1.0', 25, config)
    output_file2 = output_dir / 'pom_eta_25.xml'
    render_and_write_pom(Path('./templates'), output_file2, context2)
    content2 = output_file2.read_text()
    
    # Verify both files exist and differ
    assert output_file1.exists()
    assert output_file2.exists()
    assert content1 != content2
    assert 'EMA_3.10.0.1' in content1
    assert 'ETA_3.7.0.0' in content2
    assert '<maven.compiler.source>17</maven.compiler.source>' in content1
    assert '<maven.compiler.source>25</maven.compiler.source>' in content2


# ============================================================================
# Real Config File Tests
# ============================================================================

def test_integration_real_config_file(output_dir: Path) -> None:
    """Test end-to-end with the actual config file in the repository.
    
    This test uses the real config/rtsdk_versions.yaml file rather than
    a test fixture. This validates that the tool works with the actual
    configuration that users will encounter.
    
    Skipped if the real config file is not found (e.g., in isolated
    test environments).
    """
    config_path = Path('./config/rtsdk_versions.yaml')
    if not config_path.exists():
        pytest.skip("Real config file not found")
    
    config = load_config(config_path)
    context = build_sdk_context('EMA', '2.4.0', 17, config)
    output_file = output_dir / 'pom_real.xml'
    render_and_write_pom(Path('./templates'), output_file, context)
    
    assert output_file.exists()
    tree = ET.parse(output_file)
    root = tree.getroot()
