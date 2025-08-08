import logging
from abc import ABC
from typing import Generic, TypeVar

from google.protobuf.timestamp_pb2 import Timestamp
from google.type.interval_pb2 import Interval
from grpc import Channel, RpcError, StatusCode
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

    def _start(self) -> bool:
        self.logger.warning("Начало работы")
        if self.state:
            self.logger.warning("Уже запущено")
            return False
        self.__state = State.Started
        return True

    def _stop(self) -> bool:
        self.logger.warning("Завершение работы")
        if not self.state:
            self.logger.warning("Уже остановлено")
            return False
        self.__state = State.Stopped
        return True

    @classmethod
    def _error_handler(cls, exception: RpcError, count: int, request) -> int:
        """
        Обработчик ошибок подключения к стримам.

        :param exception: Ошибка при подключении.
        :param count: Внешний счетчик ошибок.
        :param request: Информация о запросе.

        :return: Счетчик. Если -1, необходимо выйти из стрима.
        Если >3 выйти и (опционально) завершить подключение.
        """
        match exception.code():
            case StatusCode.CANCELLED:
                cls.logger.info("Принудительная отмена подписки %s", request)
                return -1
            case (
                StatusCode.INTERNAL
                | StatusCode.UNKNOWN
                | StatusCode.UNAVAILABLE
            ):
                count += 1
                if count > 3:
                    cls.logger.error(
                        "Разрыв соединения подписки %s с ошибкой: %s."
                        "Достигнуто максимальное количество попыток. Соединение разорвано",
                        request,
                        exception,
                    )
                else:
                    cls.logger.warning(
                        "Разрыв соединения подписки %s с ошибкой: %s. Переподключение.",
                        request,
                        exception,
                    )
                return count
        cls.logger.error(
            "При обработке подписки на ордера и сделки произошла ошибка: %s",
            exception,
        )
        return 4

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
