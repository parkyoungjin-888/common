import asyncio
import grpc
import json
from datetime import datetime
from functools import wraps
from google.protobuf.json_format import MessageToDict
from google.protobuf import struct_pb2
from mongodb_module.proto import collection_pb2 as pb2
from mongodb_module.proto import collection_pb2_grpc
from pydantic import BaseModel


convert_map = {
    'str': str,
    'int': int,
    'float': float,
    'bool': bool,
    'list': lambda x: json.loads(x.replace("'", '"')),
    'datetime': (lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S.%f')),
    'ObjectId': str
}


def grpc_client_error_handler(response):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                func_response = await func(*args, **kwargs)
                return func_response
            except grpc.aio.AioRpcError as e:
                print(f'{func.__name__} gRPC Error: {e.code()} - {e.details()}')
                response.code = 400
                response.message = f'{func.__name__} gRPC Error: {e.code()} - {e.details()}'
                return MessageToDict(response, preserving_proto_field_name=True)
            except Exception as e:
                print(f'{func.__name__} Error: {str(e)}')
                response.code = 500
                response.message = f'{func.__name__} Error: {str(e)}'
                return MessageToDict(response, preserving_proto_field_name=True)
        return wrapper
    return decorator


class CollectionClient:
    def __init__(self, host: str, port: int, collection_model: type[BaseModel]):
        self.channel = grpc.aio.insecure_channel(f'{host}:{port}')
        self.stub = collection_pb2_grpc.CollectionServerStub(self.channel)
        self.collection_model = collection_model

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.channel.close()

    @grpc_client_error_handler(pb2.IdResponse())
    async def insert_one(self, doc_req: pb2.DocRequest) -> dict:
        res = await self.stub.InsertOne(doc_req)
        res = MessageToDict(res, preserving_proto_field_name=True)
        return res

    @grpc_client_error_handler(pb2.IdListResponse())
    async def insert_many(self, doc_list_req: pb2.DocListRequest) -> dict:
        res = await self.stub.InsertMany(doc_list_req)
        res = MessageToDict(res, preserving_proto_field_name=True)
        return res

    @grpc_client_error_handler(pb2.DocResponse())
    async def get_tag(self, query_req: pb2.DocResponse) -> dict:
        res = await self.stub.GetTag(query_req)
        res = MessageToDict(res, preserving_proto_field_name=True)
        if res['code'] // 100 != 2:
            return res
        doc = {}
        for key, value in res['doc'].items():
            doc[key] = list(map(lambda x: convert_map[x['type']](x['value']), value))
        res['doc'] = doc
        return res

    @grpc_client_error_handler(pb2.DocResponse())
    async def get_one(self, query_req: pb2.DocResponse) -> dict:
        res = await self.stub.GetOne(query_req)
        res = MessageToDict(res, preserving_proto_field_name=True)
        if res['code'] // 100 != 2:
            return res
        res['doc'] = self.collection_model(**res['doc']).model_dump(by_alias=True)
        return res

    @grpc_client_error_handler(pb2.DocListResponse())
    async def get_many(self, query_req: pb2.QueryRequest) -> dict:
        res = await self.stub.GetMany(query_req)
        res = MessageToDict(res, preserving_proto_field_name=True)
        if res['code'] // 100 != 2:
            return res
        res['doc_list'] = [self.collection_model(**doc).model_dump(by_alias=True) for doc in res['doc_list']]
        return res

    @grpc_client_error_handler(pb2.CountResponse())
    async def update_many(self, update_many_req: pb2.UpdateManyRequest) -> dict:
        res = await self.stub.UpdateMany(update_many_req)
        res = MessageToDict(res, preserving_proto_field_name=True)
        return res


async def main():
    from mongodb_module.beanie_data_model.user_model import UserBase
    async with CollectionClient('127.0.0.1', 11122, UserBase) as client:
        # doc_req = pb2.DocRequest()
        # doc_req.doc = {'name': '1', 'age': 333}
        # res = await client.insert_one(doc_req)

        # doc_list_req = pb2.DocListRequest()
        # for i in range(5):
        #     doc = struct_pb2.Struct()
        #     doc.update({'name': str(i), 'age': i})
        #     doc_list_req.doc_list.append(doc)
        # res = await client.insert_many(doc_list_req)

        # tag_req = pb2.TagRequest()
        # tag_req.field_list.extend(['_id', 'age', 'name'])
        # tag_req.query = {'name': {'$gte': '1'}}
        # res = await client.get_tag(tag_req)

        # id_req = pb2.IdRequest()
        # id_req.doc_id = '6734aa6c310830ac00960585'
        # res = await client.get_one(id_req)

        # query_req = pb2.QueryRequest()
        # query_req.query = {'name': {'$gte': '1'}}
        # query_req.project_model = 'ProjectUser'
        # query_req.sort.extend(['+age'])
        # query_req.page_size = 7
        # query_req.page_num = 1
        # res = await client.get_many(query_req)

        update_many_req = pb2.UpdateManyRequest()
        # update_req = pb2.UpdateRequest()
        # update_req.query = {'name': '0'}
        # update_req.set = {'aa': 'sss22'}
        # update_many_req.update_request_list.append(update_req)
        update_req = pb2.UpdateRequest()
        update_req.query = {'name': '7'}
        update_req.set = {'aa.$[elem].a': 'aaaaaaaaa'}
        update_req.array_filter = {'elem.index': 1}
        # update_req.upsert = True
        update_many_req.update_request_list.append(update_req)
        res = await client.update_many(update_many_req)

        print(res)


if __name__ == '__main__':
    asyncio.run(main())
