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


import sys
import os
import yaml
from jinja2 import Environment, FileSystemLoader

config_file_path = './config/rtsdk_versions.yaml'
template_folder = './templates/'
template_file = 'rtsdk_maven_pom_xml.txt'
output_file_path = './output/pom.xml'

api = 'EMA'
rtsdkversion = '3.9.0.1'
compat_jdk_version = '17'
junitscope = 'test'
namespace = 'com.refinitiv'
transportapi = 'eta'

sdk_information = {
    'api': 'ETA',
    'rtsdkversion': '3.8.3.0',
    'compat_jdk_version': 17,
    'junitscope': '',
    'namespace': 'com.refinitiv',
    'transportapi': 'eta',
    'artifactid': ''
}

if __name__ == '__main__':
    try:
        environment = Environment(loader=FileSystemLoader(template_folder))
        template = environment.get_template(template_file)
        sdk_information['artifactid'] = f'{sdk_information["api"]}_{sdk_information["rtsdkversion"]}'

        if sdk_information['api'] == 'ETA':
            sdk_information['junitscope'] = 'compile'
        else:
            sdk_information['junitscope'] = 'test'

        content = template.render(
            sdk_information
        )
        with open(output_file_path, 'w', encoding='utf-8') as pom_file:
            pom_file.write(content)
            print(f'... wrote {output_file_path}')

    except FileNotFoundError:
        print('Error: Config File not found')
    except UnicodeDecodeError:
        print('Error: Config File decoding error')
