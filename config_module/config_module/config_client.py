from datetime import datetime
import json
import grpc
from config_module.proto import config_pb2
from config_module.proto import config_pb2_grpc

from utils_module.type_convert import convert_date_type


def convert_dict(flat_dict):
    result = {}
    for key, value in flat_dict.items():
        parts = key.split('.')
        d = result
        for part in parts[:-1]:
            if part not in d:
                d[part] = {}
            d = d[part]
        d[parts[-1]] = value
    return result


class ConfigClient:
    def __init__(self, host: str, port: int):
        channel = grpc.insecure_channel(f'{host}:{port}')
        self.stub = config_pb2_grpc.ConfigServerStub(channel)

    def get_config_data(self, app_id: str) -> dict:
        res = self.stub.GetConfig(config_pb2.ConfigRequest(app_id=app_id))

        config_data = {}
        for r_c_d in res.config_data:
            config_data[r_c_d.key] = convert_date_type(r_c_d.value, r_c_d.type)

        config_data = convert_dict(config_data)
        return config_data
