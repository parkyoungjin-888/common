import pymongo
from datetime import datetime


class ConfigLoader:
    def __init__(self, config_path: str, app_name: str, start_recode_count=10):
        client = pymongo.MongoClient(config_path)
        db = client["admin"]
        self.collection = db.get_collection('app_config')
        self.config = self.collection.find_one({'app_name': app_name})
        if self.config is not None:
            updated_datetime = datetime.now()
            if 'app_start_datetime_list' in self.config.keys():
                app_start_datetime_list = self.config['app_start_datetime_list']
                app_start_datetime_list.append(updated_datetime)
                if len(app_start_datetime_list) > start_recode_count:
                    remain_start_index = len(app_start_datetime_list) - start_recode_count
                    del app_start_datetime_list[0:remain_start_index]
            else:
                app_start_datetime_list = [updated_datetime]

            update_result = self.collection.update_one({'app_name': app_name},
                                                       {"$set": {'app_start_datetime_list': app_start_datetime_list}})

            if update_result.modified_count != 1:
                print(f'ERROR : config app_start_datetime_list update is strange,'
                      f' update_count : {update_result.modified_count}')

    def get_config(self):
        return self.config if self.config is not None else {}
