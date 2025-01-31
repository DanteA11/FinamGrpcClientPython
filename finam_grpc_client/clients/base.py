"""Базовый класс и интерфейс клиента."""

from abc import ABC, abstractmethod
from logging import Logger
from typing import Sequence

from google.protobuf.message import Message
from grpc import RpcError, ssl_channel_credentials
from grpc.aio import Channel, UnaryUnaryMultiCallable, secure_channel

from finam_grpc_client.models.grpc.candles_pb2_grpc import CandlesStub
from finam_grpc_client.models.grpc.orders_pb2_grpc import OrdersStub
from finam_grpc_client.models.grpc.portfolios_pb2_grpc import PortfoliosStub
from finam_grpc_client.models.grpc.securities_pb2_grpc import SecuritiesStub
from finam_grpc_client.models.grpc.stops_pb2_grpc import StopsStub


class GrpcClientInterface(ABC):
    """Интерфейс клиента."""

    @abstractmethod
    async def get_candles(self, *args, **kwargs):
        """Получение свечей."""

    @abstractmethod
    async def get_securities(self, *args, **kwargs):
        """Получение списка инструментов."""

    @abstractmethod
    async def get_portfolio(self, *args, **kwargs):
        """Получение информации о портфеле."""

    @abstractmethod
    async def get_orders(self, *args, **kwargs):
        """Получение списка заявок."""

    @abstractmethod
    async def create_order(self, *args, **kwargs):
        """Создание нового ордера."""

    @abstractmethod
    async def cancel_order(self, *args, **kwargs):
        """Отмена ордера."""

    @abstractmethod
    async def get_stops(self, *args, **kwargs):
        """Получение списка стоп-заявок."""

    @abstractmethod
    async def create_stop(self, *args, **kwargs):
        """Создание нового стоп-ордера."""

    @abstractmethod
    async def cancel_stop(self, *args, **kwargs):
        """Отмена стоп-ордера."""


class BaseGrpcClient(GrpcClientInterface, ABC):
    """Базовый класс клиента."""

    __slots__ = (
        "__metadata",
        "__channel",
        "_candles",
        "_orders",
        "_stops",
        "_portfolio",
        "_securities",
    )

    logger: Logger

    def __init__(
        self,
        url: str,
        metadata: Sequence[tuple[str, str | bytes]],
    ):
        self.__metadata = metadata
        self.__channel = channel = secure_channel(
            url, ssl_channel_credentials()
        )
        self._candles = CandlesStub(channel)
        self._orders = OrdersStub(channel)
        self._stops = StopsStub(channel)
        self._portfolio = PortfoliosStub(channel)
        self._securities = SecuritiesStub(channel)

    async def __aenter__(self):
        """Вход в менеджер контекста."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Выход из менеджера контекста."""
        await self.close()

    async def close(self):
        """Закрывает соединение."""
        await self.channel.close(None)
        self.logger.debug("Соединение закрыто.")

    @property
    def metadata(self) -> Sequence[tuple[str, str | bytes]]:
        """Метаданные для отправки на сервер."""
        return self.__metadata

    @property
    def channel(self) -> Channel:
        """Соединение."""
        return self.__channel

    async def _execute_request(
        self,
        method: UnaryUnaryMultiCallable,
        message: Message,
    ):
        """
        Метод для отправки запросов к Api.

        :param method: Тип запроса.
        :param message: Тело запроса.

        :return: Модель ответа на запрос или None, если произошла ошибка.
        """
        try:
            return await method(request=message, metadata=self.metadata)
        except RpcError as exc:
            self.logger.warning(
                "При выполнении запроса произошла ошибка: %s.", exc
            )
