from config_module.config_client import ConfigClient


if __name__ == '__main__':
    config_client = ConfigClient('192.168.0.104', 31001)

    config_data = config_client.get_config_data('test_app_id')

    print('end')
