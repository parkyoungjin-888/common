import asyncio
import grpc
from functools import wraps
from google.protobuf.json_format import MessageToDict
from google.protobuf import struct_pb2
from mongodb_module.proto import collection_pb2 as pb2
from mongodb_module.proto import collection_pb2_grpc


def grpc_client_error_handler(response):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                func_response = await func(*args, **kwargs)
            except grpc.aio.AioRpcError as e:
                print(f'{func.__name__} gRPC Error: {e.code()} - {e.details()}')
                response.code = 400
                response.message = f'{func.__name__} gRPC Error: {e.code()} - {e.details()}'
                func_response = response
            except Exception as e:
                print(f'{func.__name__} Error: {str(e)}')
                response.code = 500
                response.message = f'{func.__name__} Error: {str(e)}'
                func_response = response
            return MessageToDict(func_response, preserving_proto_field_name=True)
        return wrapper
    return decorator


class CollectionClient:
    def __init__(self, host: str, port: int):
        self.channel = grpc.aio.insecure_channel(f'{host}:{port}')
        self.stub = collection_pb2_grpc.CollectionServerStub(self.channel)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.channel.close()

    @grpc_client_error_handler(pb2.IdResponse())
    async def insert_one(self, doc_req: pb2.DocRequest) -> dict:
        res = await self.stub.InsertOne(doc_req)
        return res

    @grpc_client_error_handler(pb2.IdListResponse())
    async def insert_many(self, doc_list_req: pb2.DocListRequest) -> dict:
        res = await self.stub.InsertMany(doc_list_req)
        return res

    @grpc_client_error_handler(pb2.CountResponse())
    async def get_count(self, query_req: pb2.QueryRequest) -> dict:
        res = await self.stub.GetCount(query_req)
        return res


async def main():
    async with CollectionClient('127.0.0.1', 11122) as client:
        # doc_req = pb2.DocRequest()
        # doc_req.doc = {'name': '1', 'age': 333}
        # res = await client.insert_one(doc_req)

        # doc_list_req = pb2.DocListRequest()
        # for i in range(5):
        #     doc = struct_pb2.Struct()
        #     doc.update({'name': str(i), 'age': i})
        #     doc_list_req.doc_list.append(doc)
        # res = await client.insert_many(doc_list_req)

        query_req = pb2.QueryRequest()
        query_req.filter = {'name': {'$gte': '1'}}
        res = await client.get_count(query_req)

        print(res)


if __name__ == '__main__':
    asyncio.run(main())
