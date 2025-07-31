import yaml

config_file_path = './config/rtsdk_versions.yaml'

if __name__ == '__main__':
    try:
        with open(config_file_path, 'r', encoding='utf-8') as config_file:
            config_data = yaml.safe_load(config_file)

        print(f'RTSDK latest version is {config_data["latest_version"]}')
        print(f'Supported JDK version is {config_data["support_jdk_version"]}')
        print(f'Namespace is is {config_data["namespace"]["refinitiv"]}')

        rtsdk_versions = config_data["rtsdk_versions"]
        for rtsdk_version, ema_version in rtsdk_versions.items():
            print(f'RTSDK version {rtsdk_version} === EMA version {ema_version}')
    except FileNotFoundError:
        print('Error: Config File not found')
    except UnicodeDecodeError:
        print('Error: Config File decoding error')
