from finam_grpc_client.models.proto import security_pb2 as _security_pb2
from google.protobuf import wrappers_pb2 as _wrappers_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import (
    ClassVar as _ClassVar,
    Iterable as _Iterable,
    Mapping as _Mapping,
    Optional as _Optional,
    Union as _Union,
)

DESCRIPTOR: _descriptor.FileDescriptor

class GetSecuritiesRequest(_message.Message):
    __slots__ = ("board", "seccode")
    BOARD_FIELD_NUMBER: _ClassVar[int]
    SECCODE_FIELD_NUMBER: _ClassVar[int]
    board: _wrappers_pb2.StringValue
    seccode: _wrappers_pb2.StringValue
    def __init__(
        self,
        board: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ...,
        seccode: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ...,
    ) -> None: ...

class GetSecuritiesResult(_message.Message):
    __slots__ = ("securities",)
    SECURITIES_FIELD_NUMBER: _ClassVar[int]
    securities: _containers.RepeatedCompositeFieldContainer[_security_pb2.Security]
    def __init__(
        self,
        securities: _Optional[
            _Iterable[_Union[_security_pb2.Security, _Mapping]]
        ] = ...,
    ) -> None: ...
