# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: finam_grpc_client/models/grpc/portfolios.proto
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
    "finam_grpc_client/models/grpc/portfolios.proto",
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from finam_grpc_client.models.proto import (
    portfolios_pb2 as finam__grpc__client_dot_models_dot_proto_dot_portfolios__pb2,
)


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b"\n.finam_grpc_client/models/grpc/portfolios.proto\x12\x10grpc.tradeapi.v1\x1a/finam_grpc_client/models/proto/portfolios.proto2k\n\nPortfolios\x12]\n\x0cGetPortfolio\x12&.proto.tradeapi.v1.GetPortfolioRequest\x1a%.proto.tradeapi.v1.GetPortfolioResultB\x19\xaa\x02\x16\x46inam.TradeApi.Grpc.V1b\x06proto3"
)

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(
    DESCRIPTOR, "finam_grpc_client.models.grpc.portfolios_pb2", _globals
)
if not _descriptor._USE_C_DESCRIPTORS:
    _globals["DESCRIPTOR"]._loaded_options = None
    _globals["DESCRIPTOR"]._serialized_options = b"\252\002\026Finam.TradeApi.Grpc.V1"
    _globals["_PORTFOLIOS"]._serialized_start = 117
    _globals["_PORTFOLIOS"]._serialized_end = 224
# @@protoc_insertion_point(module_scope)
