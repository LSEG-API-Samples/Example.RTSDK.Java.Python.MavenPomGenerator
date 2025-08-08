# |-----------------------------------------------------------------------------
# |            This source code is provided under the MIT license             --
# |  and is provided AS IS with no warranty or guarantee of fit for purpose.  --
# |                See the project's LICENSE.md for details.                  --
# |           Copyright LSEG 2025.       All rights reserved.                 --
# |-----------------------------------------------------------------------------

# Example Code Disclaimer:
# ALL EXAMPLE CODE IS PROVIDED ON AN “AS IS” AND “AS AVAILABLE” BASIS FOR ILLUSTRATIVE PURPOSES ONLY. REFINITIV MAKES NO REPRESENTATIONS OR
# WARRANTIES OF ANY KIND, EXPRESS OR IMPLIED, AS TO THE OPERATION OF THE EXAMPLE CODE, OR THE INFORMATION, CONTENT,
# OR MATERIALS USED IN CONNECTION # WITH THE EXAMPLE CODE. YOU EXPRESSLY AGREE THAT YOUR USE OF THE EXAMPLE CODE IS AT YOUR SOLE RISK.


import os
import argparse
import yaml
from jinja2 import Environment, FileSystemLoader, TemplateNotFound

# Constants
config_file_path = './config/rtsdk_versions.yaml'
template_folder = './templates/'
template_file = 'rtsdk_maven_pom_xml.txt'
output_file_path = './output/pom.xml'

# Default SDK information
sdk_information = {
    'api': 'EMA',
    'apiversion': '',
    'compat_jdk_version': 17,
    'junitscope': '',
    'namespace': 'com.refinitiv',
    'transportapi': 'eta',
    'artifactid': ''
}

if __name__ == '__main__':
    try:
        # Load template file
        environment = Environment(loader=FileSystemLoader(template_folder))
        template = environment.get_template(template_file)

        # Load RTSDK config from YAML file
        with open(config_file_path, 'r', encoding='utf-8') as config_file:
            config_data = yaml.safe_load(config_file)

        # some data from YAML file for use
        latest_version = config_data.get('latest_version')
        available_versions = config_data.get('rtsdk_versions', {})
        supported_jdks = config_data.get('support_jdk_versions', {})

        # Populate Command Line arguments
        parser = argparse.ArgumentParser(
            prog='RTSDK Java Maven pom.xml generator',
            description='A Python file to generate Maven pom.xml file for ETA and EMA APIs',
            epilog='This tool provides as is only, no support'
        )
        parser.add_argument('--api', type=str,
                            help='EMA or ETA  [optional]',
                            default='EMA', choices=['EMA', 'ETA'])
        parser.add_argument('--version', type=str,
                            help='RTSDK Java version [optional]',
                            default=latest_version)
        parser.add_argument('--jdkversion', type=int,
                            help=f'Set JDK version (supported {supported_jdks}) [optional]',
                            default=17, choices=supported_jdks)

        args = parser.parse_args()
        sdk_information['api'] = args.api
        input_version = args.version
        jdk_version = args.jdkversion

        # Set sdk_information
        # Set version
        if input_version not in available_versions:
            sdk_information['apiversion'] = latest_version
            print(
                f'not found the version, use latest version {latest_version}')
        else:
            sdk_information['apiversion'] = available_versions[input_version]
            print(f'API version is {sdk_information["apiversion"]}')

        # Set compat JDK
        sdk_information['compat_jdk_version'] = jdk_version
        print(f'Use Java SDK {jdk_version}')
        # Set namespace and transport api
        sdk_information['namespace'] = config_data['namespace']['refinitiv']
        sdk_information['transportapi'] = config_data['transportapi']['refinitiv']
        # Set pom artifactid
        sdk_information['artifactid'] = f'{sdk_information["api"]}_{sdk_information["apiversion"]}'
        # set junit
        sdk_information['junitscope'] = 'compile' if sdk_information['api'] == 'ETA' else 'test'

        # apply content to template
        content = template.render(
            sdk_information
        )
        # write pom.xml file
        os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
        with open(output_file_path, 'w', encoding='utf-8') as pom_file:
            pom_file.write(content)
            print(f'Done creating {output_file_path}')
    except TemplateNotFound:
        print('Error: pom.xml file template not found')
    except FileNotFoundError:
        print('Error: Config File not found')
    except UnicodeDecodeError:
        print('Error: Config File decoding error')
