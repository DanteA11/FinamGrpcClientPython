import logging
from abc import ABC
from typing import Generic, TypeVar

from google.protobuf.timestamp_pb2 import Timestamp
from google.type.interval_pb2 import Interval
from grpc import Channel
from grpc.aio import Channel as AsyncChannel

from finam_grpc_client.grpc.tradeapi.v1.accounts.accounts_service_pb2_grpc import (
    AccountsServiceStub,
)
from finam_grpc_client.grpc.tradeapi.v1.assets.assets_service_pb2_grpc import (
    AssetsServiceStub,
)
from finam_grpc_client.grpc.tradeapi.v1.auth.auth_service_pb2_grpc import (
    AuthServiceStub,
)
from finam_grpc_client.grpc.tradeapi.v1.marketdata.marketdata_service_pb2_grpc import (
    MarketDataServiceStub,
)
from finam_grpc_client.grpc.tradeapi.v1.orders.orders_service_pb2_grpc import (
    OrdersServiceStub,
)

from .client_interfaces import State

_C = TypeVar("_C", Channel, AsyncChannel)


class BaseClient(Generic[_C], ABC):
    logger = logging.getLogger("finam_grpc_client.BaseClient")

    __jwt_token_lt = 15 * 60  # 15 минут.
    """Время жизни токена."""

    def __init__(self, channel: _C, token: str) -> None:
        self.__channel = channel
        self.__token = token
        self.__session_token = ""
        self.__state: State = State.Stopped
        self.__account_ids = ()
        self._auth = AuthServiceStub(channel)
        self._accounts = AccountsServiceStub(channel)
        self._assets = AssetsServiceStub(channel)
        self._orders = OrdersServiceStub(channel)
        self._market_data = MarketDataServiceStub(channel)

    @property
    def state(self) -> State:
        return self.__state

    @property
    def session_lifetime(self) -> int:
        return self.__jwt_token_lt

    @property
    def token(self) -> str:
        return self.__token

    @property
    def session_token(self) -> str:
        return self.__session_token

    @session_token.setter
    def session_token(self, value: str) -> None:
        self.__session_token = value

    @property
    def account_ids(self) -> tuple[str, ...]:
        return self.__account_ids

    @account_ids.setter
    def account_ids(self, value: tuple[str, ...]) -> None:
        self.__account_ids = value

    @property
    def channel(self) -> _C:
        return self.__channel

    def _start(self):
        self.logger.warning("Начало работы")
        if self.state:
            self.logger.warning("Уже запущено")
            return
        self.__state = State.Started

    def _stop(self):
        self.logger.warning("Завершение работы")
        if not self.state:
            self.logger.warning("Уже остановлено")
            return
        self.__state = State.Stopped

    @staticmethod
    def _create_interval(start_time, end_time):
        from_ = Timestamp()
        to_ = Timestamp()
        from_.FromDatetime(start_time)
        to_.FromDatetime(end_time)
        return Interval(
            start_time=from_,
            end_time=to_,
        )
