"""End-to-end integration tests for the entire pom.xml generation workflow."""

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


def test_integration_ema_2_4_0_jdk17(config_file: Path, output_dir: Path) -> None:
    """Test end-to-end: EMA 2.4.0 with JDK 17."""
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
    """Test end-to-end: ETA 2.3.1 with JDK 21."""
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


def test_integration_invalid_version_fallback(config_file: Path, output_dir: Path) -> None:
    """Test end-to-end: Invalid version falls back to latest."""
    config = load_config(config_file)
    parser = setup_argument_parser(config)
    args = parser.parse_args(['--api', 'EMA', '--version', '9.9.9', '--jdkversion', '17'])
    
    context = build_sdk_context(args.api, args.version, args.jdkversion, config)
    output_file = output_dir / 'pom.xml'
    render_and_write_pom(Path('./templates'), output_file, context)
    
    # Should use latest_version key (not resolved Maven version)
    content = output_file.read_text()
    assert 'EMA_2.4.0' in content


@pytest.mark.parametrize('api,version,jdk', [
    ('EMA', '2.0.0', 11),
    ('ETA', '2.1.0', 17),
    ('EMA', '2.4.0', 21),
    ('ETA', '2.4.0', 25),
])
def test_integration_various_combinations(config_file: Path, output_dir: Path, api: str, version: str, jdk: int) -> None:
    """Test end-to-end with various API/version/JDK combinations."""
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


def test_integration_multiple_runs_different_outputs(config_file: Path, output_dir: Path) -> None:
    """Test that multiple runs produce different outputs correctly."""
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


def test_integration_real_config_file(output_dir: Path) -> None:
    """Test end-to-end with the actual config file."""
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
