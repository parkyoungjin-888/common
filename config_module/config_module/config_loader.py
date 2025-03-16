import pymongo
from datetime import datetime


class ConfigLoader:
    def __init__(self, config_db_path: str, db: str = 'app', collection: str = 'config'):
        client = pymongo.MongoClient(config_db_path)
        db = client[db]
        self.collection = db.get_collection(collection)
        self.exclude_field = ['_id']

    def get_config(self, app_id: str) -> dict:
        config = self.collection.find_one({'app_id': app_id})
        return config if config is not None else {}

    def unpack_config(self, config: dict, parent_key: str = '') -> list[dict]:
        flatten_config = []
        for key, value in config.items():
            if key in self.exclude_field:
                continue

            new_key = f'{parent_key}.{key}' if parent_key else key
            if isinstance(value, dict):
                flatten_config.extend(self.unpack_config(value, new_key))
            else:
                flatten_config.append({'key': new_key, 'value': str(value), 'type': type(value).__name__})
        return flatten_config

