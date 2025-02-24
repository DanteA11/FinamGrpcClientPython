"""Классы для работы с подписками."""

import asyncio
from abc import ABC, abstractmethod
from logging import Logger
from typing import Any, Callable, Coroutine, Never

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
    async def unsubscribe_order_book(self, *args, **kwargs):
        """Отмена подписки на стакан."""


class SubscribesMixin(SubscribesInterface, ABC):
    """
    Класс-миксин для работы с подписками.

    :param keep_alive_request_id: ID для запроса на поддержание активности.
    """

    _keep_alive_task: asyncio.Task | None = None
    """Задача по отправке сообщений на поддержание активности."""
    _subscriptions_task: asyncio.Task | None = None
    """Задача по обработке подписок."""
    _events_task: asyncio.Task | None = None
    """Задача по обработке событий."""
    _background_tasks: set[asyncio.Task] = set()
    """Временные фоновые задачи."""
    __subscribe_active: bool = False
    __requests_queue: asyncio.Queue[Message] = asyncio.Queue()
    __events_queue: asyncio.Queue[Event] = asyncio.Queue()
    __for_comparison = (
        OrderEvent(),
        TradeEvent(),
        OrderBookEvent(),
        PortfolioEvent(),
        ResponseEvent(),
    )

    logger: Logger
    __keep_alive_request_id: str
    __on_order: Callable[[OrderEvent], Coroutine[Any, Any, Never]]
    __on_trade: Callable[[TradeEvent], Coroutine[Any, Any, Never]]
    __on_order_book: Callable[[OrderBookEvent], Coroutine[Any, Any, Never]]
    __on_portfolio: Callable[[PortfolioEvent], Coroutine[Any, Any, Never]]
    __on_response: Callable[[ResponseEvent], Coroutine[Any, Any, Never]]

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
        await self._cancel_tasks()
        await super().close()  # type: ignore

    @property
    def on_order(self) -> Callable[[OrderEvent], Coroutine[Any, Any, Never]]:
        """Обработчик событий заявок."""
        return self.__on_order

    @on_order.setter
    def on_order(
        self, handler: Callable[[OrderEvent], Coroutine[Any, Any, Never]]
    ) -> None:
        """Обработчик событий заявок."""
        self.__on_order = handler

    @property
    def on_trade(self) -> Callable[[TradeEvent], Coroutine[Any, Any, Never]]:
        """Обработчик событий сделок."""
        return self.__on_trade

    @on_trade.setter
    def on_trade(
        self, handler: Callable[[TradeEvent], Coroutine[Any, Any, Never]]
    ) -> None:
        """Обработчик событий сделок."""
        self.__on_trade = handler

    @property
    def on_order_book(
        self,
    ) -> Callable[[OrderBookEvent], Coroutine[Any, Any, Never]]:
        """Обработчик событий стакана."""
        return self.__on_order_book

    @on_order_book.setter
    def on_order_book(
        self, handler: Callable[[OrderBookEvent], Coroutine[Any, Any, Never]]
    ) -> None:
        """Обработчик событий стакана."""
        self.__on_order_book = handler

    @property
    def on_portfolio(
        self,
    ) -> Callable[[PortfolioEvent], Coroutine[Any, Any, Never]]:
        """Обработчик событий портфеля."""
        return self.__on_portfolio

    @on_portfolio.setter
    def on_portfolio(
        self, handler: Callable[[PortfolioEvent], Coroutine[Any, Any, Never]]
    ) -> None:
        """Обработчик событий портфеля."""
        self.__on_portfolio = handler

    @property
    def on_response(
        self,
    ) -> Callable[[ResponseEvent], Coroutine[Any, Any, Never]]:
        """Обработчик общих событий."""
        return self.__on_response

    @on_response.setter
    def on_response(
        self, handler: Callable[[ResponseEvent], Coroutine[Any, Any, Never]]
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
        task = None
        if event.order != self.__for_comparison[0]:
            task = asyncio.create_task(self.on_order(event.order))
        elif event.trade != self.__for_comparison[1]:
            task = asyncio.create_task(self.on_trade(event.trade))
        elif event.order_book != self.__for_comparison[2]:
            task = asyncio.create_task(self.on_order_book(event.order_book))
        elif event.portfolio != self.__for_comparison[3]:
            task = asyncio.create_task(self.on_portfolio(event.portfolio))
        elif event.response != self.__for_comparison[4]:
            task = asyncio.create_task(self.on_response(event.response))
        if not task:
            return
        self._background_tasks.add(task)
        task.add_done_callback(self._background_tasks.discard)

    async def _create_tasks(self) -> None:
        """Запуск фоновых задач."""
        self.logger.debug(
            "Создание задач для обработки "
            "подписок и поддержания активности."
        )
        if not self._subscriptions_task:
            self._subscriptions_task = asyncio.create_task(
                self._subscription_handler()
            )
        if not self._keep_alive_task:
            self._keep_alive_task = asyncio.create_task(
                self._keep_alive_handler()
            )
        if not self._events_task:
            self._events_task = asyncio.create_task(self._events_handler())
        self.__subscribe_active = True

    async def _cancel_tasks(self) -> None:
        """Отмена фоновых задач."""
        ka_res = None
        s_res = None
        e_res = None
        ka_task = self._keep_alive_task
        s_task = self._subscriptions_task
        e_task = self._events_task
        if ka_task:
            ka_res = ka_task.cancel()
        if s_task:
            s_res = s_task.cancel()
        if e_task:
            e_res = e_task.cancel()
        ka_task = ka_task or asyncio.sleep(0)  # type: ignore
        s_task = s_task or asyncio.sleep(0)  # type: ignore
        e_task = e_task or asyncio.sleep(0)  # type: ignore

        await asyncio.gather(ka_task, s_task, e_task, return_exceptions=True)  # type: ignore
        self.logger.debug(
            "Поддержание активности отменено: %s, "
            "обработка подписок отменена: %s, "
            "обработка событий отменена: %s.",
            ka_res,
            s_res,
            e_res,
        )
        self._keep_alive_task = None
        self._subscriptions_task = None
        self._events_task = None
        self.__subscribe_active = False

    async def _events_handler(self) -> None:
        """Обработка событий."""
        while True:
            event = await self.__events_queue.get()
            await self.on_event(event)

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
            await self._create_tasks()
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
                await self.__events_queue.put(event)
        except RpcError as exc:
            self.logger.warning(
                "При получении события произошла ошибка: %s.", exc
            )
