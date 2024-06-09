from datetime import datetime, timedelta, timezone
import pandas as pd
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS


class InfluxDbControl:
    def __init__(self, host: str, port: int, org: str, token: str):
        _url = f'http://{host}:{port}'
        self._client = InfluxDBClient(url=_url, org=org, token=token)
        self._buckets_api = self._client.buckets_api()
        self._write_api = self._client.write_api(write_options=SYNCHRONOUS)
        self._query_api = self._client.query_api()
        self._delete_api = self._client.delete_api()

    def close(self):
        self._client.close()

    def get_bucket_list(self):
        buckets = self._buckets_api.find_buckets().buckets
        bucket_name_list = []
        for bucket in buckets:
            bucket_name_list.append(bucket.name)
        return bucket_name_list

    def insert_data(self, bucket: str, measurement: str, 
                    data_list: list[list[float]], datetime_list: list[datetime],
                    column_list: list[str], tag_data: dict = {}):
        df = pd.DataFrame(data=data_list, columns=column_list,)
        df['timestamp'] = [dt.timestamp() * 1000 for dt in datetime_list]
        df.set_index('timestamp', inplace=True)
        df.index = pd.to_datetime(df.index, unit='ms')

        tag_column_list = []
        for tag_key, tag_value in tag_data.items():
            df[tag_key] = tag_value
            tag_column_list.append(tag_key)

        with self._write_api as writer:
            writer.write(bucket=bucket, record=df, data_frame_measurement_name=measurement, data_frame_tag_columns=tag_column_list)

    def read_data(self, bucket: str, measurement: str,
                  start_datetime: datetime, end_datetime: datetime, tag_data: dict = {}):
        start = int(start_datetime.astimezone(timezone.utc).timestamp())
        stop = int(end_datetime.astimezone(timezone.utc).timestamp())
        query = f'from(bucket: "{bucket}") ' \
                f'|> range(start: {start}, stop: {stop}) ' \
                f'|> filter(fn: (r) => r._measurement == "{measurement}") '
        for tag_key, tag_value in tag_data.items():
            query += f'|> filter(fn: (r) => r.{tag_key} == "{tag_value}") '
        query += f'|> aggregateWindow(every: 1s, fn: mean, createEmpty: false)'
        df = self._query_api.query_data_frame(query=query)
        return df
    
    def delete_data(self, bucket: str, measurement: str,
                    start_datetime: datetime, end_datetime: datetime, 
                    tag_data: dict = {}):
        predicate = f'_measurement={measurement}'
        for tag_key, tag_value in tag_data.items():
            predicate += f' AND {tag_key}={tag_value}'

        self._delete_api.delete(start=start_datetime, stop=end_datetime, predicate=predicate, bucket=bucket)
