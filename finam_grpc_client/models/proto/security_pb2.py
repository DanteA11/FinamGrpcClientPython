# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: finam_grpc_client/models/proto/security.proto
# Protobuf Python Version: 5.28.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder

_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    28,
    1,
    "",
    "finam_grpc_client/models/proto/security.proto",
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from finam_grpc_client.models.proto import (
    common_pb2 as finam__grpc__client_dot_models_dot_proto_dot_common__pb2,
)


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n-finam_grpc_client/models/proto/security.proto\x12\x11proto.tradeapi.v1\x1a+finam_grpc_client/models/proto/common.proto"\xf3\x02\n\x08Security\x12\x0c\n\x04\x63ode\x18\x01 \x01(\t\x12\r\n\x05\x62oard\x18\x02 \x01(\t\x12)\n\x06market\x18\x03 \x01(\x0e\x32\x19.proto.tradeapi.v1.Market\x12\x10\n\x08\x64\x65\x63imals\x18\x04 \x01(\x11\x12\x10\n\x08lot_size\x18\x05 \x01(\x11\x12\x10\n\x08min_step\x18\x06 \x01(\x11\x12\x10\n\x08\x63urrency\x18\x07 \x01(\t\x12\x12\n\nshort_name\x18\t \x01(\t\x12\x12\n\nproperties\x18\n \x01(\x05\x12\x16\n\x0etime_zone_name\x18\x0b \x01(\t\x12\x0f\n\x07\x62p_cost\x18\x0c \x01(\x01\x12\x18\n\x10\x61\x63\x63rued_interest\x18\r \x01(\x01\x12\x30\n\nprice_sign\x18\x0e \x01(\x0e\x32\x1c.proto.tradeapi.v1.PriceSign\x12\x0e\n\x06ticker\x18\x0f \x01(\t\x12\x13\n\x0blot_divider\x18\x10 \x01(\x11J\x04\x08\x08\x10\tR\x0finstrument_code*q\n\tPriceSign\x12\x1a\n\x16PRICE_SIGN_UNSPECIFIED\x10\x00\x12\x17\n\x13PRICE_SIGN_POSITIVE\x10\x01\x12\x1b\n\x17PRICE_SIGN_NON_NEGATIVE\x10\x02\x12\x12\n\x0ePRICE_SIGN_ANY\x10\x03\x42\x1a\xaa\x02\x17\x46inam.TradeApi.Proto.V1b\x06proto3'
)

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(
    DESCRIPTOR, "finam_grpc_client.models.proto.security_pb2", _globals
)
if not _descriptor._USE_C_DESCRIPTORS:
    _globals["DESCRIPTOR"]._loaded_options = None
    _globals["DESCRIPTOR"]._serialized_options = b"\252\002\027Finam.TradeApi.Proto.V1"
    _globals["_PRICESIGN"]._serialized_start = 487
    _globals["_PRICESIGN"]._serialized_end = 600
    _globals["_SECURITY"]._serialized_start = 114
    _globals["_SECURITY"]._serialized_end = 485
# @@protoc_insertion_point(module_scope)
