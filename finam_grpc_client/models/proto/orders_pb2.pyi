from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf import wrappers_pb2 as _wrappers_pb2
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

class OrderProperty(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ORDER_PROPERTY_UNSPECIFIED: _ClassVar[OrderProperty]
    ORDER_PROPERTY_PUT_IN_QUEUE: _ClassVar[OrderProperty]
    ORDER_PROPERTY_CANCEL_BALANCE: _ClassVar[OrderProperty]
    ORDER_PROPERTY_IMM_OR_CANCEL: _ClassVar[OrderProperty]

class OrderConditionType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ORDER_CONDITION_TYPE_UNSPECIFIED: _ClassVar[OrderConditionType]
    ORDER_CONDITION_TYPE_BID: _ClassVar[OrderConditionType]
    ORDER_CONDITION_TYPE_BID_OR_LAST: _ClassVar[OrderConditionType]
    ORDER_CONDITION_TYPE_ASK: _ClassVar[OrderConditionType]
    ORDER_CONDITION_TYPE_ASK_OR_LAST: _ClassVar[OrderConditionType]
    ORDER_CONDITION_TYPE_TIME: _ClassVar[OrderConditionType]
    ORDER_CONDITION_TYPE_COV_DOWN: _ClassVar[OrderConditionType]
    ORDER_CONDITION_TYPE_COV_UP: _ClassVar[OrderConditionType]
    ORDER_CONDITION_TYPE_LAST_UP: _ClassVar[OrderConditionType]
    ORDER_CONDITION_TYPE_LAST_DOWN: _ClassVar[OrderConditionType]

class OrderStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ORDER_STATUS_UNSPECIFIED: _ClassVar[OrderStatus]
    ORDER_STATUS_NONE: _ClassVar[OrderStatus]
    ORDER_STATUS_ACTIVE: _ClassVar[OrderStatus]
    ORDER_STATUS_CANCELLED: _ClassVar[OrderStatus]
    ORDER_STATUS_MATCHED: _ClassVar[OrderStatus]

ORDER_PROPERTY_UNSPECIFIED: OrderProperty
ORDER_PROPERTY_PUT_IN_QUEUE: OrderProperty
ORDER_PROPERTY_CANCEL_BALANCE: OrderProperty
ORDER_PROPERTY_IMM_OR_CANCEL: OrderProperty
ORDER_CONDITION_TYPE_UNSPECIFIED: OrderConditionType
ORDER_CONDITION_TYPE_BID: OrderConditionType
ORDER_CONDITION_TYPE_BID_OR_LAST: OrderConditionType
ORDER_CONDITION_TYPE_ASK: OrderConditionType
ORDER_CONDITION_TYPE_ASK_OR_LAST: OrderConditionType
ORDER_CONDITION_TYPE_TIME: OrderConditionType
ORDER_CONDITION_TYPE_COV_DOWN: OrderConditionType
ORDER_CONDITION_TYPE_COV_UP: OrderConditionType
ORDER_CONDITION_TYPE_LAST_UP: OrderConditionType
ORDER_CONDITION_TYPE_LAST_DOWN: OrderConditionType
ORDER_STATUS_UNSPECIFIED: OrderStatus
ORDER_STATUS_NONE: OrderStatus
ORDER_STATUS_ACTIVE: OrderStatus
ORDER_STATUS_CANCELLED: OrderStatus
ORDER_STATUS_MATCHED: OrderStatus

class OrderCondition(_message.Message):
    __slots__ = ("type", "price", "time")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    PRICE_FIELD_NUMBER: _ClassVar[int]
    TIME_FIELD_NUMBER: _ClassVar[int]
    type: OrderConditionType
    price: float
    time: _timestamp_pb2.Timestamp
    def __init__(
        self,
        type: _Optional[_Union[OrderConditionType, str]] = ...,
        price: _Optional[float] = ...,
        time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
    ) -> None: ...

class NewOrderRequest(_message.Message):
    __slots__ = (
        "client_id",
        "security_board",
        "security_code",
        "buy_sell",
        "quantity",
        "use_credit",
        "price",
        "property",
        "condition",
        "valid_before",
    )
    CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    SECURITY_BOARD_FIELD_NUMBER: _ClassVar[int]
    SECURITY_CODE_FIELD_NUMBER: _ClassVar[int]
    BUY_SELL_FIELD_NUMBER: _ClassVar[int]
    QUANTITY_FIELD_NUMBER: _ClassVar[int]
    USE_CREDIT_FIELD_NUMBER: _ClassVar[int]
    PRICE_FIELD_NUMBER: _ClassVar[int]
    PROPERTY_FIELD_NUMBER: _ClassVar[int]
    CONDITION_FIELD_NUMBER: _ClassVar[int]
    VALID_BEFORE_FIELD_NUMBER: _ClassVar[int]
    client_id: str
    security_board: str
    security_code: str
    buy_sell: _common_pb2.BuySell
    quantity: int
    use_credit: bool
    price: _wrappers_pb2.DoubleValue
    property: OrderProperty
    condition: OrderCondition
    valid_before: _common_pb2.OrderValidBefore
    def __init__(
        self,
        client_id: _Optional[str] = ...,
        security_board: _Optional[str] = ...,
        security_code: _Optional[str] = ...,
        buy_sell: _Optional[_Union[_common_pb2.BuySell, str]] = ...,
        quantity: _Optional[int] = ...,
        use_credit: bool = ...,
        price: _Optional[_Union[_wrappers_pb2.DoubleValue, _Mapping]] = ...,
        property: _Optional[_Union[OrderProperty, str]] = ...,
        condition: _Optional[_Union[OrderCondition, _Mapping]] = ...,
        valid_before: _Optional[_Union[_common_pb2.OrderValidBefore, _Mapping]] = ...,
    ) -> None: ...

class NewOrderResult(_message.Message):
    __slots__ = ("client_id", "transaction_id", "security_code")
    CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    TRANSACTION_ID_FIELD_NUMBER: _ClassVar[int]
    SECURITY_CODE_FIELD_NUMBER: _ClassVar[int]
    client_id: str
    transaction_id: int
    security_code: str
    def __init__(
        self,
        client_id: _Optional[str] = ...,
        transaction_id: _Optional[int] = ...,
        security_code: _Optional[str] = ...,
    ) -> None: ...

class CancelOrderRequest(_message.Message):
    __slots__ = ("client_id", "transaction_id")
    CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    TRANSACTION_ID_FIELD_NUMBER: _ClassVar[int]
    client_id: str
    transaction_id: int
    def __init__(
        self, client_id: _Optional[str] = ..., transaction_id: _Optional[int] = ...
    ) -> None: ...

class CancelOrderResult(_message.Message):
    __slots__ = ("client_id", "transaction_id")
    CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    TRANSACTION_ID_FIELD_NUMBER: _ClassVar[int]
    client_id: str
    transaction_id: int
    def __init__(
        self, client_id: _Optional[str] = ..., transaction_id: _Optional[int] = ...
    ) -> None: ...

class GetOrdersRequest(_message.Message):
    __slots__ = ("client_id", "include_matched", "include_canceled", "include_active")
    CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_MATCHED_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_CANCELED_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_ACTIVE_FIELD_NUMBER: _ClassVar[int]
    client_id: str
    include_matched: bool
    include_canceled: bool
    include_active: bool
    def __init__(
        self,
        client_id: _Optional[str] = ...,
        include_matched: bool = ...,
        include_canceled: bool = ...,
        include_active: bool = ...,
    ) -> None: ...

class Order(_message.Message):
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
        "security_board",
        "market",
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
    SECURITY_BOARD_FIELD_NUMBER: _ClassVar[int]
    MARKET_FIELD_NUMBER: _ClassVar[int]
    order_no: int
    transaction_id: int
    security_code: str
    client_id: str
    status: OrderStatus
    buy_sell: _common_pb2.BuySell
    created_at: _timestamp_pb2.Timestamp
    price: float
    quantity: int
    balance: int
    message: str
    currency: str
    condition: OrderCondition
    valid_before: _common_pb2.OrderValidBefore
    accepted_at: _timestamp_pb2.Timestamp
    security_board: str
    market: _common_pb2.Market
    def __init__(
        self,
        order_no: _Optional[int] = ...,
        transaction_id: _Optional[int] = ...,
        security_code: _Optional[str] = ...,
        client_id: _Optional[str] = ...,
        status: _Optional[_Union[OrderStatus, str]] = ...,
        buy_sell: _Optional[_Union[_common_pb2.BuySell, str]] = ...,
        created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        price: _Optional[float] = ...,
        quantity: _Optional[int] = ...,
        balance: _Optional[int] = ...,
        message: _Optional[str] = ...,
        currency: _Optional[str] = ...,
        condition: _Optional[_Union[OrderCondition, _Mapping]] = ...,
        valid_before: _Optional[_Union[_common_pb2.OrderValidBefore, _Mapping]] = ...,
        accepted_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        security_board: _Optional[str] = ...,
        market: _Optional[_Union[_common_pb2.Market, str]] = ...,
    ) -> None: ...

class GetOrdersResult(_message.Message):
    __slots__ = ("client_id", "orders")
    CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    ORDERS_FIELD_NUMBER: _ClassVar[int]
    client_id: str
    orders: _containers.RepeatedCompositeFieldContainer[Order]
    def __init__(
        self,
        client_id: _Optional[str] = ...,
        orders: _Optional[_Iterable[_Union[Order, _Mapping]]] = ...,
    ) -> None: ...
