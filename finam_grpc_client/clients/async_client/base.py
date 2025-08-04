"""Базовый класс и интерфейс клиента."""

import asyncio
import logging
from abc import ABC
from logging import Logger
from typing import Callable, Coroutine

from google.protobuf.message import Message
from grpc import StatusCode, ssl_channel_credentials
from grpc.aio import (
    AioRpcError,
    Metadata,
    UnaryStreamCall,
    UnaryStreamMultiCallable,
    UnaryUnaryMultiCallable,
    secure_channel,
)

from finam_grpc_client.grpc.tradeapi.v1.auth.auth_service_pb2 import (
    AuthRequest,
    AuthResponse,
    TokenDetailsRequest,
    TokenDetailsResponse,
)
from finam_grpc_client.grpc.tradeapi.v1.marketdata.marketdata_service_pb2 import (
    SubscribeBarsRequest,
    SubscribeLatestTradesRequest,
    SubscribeOrderBookRequest,
    SubscribeQuoteRequest,
    TimeFrame,
)
from finam_grpc_client.grpc.tradeapi.v1.orders.orders_service_pb2 import (
    OrderTradeRequest,
)

from ..base import BaseClient
from ..client_interfaces import AsyncClientInterface


class BaseAsyncClient(BaseClient, AsyncClientInterface, ABC):
    """Базовый класс асинхронного клиента."""

    __subscribe_calls: dict[
        tuple[str, ...] | str | tuple[str, TimeFrame.ValueType],
        UnaryStreamCall,
    ] = {}
    """Задачи по обработке подписок."""
    __order_trade_requests: asyncio.Queue[OrderTradeRequest] = asyncio.Queue(
        maxsize=20
    )
    """Очередь для заявок на подписку/отписку."""
    __background_tasks: set[asyncio.Task] = set()
    """Задачи по обработке пришедших событий."""

    logger: Logger = logging.getLogger("finam_grpc_client.BaseAsyncClient")

    def __init__(
        self,
        url: str,
        token: str,
    ) -> None:
        channel = secure_channel(url, ssl_channel_credentials())
        super().__init__(channel=channel, token=token)
        self.__refresh_token_task: asyncio.Task | None = None
        self.__subscribe_workers: asyncio.Task | None = None
        self.__on_quote = self.default_handler
        self.__on_order_book = self.default_handler
        self.__on_latest_trade = self.default_handler
        self.__on_bar = self.default_handler
        self.__on_order_trade = self.default_handler
        self.__types_handlers = {
            SubscribeQuoteRequest: "on_quote",
            SubscribeOrderBookRequest: "on_order_book",
            SubscribeLatestTradesRequest: "on_latest_trade",
            SubscribeBarsRequest: "on_bar",
        }

    async def __aenter__(self):
        """Вход в менеджер контекста."""
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Выход из менеджера контекста."""
        await self.stop()

    @property
    def metadata(self) -> Metadata:
        """Метаданные для отправки на сервер."""
        return Metadata(
            ("authorization", self.session_token),
        )

    @property
    def on_quote(self):
        return self.__on_quote

    @on_quote.setter
    def on_quote(self, value):
        self.logger.debug("Назначение нового обработчика on_quote: %s", value)
        self.__on_quote = value

    @property
    def on_order_book(self):
        return self.__on_order_book

    @on_order_book.setter
    def on_order_book(self, value):
        self.logger.debug(
            "Назначение нового обработчика on_order_book: %s", value
        )
        self.__on_order_book = value

    @property
    def on_latest_trade(self):
        return self.__on_latest_trade

    @on_latest_trade.setter
    def on_latest_trade(self, value):
        self.logger.debug(
            "Назначение нового обработчика on_latest_trade: %s", value
        )
        self.__on_latest_trade = value

    @property
    def on_bar(self):
        return self.__on_bar

    @on_bar.setter
    def on_bar(self, value):
        self.logger.debug("Назначение нового обработчика on_bar: %s", value)
        self.__on_bar = value

    @property
    def on_order_trade(self):
        return self.__on_order_trade

    @on_order_trade.setter
    def on_order_trade(self, value):
        self.logger.debug(
            "Назначение нового обработчика on_order_trade: %s", value
        )
        self.__on_order_trade = value

    async def start(self):
        if not self._start():
            return
        await self._get_session_token()
        self._start_subscribe_workers()
        if self.__refresh_token_task is None:
            self.__refresh_token_task = asyncio.create_task(
                self.__session_token_job(), name="RefreshToken"
            )
        details = await self._get_session_token_details()
        self.account_ids = tuple(details.account_ids)

    async def stop(self):
        if not self._stop():
            return
        await self.channel.close(None)
        self.logger.info("Соединение закрыто")

    def _stop(self):
        if not super()._stop():
            return False
        self._stop_subscribe_workers()
        self.__on_quote = self.default_handler
        self.__on_order_book = self.default_handler
        self.__on_latest_trade = self.default_handler
        self.__on_bar = self.default_handler
        self.__on_order_trade = self.default_handler
        if self.__refresh_token_task is not None:
            self.__refresh_token_task.cancel()
        return True

    async def _get_session_token(self) -> None:
        """Получение токена сессии"""
        self.logger.info("Запрос токена сессии")
        response: AuthResponse = await self.__execute_request(
            self._auth.Auth, AuthRequest(secret=self.token)
        )
        self.session_token = response.token
        self.logger.debug("Получен токен сессии: [\n%s\n]", self.session_token)

    async def _get_session_token_details(self) -> TokenDetailsResponse:
        """Получение информации о токене сессии."""
        self.logger.info("Запрос информации о токене сессии")
        res: TokenDetailsResponse = await self.__execute_request(
            self._auth.TokenDetails,
            TokenDetailsRequest(token=self.session_token),
        )
        self.logger.debug("Ответ на запрос информации о токене: [\n%s\n]", res)
        return res

    def _start_subscribe_workers(self):
        """Запуск обработки событий подписок."""
        self.logger.info("Запуск обработки событий подписок")
        if self.__subscribe_workers:
            self.logger.warning("Обработка событий подписок уже запущена")
            return
        self.__subscribe_workers = asyncio.create_task(
            self.__order_trade_events_worker(), name="OrderTradeEventsWorker"
        )

    def _stop_subscribe_workers(self):
        """Остановка обработки событий подписок."""
        self.logger.info("Остановка обработки событий подписок")
        if self.__subscribe_workers is None:
            self.logger.warning("Обработка событий подписок уже остановлена")
            return
        self.__subscribe_workers.cancel()
        self.__subscribe_workers = None

    async def _execute_request(
        self, method: UnaryUnaryMultiCallable, message: Message
    ):
        """
        Метод для отправки запросов к Api.

        :param method: Тип запроса.
        :param message: Тело запроса.

        :return: Модель ответа на запрос.
        """
        return await self.__execute_request(method, message, self.metadata)

    def _subscribe_unary_stream(
        self,
        request,
        method: UnaryStreamMultiCallable,
        worker: Callable[[Message], Coroutine] | None = None,
    ):
        handler = self.__types_handlers[type(request)]
        key = getattr(request, "symbol", None) or tuple(
            getattr(request, "symbols")
        )
        timeframe = getattr(request, "timeframe", None)

        if timeframe:
            key = (key, timeframe)
        if key in self.__subscribe_calls:
            self.logger.warning("Подписка уже существует: %s", request)
            return

        async def subscribe_worker():
            count = 0
            while True:
                try:
                    call = method(request=request, metadata=self.metadata)
                    self.__subscribe_calls[key] = call
                    call.add_done_callback(
                        lambda x: self.__subscribe_calls.pop(key, None)
                    )
                    count = 0
                    async for event in call:
                        self.logger.debug(
                            "Получен новый event: [\n%s\n]", event
                        )
                        h = worker or getattr(self, handler)
                        t = asyncio.create_task(h(event))
                        self.__background_tasks.add(t)
                        t.add_done_callback(self.__background_tasks.discard)
                except AioRpcError as exc:
                    match exc.code():
                        case StatusCode.CANCELLED:
                            self.logger.info(
                                "Принудительная отмена подписки %s", request
                            )
                            break
                        case StatusCode.INTERNAL | StatusCode.UNKNOWN:
                            count += 1
                            if count > 3:
                                self.logger.error(
                                    "Достигнуто максимальное количество попыток соединения для подписки %s. Соединение разорвано",
                                    request,
                                )
                                break
                            self.logger.warning(
                                "Разрыв соединения подписки %s с ошибкой: %s. Переподключение.",
                                request,
                                exc,
                            )
                            continue
                    self.logger.error(
                        "При обработке подписки на ордера и сделки произошла ошибка: %s",
                        exc,
                    )
                    break

        task = asyncio.create_task(subscribe_worker(), name=str(key))
        self.__background_tasks.add(task)
        task.add_done_callback(self.__background_tasks.discard)

    def _unsubscribe_unary_stream(self, request):
        key = getattr(request, "symbol", None) or tuple(
            getattr(request, "symbols")
        )
        timeframe = getattr(request, "timeframe", None)
        if timeframe:
            key = (key, timeframe)
        call = self.__subscribe_calls.pop(key, None)
        if call:
            call.cancel()

    async def _execute_order_trade_subscribe_request(
        self, request: OrderTradeRequest
    ) -> None:
        """Добавление запроса на подписку в очередь."""
        await self.__order_trade_requests.put(request)

    async def __session_token_job(self):
        self.logger.info("Запуск задачи по обновлению токена сессии")
        try:
            while self.state:
                await asyncio.sleep(
                    self.session_lifetime - 10
                )  # За десять секунд до конца.
                await self._get_session_token()
            self.logger.info("Завершение задачи по обновлению токена сессии")
        except asyncio.CancelledError:
            self.logger.info("Отмена задачи по обновлению токена сессии")
        finally:
            self.__refresh_token_task = None

    async def __order_trade_events_worker(self) -> None:

        async def request_iterator():
            while self.state:
                yield await self.__order_trade_requests.get()

        count = 0
        while True:
            try:
                call = self._orders.SubscribeOrderTrade(
                    request_iterator=request_iterator(),
                    metadata=self.metadata,
                )
                count = 0
                async for event in call:
                    self.logger.debug(
                        "Получен новый OrderTrade: [\n%s\n]", event
                    )
                    task = asyncio.create_task(self.on_order_trade(event))
                    self.__background_tasks.add(task)
                    task.add_done_callback(self.__background_tasks.discard)
            except AioRpcError as exc:
                match exc.code():
                    case StatusCode.CANCELLED:
                        self.logger.info(
                            "Принудительная отмена подписки на ордера и сделки."
                        )
                        break
                    case StatusCode.INTERNAL | StatusCode.UNKNOWN:
                        count += 1
                        if count > 3:
                            self.logger.error(
                                "Достигнуто максимальное количество попыток соединения для подписки на ордера и сделки. Соединение разорвано"
                            )
                            await self.stop()
                            break
                        self.logger.warning(
                            "Разрыв соединения подписки на ордера и сделки с ошибкой: %s. Переподключение.",
                            exc,
                        )
                        continue
                self.logger.error(
                    "При обработке подписки на ордера и сделки произошла ошибка: %s",
                    exc,
                )
                await self.stop()
                break

    @staticmethod
    async def __execute_request(
        method: UnaryUnaryMultiCallable,
        message: Message,
        metadata: Metadata | None = None,
    ):
        return await method(request=message, metadata=metadata)
