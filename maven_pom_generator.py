# |-----------------------------------------------------------------------------
# |            This source code is provided under the MIT license             --
# |  and is provided AS IS with no warranty or guarantee of fit for purpose.  --
# |                See the project's LICENSE.md for details.                  --
# |           Copyright LSEG 2026.       All rights reserved.                 --
# |-----------------------------------------------------------------------------

"""
RTSDK Java Maven pom.xml generator.

Generates Maven pom.xml configuration files for RTSDK Java (EMA/ETA) applications
based on version, JDK compatibility, and API selection. Supports RTSDK versions
2.0.0.L1 and later.
"""

import argparse
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml
from jinja2 import Environment, FileSystemLoader, TemplateNotFound


@dataclass
class Config:
    """Configuration paths for the generator."""

    config_file: Path = Path('./config/rtsdk_versions.yaml')
    template_folder: Path = Path('./templates')
    template_file: str = 'rtsdk_maven_pom_xml.txt'
    output_file: Path = Path('./output/pom.xml')

def load_config(config_path: Path) -> dict[str, Any]:
    """Load RTSDK configuration from YAML file.
    
    Args:
        config_path: Path to the rtsdk_versions.yaml config file
        
    Returns:
        Dictionary containing version mappings, supported JDKs, and JavaFX versions
        
    Raises:
        FileNotFoundError: If config file does not exist
        UnicodeDecodeError: If file cannot be decoded as UTF-8
    """
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def setup_argument_parser(config: dict[str, Any]) -> argparse.ArgumentParser:
    """Set up command-line argument parser.
    
    Args:
        config: Configuration dictionary with supported versions and JDKs
        
    Returns:
        Configured ArgumentParser instance
    """
    supported_jdk_jfx = config.get('support_jdk_jfx_versions', {})
    supported_jdks = list(supported_jdk_jfx.keys())
    latest_version = config.get('latest_version', '')
    
    parser = argparse.ArgumentParser(
        prog='RTSDK Java Maven pom.xml generator',
        description='Generate Maven pom.xml for ETA and EMA APIs',
        epilog='This tool provides as is only, no support'
    )
    parser.add_argument(
        '--api',
        type=str,
        default='EMA',
        choices=['EMA', 'ETA'],
        help='API type: EMA or ETA (default: EMA)'
    )
    parser.add_argument(
        '--version',
        type=str,
        default=latest_version,
        help=f'RTSDK Java version (default: {latest_version})'
    )
    parser.add_argument(
        '--jdkversion',
        type=int,
        default=17,
        choices=supported_jdks,
        help=f'JDK version: {supported_jdks} (default: 17)'
    )
    return parser


def build_sdk_context(
    api: str,
    input_version: str,
    jdk_version: int,
    config: dict[str, Any]
) -> dict[str, Any]:
    """Build SDK information context for template rendering.
    
    Args:
        api: API type (EMA or ETA)
        input_version: Requested RTSDK version
        jdk_version: Requested JDK version
        config: Configuration dictionary
        
    Returns:
        Dictionary with resolved SDK information
    """
    available_versions = config.get('rtsdk_versions', {})
    supported_jdk_jfx = config.get('support_jdk_jfx_versions', {})
    latest_version = config.get('latest_version', '')
    
    # Resolve RTSDK version (fallback to latest if not found)
    if input_version not in available_versions:
        api_version = latest_version
        print(f'Version not found; using latest: {latest_version}')
    else:
        api_version = available_versions[input_version]
        print(f'API version: {api_version}')
    
    # Resolve JavaFX version
    javafx_version = supported_jdk_jfx[jdk_version]
    print(f'Java SDK: {jdk_version}')
    print(f'JavaFX SDK: {javafx_version}')
    
    # Determine JUnit scope based on API
    junit_scope = 'compile' if api == 'ETA' else 'test'
    
    return {
        'api': api,
        'apiversion': api_version,
        'compat_jdk_version': jdk_version,
        'compat_jfx_version': javafx_version,
        'junitscope': junit_scope,
        'namespace': config['namespace']['refinitiv'],
        'transportapi': config['transportapi']['refinitiv'],
        'artifactid': f'{api}_{api_version}'
    }


def render_and_write_pom(
    template_path: Path,
    output_path: Path,
    context: dict[str, Any]
) -> None:
    """Render Jinja2 template and write pom.xml file.
    
    Args:
        template_path: Path to template folder
        output_path: Path where pom.xml will be written
        context: Context dictionary for template rendering
        
    Raises:
        TemplateNotFound: If template file cannot be found
    """
    env = Environment(loader=FileSystemLoader(template_path))
    template = env.get_template('rtsdk_maven_pom_xml.txt')
    content = template.render(context)
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content, encoding='utf-8')
    print(f'Generated: {output_path}')


def main() -> None:
    """Main entry point for the pom.xml generator."""
    config_obj = Config()
    
    try:
        config = load_config(config_obj.config_file)
        parser = setup_argument_parser(config)
        args = parser.parse_args()
        
        sdk_context = build_sdk_context(
            args.api,
            args.version,
            args.jdkversion,
            config
        )
        
        render_and_write_pom(
            config_obj.template_folder,
            config_obj.output_file,
            sdk_context
        )
    except FileNotFoundError as e:
        print(f'Error: Config file not found: {e}')
    except UnicodeDecodeError:
        print('Error: Config file encoding error (expected UTF-8)')
    except TemplateNotFound as e:
        print(f'Error: Template not found: {e}')
    except KeyError as e:
        print(f'Error: Missing config key: {e}')


if __name__ == '__main__':
    main()

