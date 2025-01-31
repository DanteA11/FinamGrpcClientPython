from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
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

class Market(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    MARKET_UNSPECIFIED: _ClassVar[Market]
    MARKET_STOCK: _ClassVar[Market]
    MARKET_FORTS: _ClassVar[Market]
    MARKET_SPBEX: _ClassVar[Market]
    MARKET_MMA: _ClassVar[Market]
    MARKET_ETS: _ClassVar[Market]
    MARKET_BONDS: _ClassVar[Market]
    MARKET_OPTIONS: _ClassVar[Market]

class BuySell(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    BUY_SELL_UNSPECIFIED: _ClassVar[BuySell]
    BUY_SELL_SELL: _ClassVar[BuySell]
    BUY_SELL_BUY: _ClassVar[BuySell]

class OrderValidBeforeType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ORDER_VALID_BEFORE_TYPE_UNSPECIFIED: _ClassVar[OrderValidBeforeType]
    ORDER_VALID_BEFORE_TYPE_TILL_END_SESSION: _ClassVar[OrderValidBeforeType]
    ORDER_VALID_BEFORE_TYPE_TILL_CANCELLED: _ClassVar[OrderValidBeforeType]
    ORDER_VALID_BEFORE_TYPE_EXACT_TIME: _ClassVar[OrderValidBeforeType]

MARKET_UNSPECIFIED: Market
MARKET_STOCK: Market
MARKET_FORTS: Market
MARKET_SPBEX: Market
MARKET_MMA: Market
MARKET_ETS: Market
MARKET_BONDS: Market
MARKET_OPTIONS: Market
BUY_SELL_UNSPECIFIED: BuySell
BUY_SELL_SELL: BuySell
BUY_SELL_BUY: BuySell
ORDER_VALID_BEFORE_TYPE_UNSPECIFIED: OrderValidBeforeType
ORDER_VALID_BEFORE_TYPE_TILL_END_SESSION: OrderValidBeforeType
ORDER_VALID_BEFORE_TYPE_TILL_CANCELLED: OrderValidBeforeType
ORDER_VALID_BEFORE_TYPE_EXACT_TIME: OrderValidBeforeType

class ResponseEvent(_message.Message):
    __slots__ = ("request_id", "success", "errors")
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ERRORS_FIELD_NUMBER: _ClassVar[int]
    request_id: str
    success: bool
    errors: _containers.RepeatedCompositeFieldContainer[Error]
    def __init__(
        self,
        request_id: _Optional[str] = ...,
        success: bool = ...,
        errors: _Optional[_Iterable[_Union[Error, _Mapping]]] = ...,
    ) -> None: ...

class Error(_message.Message):
    __slots__ = ("code", "message")
    CODE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    code: str
    message: str
    def __init__(
        self, code: _Optional[str] = ..., message: _Optional[str] = ...
    ) -> None: ...

class OrderValidBefore(_message.Message):
    __slots__ = ("type", "time")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    TIME_FIELD_NUMBER: _ClassVar[int]
    type: OrderValidBeforeType
    time: _timestamp_pb2.Timestamp
    def __init__(
        self,
        type: _Optional[_Union[OrderValidBeforeType, str]] = ...,
        time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
    ) -> None: ...

class Decimal(_message.Message):
    __slots__ = ("num", "scale")
    NUM_FIELD_NUMBER: _ClassVar[int]
    SCALE_FIELD_NUMBER: _ClassVar[int]
    num: int
    scale: int
    def __init__(
        self, num: _Optional[int] = ..., scale: _Optional[int] = ...
    ) -> None: ...
