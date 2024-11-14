from typing import List, Type
from beanie import Document, init_beanie
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient


class BaseDocument(Document):
    @classmethod
    async def find_with_paginate(cls, find_key: dict, sort: list[str] = None, project_model: Type[BaseModel] = None,
                                 page_size: int = None, page_num: int = None) -> List[dict]:
        default_sort = ['-_id'] if sort is None or ('+_id' not in sort and '-_id' not in sort) else []
        sort = sort + default_sort if sort is not None else default_sort
        cursor = cls.find(find_key, projection_model=project_model).sort(*sort)

        if page_size is not None:
            skip = page_size * (page_num - 1)
            cursor = cursor.skip(skip).limit(page_size)

        doc_list = await cursor.to_list()
        doc_list = [doc.model_dump(by_alias=True) for doc in doc_list]
        return doc_list

    @classmethod
    async def delete_many(cls, find_key: dict) -> int:
        result = await cls.find(find_key).delete()
        return result.deleted_count

    @classmethod
    async def get_aggregate_result(cls, pipeline: list[dict]):
        return await cls.aggregate(pipeline).to_list()


class BeanieControl:
    def __init__(self, db: str, db_id: str, db_pw: str, server_urls: list[str], replica_name: str = 'rs0'):
        self.db = db
        server_urls_str = ','.join(server_urls)
        self.db_url = f'mongodb://{db_id}:{db_pw}@{server_urls_str}/?replicaSet={replica_name}'

    async def init(self, data_model_list: list[Type[BaseDocument]]):
        client = AsyncIOMotorClient(self.db_url)
        await init_beanie(database=client[self.db], document_models=data_model_list)
