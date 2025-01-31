from google.protobuf import timestamp_pb2 as _timestamp_pb2
from finam_grpc_client.models.google import date_pb2 as _date_pb2
from finam_grpc_client.models.proto import common_pb2 as _common_pb2
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

class IntradayCandleTimeFrame(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    INTRADAYCANDLE_TIMEFRAME_UNSPECIFIED: _ClassVar[IntradayCandleTimeFrame]
    INTRADAYCANDLE_TIMEFRAME_M1: _ClassVar[IntradayCandleTimeFrame]
    INTRADAYCANDLE_TIMEFRAME_M5: _ClassVar[IntradayCandleTimeFrame]
    INTRADAYCANDLE_TIMEFRAME_M15: _ClassVar[IntradayCandleTimeFrame]
    INTRADAYCANDLE_TIMEFRAME_H1: _ClassVar[IntradayCandleTimeFrame]

class DayCandleTimeFrame(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DAYCANDLE_TIMEFRAME_UNSPECIFIED: _ClassVar[DayCandleTimeFrame]
    DAYCANDLE_TIMEFRAME_D1: _ClassVar[DayCandleTimeFrame]
    DAYCANDLE_TIMEFRAME_W1: _ClassVar[DayCandleTimeFrame]

INTRADAYCANDLE_TIMEFRAME_UNSPECIFIED: IntradayCandleTimeFrame
INTRADAYCANDLE_TIMEFRAME_M1: IntradayCandleTimeFrame
INTRADAYCANDLE_TIMEFRAME_M5: IntradayCandleTimeFrame
INTRADAYCANDLE_TIMEFRAME_M15: IntradayCandleTimeFrame
INTRADAYCANDLE_TIMEFRAME_H1: IntradayCandleTimeFrame
DAYCANDLE_TIMEFRAME_UNSPECIFIED: DayCandleTimeFrame
DAYCANDLE_TIMEFRAME_D1: DayCandleTimeFrame
DAYCANDLE_TIMEFRAME_W1: DayCandleTimeFrame

class DayCandle(_message.Message):
    __slots__ = ("date", "open", "close", "high", "low", "volume")
    DATE_FIELD_NUMBER: _ClassVar[int]
    OPEN_FIELD_NUMBER: _ClassVar[int]
    CLOSE_FIELD_NUMBER: _ClassVar[int]
    HIGH_FIELD_NUMBER: _ClassVar[int]
    LOW_FIELD_NUMBER: _ClassVar[int]
    VOLUME_FIELD_NUMBER: _ClassVar[int]
    date: _date_pb2.Date
    open: _common_pb2.Decimal
    close: _common_pb2.Decimal
    high: _common_pb2.Decimal
    low: _common_pb2.Decimal
    volume: int
    def __init__(
        self,
        date: _Optional[_Union[_date_pb2.Date, _Mapping]] = ...,
        open: _Optional[_Union[_common_pb2.Decimal, _Mapping]] = ...,
        close: _Optional[_Union[_common_pb2.Decimal, _Mapping]] = ...,
        high: _Optional[_Union[_common_pb2.Decimal, _Mapping]] = ...,
        low: _Optional[_Union[_common_pb2.Decimal, _Mapping]] = ...,
        volume: _Optional[int] = ...,
    ) -> None: ...

class IntradayCandle(_message.Message):
    __slots__ = ("timestamp", "open", "close", "high", "low", "volume")
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    OPEN_FIELD_NUMBER: _ClassVar[int]
    CLOSE_FIELD_NUMBER: _ClassVar[int]
    HIGH_FIELD_NUMBER: _ClassVar[int]
    LOW_FIELD_NUMBER: _ClassVar[int]
    VOLUME_FIELD_NUMBER: _ClassVar[int]
    timestamp: _timestamp_pb2.Timestamp
    open: _common_pb2.Decimal
    close: _common_pb2.Decimal
    high: _common_pb2.Decimal
    low: _common_pb2.Decimal
    volume: int
    def __init__(
        self,
        timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        open: _Optional[_Union[_common_pb2.Decimal, _Mapping]] = ...,
        close: _Optional[_Union[_common_pb2.Decimal, _Mapping]] = ...,
        high: _Optional[_Union[_common_pb2.Decimal, _Mapping]] = ...,
        low: _Optional[_Union[_common_pb2.Decimal, _Mapping]] = ...,
        volume: _Optional[int] = ...,
    ) -> None: ...

class DayCandleInterval(_message.Message):
    __slots__ = ("to", "count")
    FROM_FIELD_NUMBER: _ClassVar[int]
    TO_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    to: _date_pb2.Date
    count: int
    def __init__(
        self,
        to: _Optional[_Union[_date_pb2.Date, _Mapping]] = ...,
        count: _Optional[int] = ...,
        **kwargs
    ) -> None: ...

class IntradayCandleInterval(_message.Message):
    __slots__ = ("to", "count")
    FROM_FIELD_NUMBER: _ClassVar[int]
    TO_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    to: _timestamp_pb2.Timestamp
    count: int
    def __init__(
        self,
        to: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        count: _Optional[int] = ...,
        **kwargs
    ) -> None: ...

class GetDayCandlesRequest(_message.Message):
    __slots__ = ("security_board", "security_code", "time_frame", "interval")
    SECURITY_BOARD_FIELD_NUMBER: _ClassVar[int]
    SECURITY_CODE_FIELD_NUMBER: _ClassVar[int]
    TIME_FRAME_FIELD_NUMBER: _ClassVar[int]
    INTERVAL_FIELD_NUMBER: _ClassVar[int]
    security_board: str
    security_code: str
    time_frame: DayCandleTimeFrame
    interval: DayCandleInterval
    def __init__(
        self,
        security_board: _Optional[str] = ...,
        security_code: _Optional[str] = ...,
        time_frame: _Optional[_Union[DayCandleTimeFrame, str]] = ...,
        interval: _Optional[_Union[DayCandleInterval, _Mapping]] = ...,
    ) -> None: ...

class GetDayCandlesResult(_message.Message):
    __slots__ = ("candles",)
    CANDLES_FIELD_NUMBER: _ClassVar[int]
    candles: _containers.RepeatedCompositeFieldContainer[DayCandle]
    def __init__(
        self, candles: _Optional[_Iterable[_Union[DayCandle, _Mapping]]] = ...
    ) -> None: ...

class GetIntradayCandlesRequest(_message.Message):
    __slots__ = ("security_board", "security_code", "time_frame", "interval")
    SECURITY_BOARD_FIELD_NUMBER: _ClassVar[int]
    SECURITY_CODE_FIELD_NUMBER: _ClassVar[int]
    TIME_FRAME_FIELD_NUMBER: _ClassVar[int]
    INTERVAL_FIELD_NUMBER: _ClassVar[int]
    security_board: str
    security_code: str
    time_frame: IntradayCandleTimeFrame
    interval: IntradayCandleInterval
    def __init__(
        self,
        security_board: _Optional[str] = ...,
        security_code: _Optional[str] = ...,
        time_frame: _Optional[_Union[IntradayCandleTimeFrame, str]] = ...,
        interval: _Optional[_Union[IntradayCandleInterval, _Mapping]] = ...,
    ) -> None: ...

class GetIntradayCandlesResult(_message.Message):
    __slots__ = ("candles",)
    CANDLES_FIELD_NUMBER: _ClassVar[int]
    candles: _containers.RepeatedCompositeFieldContainer[IntradayCandle]
    def __init__(
        self, candles: _Optional[_Iterable[_Union[IntradayCandle, _Mapping]]] = ...
    ) -> None: ...
