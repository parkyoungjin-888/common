# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: mongodb_module/proto/collection.proto
# Protobuf Python Version: 5.27.2
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    27,
    2,
    '',
    'mongodb_module/proto/collection.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import struct_pb2 as google_dot_protobuf_dot_struct__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n%mongodb_module/proto/collection.proto\x12\ncollection\x1a\x1cgoogle/protobuf/struct.proto\"\x1b\n\tIdRequest\x12\x0e\n\x06\x64oc_id\x18\x01 \x01(\t\"2\n\nDocRequest\x12$\n\x03\x64oc\x18\x01 \x01(\x0b\x32\x17.google.protobuf.Struct\";\n\x0e\x44ocListRequest\x12)\n\x08\x64oc_list\x18\x01 \x03(\x0b\x32\x17.google.protobuf.Struct\"\x94\x01\n\x0cQueryRequest\x12\'\n\x06\x66ilter\x18\x01 \x01(\x0b\x32\x17.google.protobuf.Struct\x12(\n\x07project\x18\x02 \x01(\x0b\x32\x17.google.protobuf.Struct\x12\x0c\n\x04sort\x18\x03 \x03(\t\x12\x11\n\tpage_size\x18\x04 \x01(\x05\x12\x10\n\x08page_num\x18\x05 \x01(\x05\"\xad\x01\n\rUpdateRequest\x12\'\n\x06\x66ilter\x18\x01 \x01(\x0b\x32\x17.google.protobuf.Struct\x12$\n\x03set\x18\x02 \x01(\x0b\x32\x17.google.protobuf.Struct\x12&\n\x05unset\x18\x03 \x01(\x0b\x32\x17.google.protobuf.Struct\x12%\n\x04push\x18\x04 \x01(\x0b\x32\x17.google.protobuf.Struct\"F\n\x11UpdateManyRequest\x12\x31\n\x0eupdate_request\x18\x01 \x03(\x0b\x32\x19.collection.UpdateRequest\"=\n\x10\x41ggregateRequest\x12)\n\x08pipeline\x18\x01 \x03(\x0b\x32\x17.google.protobuf.Struct\";\n\nIdResponse\x12\x0e\n\x06\x64oc_id\x18\x01 \x01(\t\x12\x0c\n\x04\x63ode\x18\x02 \x01(\x05\x12\x0f\n\x07message\x18\x03 \x01(\t\"D\n\x0eIdListResponse\x12\x13\n\x0b\x64oc_id_list\x18\x01 \x03(\t\x12\x0c\n\x04\x63ode\x18\x02 \x01(\x05\x12\x0f\n\x07message\x18\x03 \x01(\t\"R\n\x0b\x44ocResponse\x12$\n\x03\x64oc\x18\x01 \x01(\x0b\x32\x17.google.protobuf.Struct\x12\x0c\n\x04\x63ode\x18\x02 \x01(\x05\x12\x0f\n\x07message\x18\x03 \x01(\t\"p\n\x0f\x44ocListResponse\x12)\n\x08\x64oc_list\x18\x01 \x03(\x0b\x32\x17.google.protobuf.Struct\x12\x13\n\x0btotal_count\x18\x02 \x01(\x05\x12\x0c\n\x04\x63ode\x18\x03 \x01(\x05\x12\x0f\n\x07message\x18\x04 \x01(\t\"=\n\rCountResponse\x12\r\n\x05\x63ount\x18\x01 \x01(\x05\x12\x0c\n\x04\x63ode\x18\x02 \x01(\x05\x12\x0f\n\x07message\x18\x03 \x01(\t2\xe7\x05\n\x10\x43ollectionServer\x12;\n\tInsertOne\x12\x16.collection.DocRequest\x1a\x16.collection.IdResponse\x12\x44\n\nInsertMany\x12\x1a.collection.DocListRequest\x1a\x1a.collection.IdListResponse\x12?\n\x08GetCount\x12\x18.collection.QueryRequest\x1a\x19.collection.CountResponse\x12;\n\x06GetTag\x12\x18.collection.QueryRequest\x1a\x17.collection.DocResponse\x12;\n\tGetDetail\x12\x15.collection.IdRequest\x1a\x17.collection.DocResponse\x12@\n\x07GetList\x12\x18.collection.QueryRequest\x1a\x1b.collection.DocListResponse\x12\x41\n\tUpdateOne\x12\x19.collection.UpdateRequest\x1a\x19.collection.CountResponse\x12\x46\n\nUpdateMany\x12\x1d.collection.UpdateManyRequest\x1a\x19.collection.CountResponse\x12=\n\tDeleteOne\x12\x15.collection.IdRequest\x1a\x19.collection.CountResponse\x12\x41\n\nDeleteMany\x12\x18.collection.QueryRequest\x1a\x19.collection.CountResponse\x12\x46\n\tAggregate\x12\x1c.collection.AggregateRequest\x1a\x1b.collection.DocListResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'mongodb_module.proto.collection_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_IDREQUEST']._serialized_start=83
  _globals['_IDREQUEST']._serialized_end=110
  _globals['_DOCREQUEST']._serialized_start=112
  _globals['_DOCREQUEST']._serialized_end=162
  _globals['_DOCLISTREQUEST']._serialized_start=164
  _globals['_DOCLISTREQUEST']._serialized_end=223
  _globals['_QUERYREQUEST']._serialized_start=226
  _globals['_QUERYREQUEST']._serialized_end=374
  _globals['_UPDATEREQUEST']._serialized_start=377
  _globals['_UPDATEREQUEST']._serialized_end=550
  _globals['_UPDATEMANYREQUEST']._serialized_start=552
  _globals['_UPDATEMANYREQUEST']._serialized_end=622
  _globals['_AGGREGATEREQUEST']._serialized_start=624
  _globals['_AGGREGATEREQUEST']._serialized_end=685
  _globals['_IDRESPONSE']._serialized_start=687
  _globals['_IDRESPONSE']._serialized_end=746
  _globals['_IDLISTRESPONSE']._serialized_start=748
  _globals['_IDLISTRESPONSE']._serialized_end=816
  _globals['_DOCRESPONSE']._serialized_start=818
  _globals['_DOCRESPONSE']._serialized_end=900
  _globals['_DOCLISTRESPONSE']._serialized_start=902
  _globals['_DOCLISTRESPONSE']._serialized_end=1014
  _globals['_COUNTRESPONSE']._serialized_start=1016
  _globals['_COUNTRESPONSE']._serialized_end=1077
  _globals['_COLLECTIONSERVER']._serialized_start=1080
  _globals['_COLLECTIONSERVER']._serialized_end=1823
# @@protoc_insertion_point(module_scope)
