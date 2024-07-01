import pymongo
from datetime import datetime


class ConfigLoader:
    def __init__(self, config_db_path: str, app_id: str,
                 db: str = 'admin', collection: str = 'app_config', start_recode_limit=10):
        client = pymongo.MongoClient(config_db_path)
        db = client[db]
        self.collection = db.get_collection(collection)
        self.start_recode_limit = start_recode_limit
        self.exclude_field = ['_id', 'app_start_datetime_list']
        config = self.get_config(app_id=app_id)
        self.name = config['app']['name']
        self.port = config['app']['port']

    def get_config(self, app_id: str) -> dict:
        updated_datetime = datetime.now()
        config = self.collection.find_one_and_update({'app_id': app_id},
                                                     {'$push': {
                                                         'app_start_datetime_list':
                                                             {
                                                                 '$each': [updated_datetime],
                                                                 '$position': 0,
                                                                 '$slice': self.start_recode_limit
                                                             }
                                                     }})
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

