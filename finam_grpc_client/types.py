"""В модуле содержатся типы данных, необходимые для методов."""

from finam_grpc_client.grpc.tradeapi.v1.marketdata.marketdata_service_pb2 import (
    TimeFrame,
)
from finam_grpc_client.grpc.tradeapi.v1.orders.orders_service_pb2 import (
    Leg,
    OrderTradeRequest,
    OrderType,
    StopCondition,
    TimeInForce,
)
from finam_grpc_client.grpc.tradeapi.v1.side_pb2 import Side

DataType = OrderTradeRequest.DataType

__all__ = (
    "TimeFrame",
    "OrderType",
    "TimeInForce",
    "StopCondition",
    "Leg",
    "Side",
    "DataType",
)
