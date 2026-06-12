"""Tests for template rendering and pom.xml generation."""

import pytest
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

from maven_pom_generator import render_and_write_pom


def test_render_and_write_pom_creates_output_dir(output_dir: Path, test_config: dict[str, Any]) -> None:
    """Test that render_and_write_pom creates output directory."""
    output_file = output_dir / 'pom.xml'
    context = {
        'api': 'EMA',
        'apiversion': '3.10.0.1',
        'compat_jdk_version': 17,
        'compat_jfx_version': '21.0.11',
        'junitscope': 'test',
        'namespace': 'com.refinitiv',
        'transportapi': 'eta',
        'artifactid': 'EMA_3.10.0.1'
    }
    render_and_write_pom(Path('./templates'), output_file, context)
    assert output_file.parent.exists()


def test_render_and_write_pom_creates_file(output_dir: Path, test_config: dict[str, Any]) -> None:
    """Test that render_and_write_pom creates pom.xml file."""
    output_file = output_dir / 'pom.xml'
    context = {
        'api': 'EMA',
        'apiversion': '3.10.0.1',
        'compat_jdk_version': 17,
        'compat_jfx_version': '21.0.11',
        'junitscope': 'test',
        'namespace': 'com.refinitiv',
        'transportapi': 'eta',
        'artifactid': 'EMA_3.10.0.1'
    }
    render_and_write_pom(Path('./templates'), output_file, context)
    assert output_file.exists()
    assert output_file.stat().st_size > 0


def test_render_and_write_pom_produces_valid_xml(output_dir: Path) -> None:
    """Test that render_and_write_pom produces valid XML."""
    output_file = output_dir / 'pom.xml'
    context = {
        'api': 'EMA',
        'apiversion': '3.10.0.1',
        'compat_jdk_version': 17,
        'compat_jfx_version': '21.0.11',
        'junitscope': 'test',
        'namespace': 'com.refinitiv',
        'transportapi': 'eta',
        'artifactid': 'EMA_3.10.0.1'
    }
    render_and_write_pom(Path('./templates'), output_file, context)
    
    # Try to parse as XML
    tree = ET.parse(output_file)
    root = tree.getroot()
    assert root is not None


def test_render_and_write_pom_ema_groupid(output_dir: Path) -> None:
    """Test that EMA pom.xml has correct groupId."""
    output_file = output_dir / 'pom.xml'
    context = {
        'api': 'EMA',
        'apiversion': '3.10.0.1',
        'compat_jdk_version': 17,
        'compat_jfx_version': '21.0.11',
        'junitscope': 'test',
        'namespace': 'com.refinitiv',
        'transportapi': 'eta',
        'artifactid': 'EMA_3.10.0.1'
    }
    render_and_write_pom(Path('./templates'), output_file, context)
    
    tree = ET.parse(output_file)
    root = tree.getroot()
    ns = {'pom': 'http://maven.apache.org/POM/4.0.0'}
    groupid = root.find('pom:groupId', ns)
    assert groupid is not None
    assert 'com.refinitiv.ema' in groupid.text


def test_render_and_write_pom_eta_groupid(output_dir: Path) -> None:
    """Test that ETA pom.xml has correct groupId."""
    output_file = output_dir / 'pom.xml'
    context = {
        'api': 'ETA',
        'apiversion': '3.10.0.1',
        'compat_jdk_version': 17,
        'compat_jfx_version': '21.0.11',
        'junitscope': 'compile',
        'namespace': 'com.refinitiv',
        'transportapi': 'eta',
        'artifactid': 'ETA_3.10.0.1'
    }
    render_and_write_pom(Path('./templates'), output_file, context)
    
    tree = ET.parse(output_file)
    root = tree.getroot()
    ns = {'pom': 'http://maven.apache.org/POM/4.0.0'}
    groupid = root.find('pom:groupId', ns)
    assert groupid is not None
    assert 'com.refinitiv' in groupid.text


def test_render_and_write_pom_jdk_version(output_dir: Path) -> None:
    """Test that generated pom.xml has correct JDK version."""
    output_file = output_dir / 'pom.xml'
    context = {
        'api': 'EMA',
        'apiversion': '3.10.0.1',
        'compat_jdk_version': 21,
        'compat_jfx_version': '21.0.11',
        'junitscope': 'test',
        'namespace': 'com.refinitiv',
        'transportapi': 'eta',
        'artifactid': 'EMA_3.10.0.1'
    }
    render_and_write_pom(Path('./templates'), output_file, context)
    
    content = output_file.read_text()
    assert '<maven.compiler.source>21</maven.compiler.source>' in content
    assert '<maven.compiler.target>21</maven.compiler.target>' in content


def test_render_and_write_pom_ema_has_javafx(output_dir: Path) -> None:
    """Test that EMA pom.xml includes JavaFX dependencies."""
    output_file = output_dir / 'pom.xml'
    context = {
        'api': 'EMA',
        'apiversion': '3.10.0.1',
        'compat_jdk_version': 17,
        'compat_jfx_version': '21.0.11',
        'junitscope': 'test',
        'namespace': 'com.refinitiv',
        'transportapi': 'eta',
        'artifactid': 'EMA_3.10.0.1'
    }
    render_and_write_pom(Path('./templates'), output_file, context)
    
    content = output_file.read_text()
    assert 'javafx-fxml' in content
    assert 'javafx-controls' in content


def test_render_and_write_pom_eta_has_mockito(output_dir: Path) -> None:
    """Test that ETA pom.xml includes Mockito dependency."""
    output_file = output_dir / 'pom.xml'
    context = {
        'api': 'ETA',
        'apiversion': '3.10.0.1',
        'compat_jdk_version': 17,
        'compat_jfx_version': '21.0.11',
        'junitscope': 'compile',
        'namespace': 'com.refinitiv',
        'transportapi': 'eta',
        'artifactid': 'ETA_3.10.0.1'
    }
    render_and_write_pom(Path('./templates'), output_file, context)
    
    content = output_file.read_text()
    assert 'mockito-core' in content


@pytest.mark.parametrize('jdk,expected_javafx', [
    (11, '17.0.19'),
    (17, '21.0.11'),
    (21, '21.0.11'),
    (25, '25.0.3'),
])
def test_render_and_write_pom_javafx_versions(output_dir: Path, jdk: int, expected_javafx: str) -> None:
    """Test JavaFX version in generated pom.xml."""
    output_file = output_dir / 'pom.xml'
    context = {
        'api': 'EMA',
        'apiversion': '3.10.0.1',
        'compat_jdk_version': jdk,
        'compat_jfx_version': expected_javafx,
        'junitscope': 'test',
        'namespace': 'com.refinitiv',
        'transportapi': 'eta',
        'artifactid': 'EMA_3.10.0.1'
    }
    render_and_write_pom(Path('./templates'), output_file, context)
    
    content = output_file.read_text()
    assert f'<javafx.version>{expected_javafx}</javafx.version>' in content
