from finam_grpc_client.models.proto import common_pb2 as _common_pb2
from finam_grpc_client.models.proto import orders_pb2 as _orders_pb2
from finam_grpc_client.models.proto import portfolios_pb2 as _portfolios_pb2
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

class TimeFrame(_message.Message):
    __slots__ = ("time_unit",)

    class Unit(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        UNIT_UNSPECIFIED: _ClassVar[TimeFrame.Unit]
        UNIT_MINUTE: _ClassVar[TimeFrame.Unit]
        UNIT_HOUR: _ClassVar[TimeFrame.Unit]
        UNIT_DAY: _ClassVar[TimeFrame.Unit]
        UNIT_WEEK: _ClassVar[TimeFrame.Unit]
        UNIT_MONTH: _ClassVar[TimeFrame.Unit]
        UNIT_QUARTER: _ClassVar[TimeFrame.Unit]
        UNIT_YEAR: _ClassVar[TimeFrame.Unit]

    UNIT_UNSPECIFIED: TimeFrame.Unit
    UNIT_MINUTE: TimeFrame.Unit
    UNIT_HOUR: TimeFrame.Unit
    UNIT_DAY: TimeFrame.Unit
    UNIT_WEEK: TimeFrame.Unit
    UNIT_MONTH: TimeFrame.Unit
    UNIT_QUARTER: TimeFrame.Unit
    UNIT_YEAR: TimeFrame.Unit
    TIME_UNIT_FIELD_NUMBER: _ClassVar[int]
    time_unit: TimeFrame.Unit
    def __init__(
        self, time_unit: _Optional[_Union[TimeFrame.Unit, str]] = ...
    ) -> None: ...

class SubscriptionRequest(_message.Message):
    __slots__ = (
        "order_book_subscribe_request",
        "order_book_unsubscribe_request",
        "order_trade_subscribe_request",
        "order_trade_unsubscribe_request",
        "keep_alive_request",
    )
    ORDER_BOOK_SUBSCRIBE_REQUEST_FIELD_NUMBER: _ClassVar[int]
    ORDER_BOOK_UNSUBSCRIBE_REQUEST_FIELD_NUMBER: _ClassVar[int]
    ORDER_TRADE_SUBSCRIBE_REQUEST_FIELD_NUMBER: _ClassVar[int]
    ORDER_TRADE_UNSUBSCRIBE_REQUEST_FIELD_NUMBER: _ClassVar[int]
    KEEP_ALIVE_REQUEST_FIELD_NUMBER: _ClassVar[int]
    order_book_subscribe_request: OrderBookSubscribeRequest
    order_book_unsubscribe_request: OrderBookUnsubscribeRequest
    order_trade_subscribe_request: OrderTradeSubscribeRequest
    order_trade_unsubscribe_request: OrderTradeUnsubscribeRequest
    keep_alive_request: KeepAliveRequest
    def __init__(
        self,
        order_book_subscribe_request: _Optional[
            _Union[OrderBookSubscribeRequest, _Mapping]
        ] = ...,
        order_book_unsubscribe_request: _Optional[
            _Union[OrderBookUnsubscribeRequest, _Mapping]
        ] = ...,
        order_trade_subscribe_request: _Optional[
            _Union[OrderTradeSubscribeRequest, _Mapping]
        ] = ...,
        order_trade_unsubscribe_request: _Optional[
            _Union[OrderTradeUnsubscribeRequest, _Mapping]
        ] = ...,
        keep_alive_request: _Optional[_Union[KeepAliveRequest, _Mapping]] = ...,
    ) -> None: ...

class Event(_message.Message):
    __slots__ = ("order", "trade", "order_book", "portfolio", "response")
    ORDER_FIELD_NUMBER: _ClassVar[int]
    TRADE_FIELD_NUMBER: _ClassVar[int]
    ORDER_BOOK_FIELD_NUMBER: _ClassVar[int]
    PORTFOLIO_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    order: OrderEvent
    trade: TradeEvent
    order_book: OrderBookEvent
    portfolio: PortfolioEvent
    response: _common_pb2.ResponseEvent
    def __init__(
        self,
        order: _Optional[_Union[OrderEvent, _Mapping]] = ...,
        trade: _Optional[_Union[TradeEvent, _Mapping]] = ...,
        order_book: _Optional[_Union[OrderBookEvent, _Mapping]] = ...,
        portfolio: _Optional[_Union[PortfolioEvent, _Mapping]] = ...,
        response: _Optional[_Union[_common_pb2.ResponseEvent, _Mapping]] = ...,
    ) -> None: ...

class OrderBookSubscribeRequest(_message.Message):
    __slots__ = ("request_id", "security_code", "security_board")
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    SECURITY_CODE_FIELD_NUMBER: _ClassVar[int]
    SECURITY_BOARD_FIELD_NUMBER: _ClassVar[int]
    request_id: str
    security_code: str
    security_board: str
    def __init__(
        self,
        request_id: _Optional[str] = ...,
        security_code: _Optional[str] = ...,
        security_board: _Optional[str] = ...,
    ) -> None: ...

class OrderBookUnsubscribeRequest(_message.Message):
    __slots__ = ("request_id", "security_code", "security_board")
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    SECURITY_CODE_FIELD_NUMBER: _ClassVar[int]
    SECURITY_BOARD_FIELD_NUMBER: _ClassVar[int]
    request_id: str
    security_code: str
    security_board: str
    def __init__(
        self,
        request_id: _Optional[str] = ...,
        security_code: _Optional[str] = ...,
        security_board: _Optional[str] = ...,
    ) -> None: ...

class OrderTradeSubscribeRequest(_message.Message):
    __slots__ = ("request_id", "include_trades", "include_orders", "client_ids")
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_TRADES_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_ORDERS_FIELD_NUMBER: _ClassVar[int]
    CLIENT_IDS_FIELD_NUMBER: _ClassVar[int]
    request_id: str
    include_trades: bool
    include_orders: bool
    client_ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(
        self,
        request_id: _Optional[str] = ...,
        include_trades: bool = ...,
        include_orders: bool = ...,
        client_ids: _Optional[_Iterable[str]] = ...,
    ) -> None: ...

class OrderTradeUnsubscribeRequest(_message.Message):
    __slots__ = ("request_id",)
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    request_id: str
    def __init__(self, request_id: _Optional[str] = ...) -> None: ...

class PortfolioSubscription(_message.Message):
    __slots__ = ("client_id", "content")
    CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    client_id: str
    content: _portfolios_pb2.PortfolioContent
    def __init__(
        self,
        client_id: _Optional[str] = ...,
        content: _Optional[_Union[_portfolios_pb2.PortfolioContent, _Mapping]] = ...,
    ) -> None: ...

class OrderEvent(_message.Message):
    __slots__ = (
        "order_no",
        "transaction_id",
        "security_code",
        "client_id",
        "status",
        "buy_sell",
        "created_at",
        "price",
        "quantity",
        "balance",
        "message",
        "currency",
        "condition",
        "valid_before",
        "accepted_at",
    )
    ORDER_NO_FIELD_NUMBER: _ClassVar[int]
    TRANSACTION_ID_FIELD_NUMBER: _ClassVar[int]
    SECURITY_CODE_FIELD_NUMBER: _ClassVar[int]
    CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    BUY_SELL_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    PRICE_FIELD_NUMBER: _ClassVar[int]
    QUANTITY_FIELD_NUMBER: _ClassVar[int]
    BALANCE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    CURRENCY_FIELD_NUMBER: _ClassVar[int]
    CONDITION_FIELD_NUMBER: _ClassVar[int]
    VALID_BEFORE_FIELD_NUMBER: _ClassVar[int]
    ACCEPTED_AT_FIELD_NUMBER: _ClassVar[int]
    order_no: int
    transaction_id: int
    security_code: str
    client_id: str
    status: _orders_pb2.OrderStatus
    buy_sell: _common_pb2.BuySell
    created_at: _timestamp_pb2.Timestamp
    price: float
    quantity: int
    balance: int
    message: str
    currency: str
    condition: _orders_pb2.OrderCondition
    valid_before: _common_pb2.OrderValidBefore
    accepted_at: _timestamp_pb2.Timestamp
    def __init__(
        self,
        order_no: _Optional[int] = ...,
        transaction_id: _Optional[int] = ...,
        security_code: _Optional[str] = ...,
        client_id: _Optional[str] = ...,
        status: _Optional[_Union[_orders_pb2.OrderStatus, str]] = ...,
        buy_sell: _Optional[_Union[_common_pb2.BuySell, str]] = ...,
        created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        price: _Optional[float] = ...,
        quantity: _Optional[int] = ...,
        balance: _Optional[int] = ...,
        message: _Optional[str] = ...,
        currency: _Optional[str] = ...,
        condition: _Optional[_Union[_orders_pb2.OrderCondition, _Mapping]] = ...,
        valid_before: _Optional[_Union[_common_pb2.OrderValidBefore, _Mapping]] = ...,
        accepted_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
    ) -> None: ...

class TradeEvent(_message.Message):
    __slots__ = (
        "security_code",
        "trade_no",
        "order_no",
        "client_id",
        "created_at",
        "quantity",
        "price",
        "value",
        "buy_sell",
        "commission",
        "currency",
        "accrued_interest",
    )
    SECURITY_CODE_FIELD_NUMBER: _ClassVar[int]
    TRADE_NO_FIELD_NUMBER: _ClassVar[int]
    ORDER_NO_FIELD_NUMBER: _ClassVar[int]
    CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    QUANTITY_FIELD_NUMBER: _ClassVar[int]
    PRICE_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    BUY_SELL_FIELD_NUMBER: _ClassVar[int]
    COMMISSION_FIELD_NUMBER: _ClassVar[int]
    CURRENCY_FIELD_NUMBER: _ClassVar[int]
    ACCRUED_INTEREST_FIELD_NUMBER: _ClassVar[int]
    security_code: str
    trade_no: int
    order_no: int
    client_id: str
    created_at: _timestamp_pb2.Timestamp
    quantity: int
    price: float
    value: float
    buy_sell: _common_pb2.BuySell
    commission: float
    currency: str
    accrued_interest: float
    def __init__(
        self,
        security_code: _Optional[str] = ...,
        trade_no: _Optional[int] = ...,
        order_no: _Optional[int] = ...,
        client_id: _Optional[str] = ...,
        created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        quantity: _Optional[int] = ...,
        price: _Optional[float] = ...,
        value: _Optional[float] = ...,
        buy_sell: _Optional[_Union[_common_pb2.BuySell, str]] = ...,
        commission: _Optional[float] = ...,
        currency: _Optional[str] = ...,
        accrued_interest: _Optional[float] = ...,
    ) -> None: ...

class OrderBookRow(_message.Message):
    __slots__ = ("price", "quantity")
    PRICE_FIELD_NUMBER: _ClassVar[int]
    QUANTITY_FIELD_NUMBER: _ClassVar[int]
    price: float
    quantity: int
    def __init__(
        self, price: _Optional[float] = ..., quantity: _Optional[int] = ...
    ) -> None: ...

class OrderBookEvent(_message.Message):
    __slots__ = ("security_code", "security_board", "asks", "bids")
    SECURITY_CODE_FIELD_NUMBER: _ClassVar[int]
    SECURITY_BOARD_FIELD_NUMBER: _ClassVar[int]
    ASKS_FIELD_NUMBER: _ClassVar[int]
    BIDS_FIELD_NUMBER: _ClassVar[int]
    security_code: str
    security_board: str
    asks: _containers.RepeatedCompositeFieldContainer[OrderBookRow]
    bids: _containers.RepeatedCompositeFieldContainer[OrderBookRow]
    def __init__(
        self,
        security_code: _Optional[str] = ...,
        security_board: _Optional[str] = ...,
        asks: _Optional[_Iterable[_Union[OrderBookRow, _Mapping]]] = ...,
        bids: _Optional[_Iterable[_Union[OrderBookRow, _Mapping]]] = ...,
    ) -> None: ...

class PortfolioEvent(_message.Message):
    __slots__ = (
        "client_id",
        "content",
        "equity",
        "balance",
        "positions",
        "currencies",
        "money",
    )
    CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    EQUITY_FIELD_NUMBER: _ClassVar[int]
    BALANCE_FIELD_NUMBER: _ClassVar[int]
    POSITIONS_FIELD_NUMBER: _ClassVar[int]
    CURRENCIES_FIELD_NUMBER: _ClassVar[int]
    MONEY_FIELD_NUMBER: _ClassVar[int]
    client_id: str
    content: _portfolios_pb2.PortfolioContent
    equity: float
    balance: float
    positions: _containers.RepeatedCompositeFieldContainer[_portfolios_pb2.PositionRow]
    currencies: _containers.RepeatedCompositeFieldContainer[_portfolios_pb2.CurrencyRow]
    money: _containers.RepeatedCompositeFieldContainer[_portfolios_pb2.MoneyRow]
    def __init__(
        self,
        client_id: _Optional[str] = ...,
        content: _Optional[_Union[_portfolios_pb2.PortfolioContent, _Mapping]] = ...,
        equity: _Optional[float] = ...,
        balance: _Optional[float] = ...,
        positions: _Optional[
            _Iterable[_Union[_portfolios_pb2.PositionRow, _Mapping]]
        ] = ...,
        currencies: _Optional[
            _Iterable[_Union[_portfolios_pb2.CurrencyRow, _Mapping]]
        ] = ...,
        money: _Optional[_Iterable[_Union[_portfolios_pb2.MoneyRow, _Mapping]]] = ...,
    ) -> None: ...

class KeepAliveRequest(_message.Message):
    __slots__ = ("request_id",)
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    request_id: str
    def __init__(self, request_id: _Optional[str] = ...) -> None: ...
