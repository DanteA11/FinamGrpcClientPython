from finam_grpc_client.models.proto import common_pb2 as _common_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PriceSign(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PRICE_SIGN_UNSPECIFIED: _ClassVar[PriceSign]
    PRICE_SIGN_POSITIVE: _ClassVar[PriceSign]
    PRICE_SIGN_NON_NEGATIVE: _ClassVar[PriceSign]
    PRICE_SIGN_ANY: _ClassVar[PriceSign]

PRICE_SIGN_UNSPECIFIED: PriceSign
PRICE_SIGN_POSITIVE: PriceSign
PRICE_SIGN_NON_NEGATIVE: PriceSign
PRICE_SIGN_ANY: PriceSign

class Security(_message.Message):
    __slots__ = (
        "code",
        "board",
        "market",
        "decimals",
        "lot_size",
        "min_step",
        "currency",
        "short_name",
        "properties",
        "time_zone_name",
        "bp_cost",
        "accrued_interest",
        "price_sign",
        "ticker",
        "lot_divider",
    )
    CODE_FIELD_NUMBER: _ClassVar[int]
    BOARD_FIELD_NUMBER: _ClassVar[int]
    MARKET_FIELD_NUMBER: _ClassVar[int]
    DECIMALS_FIELD_NUMBER: _ClassVar[int]
    LOT_SIZE_FIELD_NUMBER: _ClassVar[int]
    MIN_STEP_FIELD_NUMBER: _ClassVar[int]
    CURRENCY_FIELD_NUMBER: _ClassVar[int]
    SHORT_NAME_FIELD_NUMBER: _ClassVar[int]
    PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    TIME_ZONE_NAME_FIELD_NUMBER: _ClassVar[int]
    BP_COST_FIELD_NUMBER: _ClassVar[int]
    ACCRUED_INTEREST_FIELD_NUMBER: _ClassVar[int]
    PRICE_SIGN_FIELD_NUMBER: _ClassVar[int]
    TICKER_FIELD_NUMBER: _ClassVar[int]
    LOT_DIVIDER_FIELD_NUMBER: _ClassVar[int]
    code: str
    board: str
    market: _common_pb2.Market
    decimals: int
    lot_size: int
    min_step: int
    currency: str
    short_name: str
    properties: int
    time_zone_name: str
    bp_cost: float
    accrued_interest: float
    price_sign: PriceSign
    ticker: str
    lot_divider: int
    def __init__(
        self,
        code: _Optional[str] = ...,
        board: _Optional[str] = ...,
        market: _Optional[_Union[_common_pb2.Market, str]] = ...,
        decimals: _Optional[int] = ...,
        lot_size: _Optional[int] = ...,
        min_step: _Optional[int] = ...,
        currency: _Optional[str] = ...,
        short_name: _Optional[str] = ...,
        properties: _Optional[int] = ...,
        time_zone_name: _Optional[str] = ...,
        bp_cost: _Optional[float] = ...,
        accrued_interest: _Optional[float] = ...,
        price_sign: _Optional[_Union[PriceSign, str]] = ...,
        ticker: _Optional[str] = ...,
        lot_divider: _Optional[int] = ...,
    ) -> None: ...
