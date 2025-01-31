from finam_grpc_client.models.proto import common_pb2 as _common_pb2
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

class PortfolioContent(_message.Message):
    __slots__ = (
        "include_currencies",
        "include_money",
        "include_positions",
        "include_max_buy_sell",
    )
    INCLUDE_CURRENCIES_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_MONEY_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_POSITIONS_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_MAX_BUY_SELL_FIELD_NUMBER: _ClassVar[int]
    include_currencies: bool
    include_money: bool
    include_positions: bool
    include_max_buy_sell: bool
    def __init__(
        self,
        include_currencies: bool = ...,
        include_money: bool = ...,
        include_positions: bool = ...,
        include_max_buy_sell: bool = ...,
    ) -> None: ...

class PositionRow(_message.Message):
    __slots__ = (
        "security_code",
        "market",
        "balance",
        "current_price",
        "equity",
        "average_price",
        "currency",
        "accumulated_profit",
        "today_profit",
        "unrealized_profit",
        "profit",
        "max_buy",
        "max_sell",
        "price_currency",
        "average_price_currency",
        "average_rate",
    )
    SECURITY_CODE_FIELD_NUMBER: _ClassVar[int]
    MARKET_FIELD_NUMBER: _ClassVar[int]
    BALANCE_FIELD_NUMBER: _ClassVar[int]
    CURRENT_PRICE_FIELD_NUMBER: _ClassVar[int]
    EQUITY_FIELD_NUMBER: _ClassVar[int]
    AVERAGE_PRICE_FIELD_NUMBER: _ClassVar[int]
    CURRENCY_FIELD_NUMBER: _ClassVar[int]
    ACCUMULATED_PROFIT_FIELD_NUMBER: _ClassVar[int]
    TODAY_PROFIT_FIELD_NUMBER: _ClassVar[int]
    UNREALIZED_PROFIT_FIELD_NUMBER: _ClassVar[int]
    PROFIT_FIELD_NUMBER: _ClassVar[int]
    MAX_BUY_FIELD_NUMBER: _ClassVar[int]
    MAX_SELL_FIELD_NUMBER: _ClassVar[int]
    PRICE_CURRENCY_FIELD_NUMBER: _ClassVar[int]
    AVERAGE_PRICE_CURRENCY_FIELD_NUMBER: _ClassVar[int]
    AVERAGE_RATE_FIELD_NUMBER: _ClassVar[int]
    security_code: str
    market: _common_pb2.Market
    balance: int
    current_price: float
    equity: float
    average_price: float
    currency: str
    accumulated_profit: float
    today_profit: float
    unrealized_profit: float
    profit: float
    max_buy: int
    max_sell: int
    price_currency: str
    average_price_currency: str
    average_rate: float
    def __init__(
        self,
        security_code: _Optional[str] = ...,
        market: _Optional[_Union[_common_pb2.Market, str]] = ...,
        balance: _Optional[int] = ...,
        current_price: _Optional[float] = ...,
        equity: _Optional[float] = ...,
        average_price: _Optional[float] = ...,
        currency: _Optional[str] = ...,
        accumulated_profit: _Optional[float] = ...,
        today_profit: _Optional[float] = ...,
        unrealized_profit: _Optional[float] = ...,
        profit: _Optional[float] = ...,
        max_buy: _Optional[int] = ...,
        max_sell: _Optional[int] = ...,
        price_currency: _Optional[str] = ...,
        average_price_currency: _Optional[str] = ...,
        average_rate: _Optional[float] = ...,
    ) -> None: ...

class CurrencyRow(_message.Message):
    __slots__ = ("name", "balance", "cross_rate", "equity", "unrealized_profit")
    NAME_FIELD_NUMBER: _ClassVar[int]
    BALANCE_FIELD_NUMBER: _ClassVar[int]
    CROSS_RATE_FIELD_NUMBER: _ClassVar[int]
    EQUITY_FIELD_NUMBER: _ClassVar[int]
    UNREALIZED_PROFIT_FIELD_NUMBER: _ClassVar[int]
    name: str
    balance: float
    cross_rate: float
    equity: float
    unrealized_profit: float
    def __init__(
        self,
        name: _Optional[str] = ...,
        balance: _Optional[float] = ...,
        cross_rate: _Optional[float] = ...,
        equity: _Optional[float] = ...,
        unrealized_profit: _Optional[float] = ...,
    ) -> None: ...

class MoneyRow(_message.Message):
    __slots__ = ("market", "currency", "balance")
    MARKET_FIELD_NUMBER: _ClassVar[int]
    CURRENCY_FIELD_NUMBER: _ClassVar[int]
    BALANCE_FIELD_NUMBER: _ClassVar[int]
    market: _common_pb2.Market
    currency: str
    balance: float
    def __init__(
        self,
        market: _Optional[_Union[_common_pb2.Market, str]] = ...,
        currency: _Optional[str] = ...,
        balance: _Optional[float] = ...,
    ) -> None: ...

class GetPortfolioRequest(_message.Message):
    __slots__ = ("client_id", "content")
    CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    client_id: str
    content: PortfolioContent
    def __init__(
        self,
        client_id: _Optional[str] = ...,
        content: _Optional[_Union[PortfolioContent, _Mapping]] = ...,
    ) -> None: ...

class GetPortfolioResult(_message.Message):
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
    content: PortfolioContent
    equity: float
    balance: float
    positions: _containers.RepeatedCompositeFieldContainer[PositionRow]
    currencies: _containers.RepeatedCompositeFieldContainer[CurrencyRow]
    money: _containers.RepeatedCompositeFieldContainer[MoneyRow]
    def __init__(
        self,
        client_id: _Optional[str] = ...,
        content: _Optional[_Union[PortfolioContent, _Mapping]] = ...,
        equity: _Optional[float] = ...,
        balance: _Optional[float] = ...,
        positions: _Optional[_Iterable[_Union[PositionRow, _Mapping]]] = ...,
        currencies: _Optional[_Iterable[_Union[CurrencyRow, _Mapping]]] = ...,
        money: _Optional[_Iterable[_Union[MoneyRow, _Mapping]]] = ...,
    ) -> None: ...
