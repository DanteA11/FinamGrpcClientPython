"""Классы для работы с подписками."""

import asyncio
from abc import ABC, abstractmethod
from logging import Logger
from typing import Awaitable, Callable

from google.protobuf.message import Message
from grpc import RpcError

from finam_grpc_client.models.grpc.events_pb2_grpc import EventsStub
from finam_grpc_client.models.proto.common_pb2 import ResponseEvent
from finam_grpc_client.models.proto.events_pb2 import (
    Event,
    KeepAliveRequest,
    OrderBookEvent,
    OrderEvent,
    PortfolioEvent,
    SubscriptionRequest,
    TradeEvent,
)


class SubscribesInterface(ABC):
    """Интерфейс для работы с подписками."""

    @abstractmethod
    async def subscribe_orders_trades(self, *args, **kwargs):
        """Подписка на заявки и сделки."""

    @abstractmethod
    async def unsubscribe_orders_trades(self, *args, **kwargs):
        """Отмена подписки на заявки и сделки."""

    @abstractmethod
    async def subscribe_order_book(self, *args, **kwargs):
        """Подписка на стакан."""

    @abstractmethod
    async def unsubscribe_book(self, *args, **kwargs):
        """Отмена подписки на стакан."""


class SubscribesMixin(SubscribesInterface, ABC):
    """Класс-миксин для работы с подписками."""

    _keep_alive_task: asyncio.Task | None = None
    _subscriptions_task: asyncio.Task | None = None
    __subscribe_active: bool = False
    __requests_queue: asyncio.Queue[Message] = asyncio.Queue()
    __for_comparison = (
        OrderEvent(),
        TradeEvent(),
        OrderBookEvent(),
        PortfolioEvent(),
        ResponseEvent(),
    )

    logger: Logger
    __keep_alive_request_id: str
    __on_order: Callable[[OrderEvent], Awaitable]
    __on_trade: Callable[[TradeEvent], Awaitable]
    __on_order_book: Callable[[OrderBookEvent], Awaitable]
    __on_portfolio: Callable[[PortfolioEvent], Awaitable]
    __on_response: Callable[[ResponseEvent], Awaitable]

    def __init__(self, keep_alive_request_id: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__keep_alive_request_id = keep_alive_request_id
        self._events = EventsStub(self.channel)  # type: ignore
        self.on_order = self.default_handler
        self.on_trade = self.default_handler
        self.on_order_book = self.default_handler
        self.on_portfolio = self.default_handler
        self.on_response = self.default_handler

    async def close(self):
        """Закрывает соединение."""
        self._cancel_tasks()
        await super().close()  # type: ignore

    @property
    def on_order(self) -> Callable[[OrderEvent], Awaitable]:
        """Обработчик событий заявок."""
        return self.__on_order

    @on_order.setter
    def on_order(self, handler: Callable[[OrderEvent], Awaitable]) -> None:
        """Обработчик событий заявок."""
        self.__on_order = handler

    @property
    def on_trade(self) -> Callable[[TradeEvent], Awaitable]:
        """Обработчик событий сделок."""
        return self.__on_trade

    @on_trade.setter
    def on_trade(self, handler: Callable[[TradeEvent], Awaitable]) -> None:
        """Обработчик событий сделок."""
        self.__on_trade = handler

    @property
    def on_order_book(self) -> Callable[[OrderBookEvent], Awaitable]:
        """Обработчик событий стакана."""
        return self.__on_order_book

    @on_order_book.setter
    def on_order_book(
        self, handler: Callable[[OrderBookEvent], Awaitable]
    ) -> None:
        """Обработчик событий стакана."""
        self.__on_order_book = handler

    @property
    def on_portfolio(self) -> Callable[[PortfolioEvent], Awaitable]:
        """Обработчик событий портфеля."""
        return self.__on_portfolio

    @on_portfolio.setter
    def on_portfolio(
        self, handler: Callable[[PortfolioEvent], Awaitable]
    ) -> None:
        """Обработчик событий портфеля."""
        self.__on_portfolio = handler

    @property
    def on_response(self) -> Callable[[ResponseEvent], Awaitable]:
        """Обработчик общих событий."""
        return self.__on_response

    @on_response.setter
    def on_response(
        self, handler: Callable[[ResponseEvent], Awaitable]
    ) -> None:
        """Обработчик общих событий."""
        self.__on_response = handler

    @staticmethod
    async def default_handler(
        event: (
            OrderEvent
            | TradeEvent
            | OrderBookEvent
            | PortfolioEvent
            | ResponseEvent
        ),
    ):
        """Обработчик по умолчанию."""

    async def on_event(self, event: Event):
        """
        Получение нового события.

        Разносит события по обработчикам.

        :param event: Событие.
        """
        self.logger.info("Пришло событие: %s.", event)
        if event.order != self.__for_comparison[0]:
            await self.on_order(event.order)
        elif event.trade != self.__for_comparison[1]:
            await self.on_trade(event.trade)
        elif event.order_book != self.__for_comparison[2]:
            await self.on_order_book(event.order_book)
        elif event.portfolio != self.__for_comparison[3]:
            await self.on_portfolio(event.portfolio)
        elif event.response != self.__for_comparison[4]:
            await self.on_response(event.response)

    def _create_tasks(self) -> None:
        """Запуск фоновых задач."""
        self.logger.debug(
            "Создание задач для обработки "
            "подписок и поддержания активности."
        )
        self._subscriptions_task = asyncio.create_task(
            self._subscription_handler()
        )
        self._keep_alive_task = asyncio.create_task(self._keep_alive_handler())
        self.__subscribe_active = True

    def _cancel_tasks(self) -> None:
        """Отмена фоновых задач."""
        ka_res = None
        sw_res = None
        if self._keep_alive_task:
            ka_res = self._keep_alive_task.cancel()
        if self._subscriptions_task:
            sw_res = self._subscriptions_task.cancel()
        self.logger.debug(
            "Поддержание активности отменено: %s, "
            "обработка подписок отменена: %s.",
            ka_res,
            sw_res,
        )
        self.__subscribe_active = False

    async def _keep_alive_handler(self) -> None:
        """Поддержание активности."""
        request = SubscriptionRequest(
            keep_alive_request=KeepAliveRequest(
                request_id=self.__keep_alive_request_id
            )
        )
        while True:
            await asyncio.sleep(120)
            await self.__requests_queue.put(request)
            self.logger.debug("Отправлен запрос для поддержания активности.")

    async def _execute_subscribe_request(
        self, request: SubscriptionRequest
    ) -> None:
        """Добавление подписки в очередь."""
        if not self.__subscribe_active:
            self._create_tasks()
        await self.__requests_queue.put(request)

    async def _subscription_handler(self) -> None:
        """Обработка подписок."""

        async def request_iterator():
            while True:
                yield await self.__requests_queue.get()

        try:
            async for event in self._events.GetEvents(
                request_iterator=request_iterator(),
                metadata=self.metadata,  # type: ignore
            ):
                await self.on_event(event)
        except RpcError as exc:
            self.logger.warning(
                "При получении события произошла ошибка: %s.", exc
            )
