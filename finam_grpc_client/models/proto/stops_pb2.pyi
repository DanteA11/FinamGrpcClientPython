from google.protobuf import timestamp_pb2 as _timestamp_pb2
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

class StopStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    STOP_STATUS_UNSPECIFIED: _ClassVar[StopStatus]
    STOP_STATUS_NONE: _ClassVar[StopStatus]
    STOP_STATUS_ACTIVE: _ClassVar[StopStatus]
    STOP_STATUS_CANCELLED: _ClassVar[StopStatus]
    STOP_STATUS_EXECUTED: _ClassVar[StopStatus]

class StopQuantityUnits(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    STOP_QUANTITY_UNITS_UNSPECIFIED: _ClassVar[StopQuantityUnits]
    STOP_QUANTITY_UNITS_PERCENT: _ClassVar[StopQuantityUnits]
    STOP_QUANTITY_UNITS_LOTS: _ClassVar[StopQuantityUnits]

class StopPriceUnits(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    STOP_PRICE_UNITS_UNSPECIFIED: _ClassVar[StopPriceUnits]
    STOP_PRICE_UNITS_PERCENT: _ClassVar[StopPriceUnits]
    STOP_PRICE_UNITS_PIPS: _ClassVar[StopPriceUnits]

STOP_STATUS_UNSPECIFIED: StopStatus
STOP_STATUS_NONE: StopStatus
STOP_STATUS_ACTIVE: StopStatus
STOP_STATUS_CANCELLED: StopStatus
STOP_STATUS_EXECUTED: StopStatus
STOP_QUANTITY_UNITS_UNSPECIFIED: StopQuantityUnits
STOP_QUANTITY_UNITS_PERCENT: StopQuantityUnits
STOP_QUANTITY_UNITS_LOTS: StopQuantityUnits
STOP_PRICE_UNITS_UNSPECIFIED: StopPriceUnits
STOP_PRICE_UNITS_PERCENT: StopPriceUnits
STOP_PRICE_UNITS_PIPS: StopPriceUnits

class Stop(_message.Message):
    __slots__ = (
        "stop_id",
        "security_code",
        "security_board",
        "market",
        "client_id",
        "buy_sell",
        "expiration_date",
        "link_order",
        "valid_before",
        "status",
        "message",
        "order_no",
        "trade_no",
        "accepted_at",
        "canceled_at",
        "currency",
        "take_profit_extremum",
        "take_profit_level",
        "stop_loss",
        "take_profit",
    )
    STOP_ID_FIELD_NUMBER: _ClassVar[int]
    SECURITY_CODE_FIELD_NUMBER: _ClassVar[int]
    SECURITY_BOARD_FIELD_NUMBER: _ClassVar[int]
    MARKET_FIELD_NUMBER: _ClassVar[int]
    CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    BUY_SELL_FIELD_NUMBER: _ClassVar[int]
    EXPIRATION_DATE_FIELD_NUMBER: _ClassVar[int]
    LINK_ORDER_FIELD_NUMBER: _ClassVar[int]
    VALID_BEFORE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    ORDER_NO_FIELD_NUMBER: _ClassVar[int]
    TRADE_NO_FIELD_NUMBER: _ClassVar[int]
    ACCEPTED_AT_FIELD_NUMBER: _ClassVar[int]
    CANCELED_AT_FIELD_NUMBER: _ClassVar[int]
    CURRENCY_FIELD_NUMBER: _ClassVar[int]
    TAKE_PROFIT_EXTREMUM_FIELD_NUMBER: _ClassVar[int]
    TAKE_PROFIT_LEVEL_FIELD_NUMBER: _ClassVar[int]
    STOP_LOSS_FIELD_NUMBER: _ClassVar[int]
    TAKE_PROFIT_FIELD_NUMBER: _ClassVar[int]
    stop_id: int
    security_code: str
    security_board: str
    market: _common_pb2.Market
    client_id: str
    buy_sell: _common_pb2.BuySell
    expiration_date: _timestamp_pb2.Timestamp
    link_order: int
    valid_before: _common_pb2.OrderValidBefore
    status: StopStatus
    message: str
    order_no: int
    trade_no: int
    accepted_at: _timestamp_pb2.Timestamp
    canceled_at: _timestamp_pb2.Timestamp
    currency: str
    take_profit_extremum: float
    take_profit_level: float
    stop_loss: StopLoss
    take_profit: TakeProfit
    def __init__(
        self,
        stop_id: _Optional[int] = ...,
        security_code: _Optional[str] = ...,
        security_board: _Optional[str] = ...,
        market: _Optional[_Union[_common_pb2.Market, str]] = ...,
        client_id: _Optional[str] = ...,
        buy_sell: _Optional[_Union[_common_pb2.BuySell, str]] = ...,
        expiration_date: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        link_order: _Optional[int] = ...,
        valid_before: _Optional[_Union[_common_pb2.OrderValidBefore, _Mapping]] = ...,
        status: _Optional[_Union[StopStatus, str]] = ...,
        message: _Optional[str] = ...,
        order_no: _Optional[int] = ...,
        trade_no: _Optional[int] = ...,
        accepted_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        canceled_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        currency: _Optional[str] = ...,
        take_profit_extremum: _Optional[float] = ...,
        take_profit_level: _Optional[float] = ...,
        stop_loss: _Optional[_Union[StopLoss, _Mapping]] = ...,
        take_profit: _Optional[_Union[TakeProfit, _Mapping]] = ...,
    ) -> None: ...

class StopLoss(_message.Message):
    __slots__ = (
        "activation_price",
        "price",
        "market_price",
        "quantity",
        "time",
        "use_credit",
    )
    ACTIVATION_PRICE_FIELD_NUMBER: _ClassVar[int]
    PRICE_FIELD_NUMBER: _ClassVar[int]
    MARKET_PRICE_FIELD_NUMBER: _ClassVar[int]
    QUANTITY_FIELD_NUMBER: _ClassVar[int]
    TIME_FIELD_NUMBER: _ClassVar[int]
    USE_CREDIT_FIELD_NUMBER: _ClassVar[int]
    activation_price: float
    price: float
    market_price: bool
    quantity: StopQuantity
    time: int
    use_credit: bool
    def __init__(
        self,
        activation_price: _Optional[float] = ...,
        price: _Optional[float] = ...,
        market_price: bool = ...,
        quantity: _Optional[_Union[StopQuantity, _Mapping]] = ...,
        time: _Optional[int] = ...,
        use_credit: bool = ...,
    ) -> None: ...

class TakeProfit(_message.Message):
    __slots__ = (
        "activation_price",
        "correction_price",
        "spread_price",
        "market_price",
        "quantity",
        "time",
        "use_credit",
    )
    ACTIVATION_PRICE_FIELD_NUMBER: _ClassVar[int]
    CORRECTION_PRICE_FIELD_NUMBER: _ClassVar[int]
    SPREAD_PRICE_FIELD_NUMBER: _ClassVar[int]
    MARKET_PRICE_FIELD_NUMBER: _ClassVar[int]
    QUANTITY_FIELD_NUMBER: _ClassVar[int]
    TIME_FIELD_NUMBER: _ClassVar[int]
    USE_CREDIT_FIELD_NUMBER: _ClassVar[int]
    activation_price: float
    correction_price: StopPrice
    spread_price: StopPrice
    market_price: bool
    quantity: StopQuantity
    time: int
    use_credit: bool
    def __init__(
        self,
        activation_price: _Optional[float] = ...,
        correction_price: _Optional[_Union[StopPrice, _Mapping]] = ...,
        spread_price: _Optional[_Union[StopPrice, _Mapping]] = ...,
        market_price: bool = ...,
        quantity: _Optional[_Union[StopQuantity, _Mapping]] = ...,
        time: _Optional[int] = ...,
        use_credit: bool = ...,
    ) -> None: ...

class StopQuantity(_message.Message):
    __slots__ = ("value", "units")
    VALUE_FIELD_NUMBER: _ClassVar[int]
    UNITS_FIELD_NUMBER: _ClassVar[int]
    value: float
    units: StopQuantityUnits
    def __init__(
        self,
        value: _Optional[float] = ...,
        units: _Optional[_Union[StopQuantityUnits, str]] = ...,
    ) -> None: ...

class StopPrice(_message.Message):
    __slots__ = ("value", "units")
    VALUE_FIELD_NUMBER: _ClassVar[int]
    UNITS_FIELD_NUMBER: _ClassVar[int]
    value: float
    units: StopPriceUnits
    def __init__(
        self,
        value: _Optional[float] = ...,
        units: _Optional[_Union[StopPriceUnits, str]] = ...,
    ) -> None: ...

class CancelStopRequest(_message.Message):
    __slots__ = ("client_id", "stop_id")
    CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    STOP_ID_FIELD_NUMBER: _ClassVar[int]
    client_id: str
    stop_id: int
    def __init__(
        self, client_id: _Optional[str] = ..., stop_id: _Optional[int] = ...
    ) -> None: ...

class CancelStopResult(_message.Message):
    __slots__ = ("client_id", "stop_id")
    CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    STOP_ID_FIELD_NUMBER: _ClassVar[int]
    client_id: str
    stop_id: int
    def __init__(
        self, client_id: _Optional[str] = ..., stop_id: _Optional[int] = ...
    ) -> None: ...

class GetStopsRequest(_message.Message):
    __slots__ = ("client_id", "include_executed", "include_canceled", "include_active")
    CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_EXECUTED_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_CANCELED_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_ACTIVE_FIELD_NUMBER: _ClassVar[int]
    client_id: str
    include_executed: bool
    include_canceled: bool
    include_active: bool
    def __init__(
        self,
        client_id: _Optional[str] = ...,
        include_executed: bool = ...,
        include_canceled: bool = ...,
        include_active: bool = ...,
    ) -> None: ...

class GetStopsResult(_message.Message):
    __slots__ = ("client_id", "stops")
    CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    STOPS_FIELD_NUMBER: _ClassVar[int]
    client_id: str
    stops: _containers.RepeatedCompositeFieldContainer[Stop]
    def __init__(
        self,
        client_id: _Optional[str] = ...,
        stops: _Optional[_Iterable[_Union[Stop, _Mapping]]] = ...,
    ) -> None: ...

class NewStopRequest(_message.Message):
    __slots__ = (
        "client_id",
        "security_board",
        "security_code",
        "buy_sell",
        "stop_loss",
        "take_profit",
        "expiration_date",
        "link_order",
        "valid_before",
    )
    CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    SECURITY_BOARD_FIELD_NUMBER: _ClassVar[int]
    SECURITY_CODE_FIELD_NUMBER: _ClassVar[int]
    BUY_SELL_FIELD_NUMBER: _ClassVar[int]
    STOP_LOSS_FIELD_NUMBER: _ClassVar[int]
    TAKE_PROFIT_FIELD_NUMBER: _ClassVar[int]
    EXPIRATION_DATE_FIELD_NUMBER: _ClassVar[int]
    LINK_ORDER_FIELD_NUMBER: _ClassVar[int]
    VALID_BEFORE_FIELD_NUMBER: _ClassVar[int]
    client_id: str
    security_board: str
    security_code: str
    buy_sell: _common_pb2.BuySell
    stop_loss: StopLoss
    take_profit: TakeProfit
    expiration_date: _timestamp_pb2.Timestamp
    link_order: int
    valid_before: _common_pb2.OrderValidBefore
    def __init__(
        self,
        client_id: _Optional[str] = ...,
        security_board: _Optional[str] = ...,
        security_code: _Optional[str] = ...,
        buy_sell: _Optional[_Union[_common_pb2.BuySell, str]] = ...,
        stop_loss: _Optional[_Union[StopLoss, _Mapping]] = ...,
        take_profit: _Optional[_Union[TakeProfit, _Mapping]] = ...,
        expiration_date: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        link_order: _Optional[int] = ...,
        valid_before: _Optional[_Union[_common_pb2.OrderValidBefore, _Mapping]] = ...,
    ) -> None: ...

class NewStopResult(_message.Message):
    __slots__ = ("client_id", "stop_id", "security_code", "security_board")
    CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    STOP_ID_FIELD_NUMBER: _ClassVar[int]
    SECURITY_CODE_FIELD_NUMBER: _ClassVar[int]
    SECURITY_BOARD_FIELD_NUMBER: _ClassVar[int]
    client_id: str
    stop_id: int
    security_code: str
    security_board: str
    def __init__(
        self,
        client_id: _Optional[str] = ...,
        stop_id: _Optional[int] = ...,
        security_code: _Optional[str] = ...,
        security_board: _Optional[str] = ...,
    ) -> None: ...
