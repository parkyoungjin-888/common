from config_module.config_client import ConfigClient


class ConfigSingleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(ConfigSingleton, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, '_config_loaded'):
            self._config = None
            self._config_loaded = False

    def load_config(self, host: str, port: int, app_id: str):
        _config_client = ConfigClient(host=host, port=port)
        self._config = _config_client.get_config_data(app_id=app_id)
        self._config_loaded = True

    def get_value(self, key):
        keys = key.split('.')
        value = self._config
        for k in keys:
            value = value.get(k)
            if value is None:
                return None
        return value
