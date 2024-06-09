from enum import Enum
from config_loader import ConfigLoader


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class ConfigDataType(Enum):
    DEFAULT = None
    STR = 1
    INT = 2
    FLOAT = 3
    BOOL = 4


def convert_value_type(value, data_type: ConfigDataType):
    if data_type == ConfigDataType.DEFAULT:
        return value
    elif data_type == ConfigDataType.STR:
        return str(value)
    elif data_type == ConfigDataType.INT:
        return int(value)
    elif data_type == ConfigDataType.FLOAT:
        return float(value)
    elif data_type == ConfigDataType.BOOL:
        return bool(value)
    else:
        print('unknown ConfigDataType')
        return value


class AppConfig:
    def __init__(self, config_path='', app_name=''):
        _config_loader = ConfigLoader(config_path=config_path,
                                      app_name=app_name)
        self._conifg = _config_loader.get_config()

    def get_value(self, section: str, option: str, data_type=ConfigDataType.DEFAULT):
        if section in self._conifg.keys() and option in self._conifg[section].keys():
            value = self._conifg[section][option]
            if data_type is not None:
                try:
                    value = convert_value_type(value, data_type)
                except Exception as e:
                    print(e)
            return value


class AppConfigSingleton(AppConfig, metaclass=Singleton):
    pass
