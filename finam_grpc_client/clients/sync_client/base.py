import logging
import time
from abc import ABC
from concurrent.futures import ThreadPoolExecutor
from queue import Queue
from threading import Event, Thread

from google.protobuf.message import Message
from grpc import (
    UnaryStreamMultiCallable,
    UnaryUnaryMultiCallable,
    secure_channel,
    ssl_channel_credentials,
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
    OrderTradeResponse,
)

from ..base import BaseClient
from ..client_interfaces import SyncClientInterface


class BaseSyncClient(BaseClient, SyncClientInterface, ABC):
    logger = logging.getLogger("finam_grpc_client.BaseSyncClient")

    __subscribe_events: dict[
        tuple[str, ...] | str | tuple[str, TimeFrame.ValueType], Event
    ] = {}
    """События для остановки задач по обработке подписок."""
    __order_trade_requests: Queue[OrderTradeResponse] = Queue(maxsize=20)
    """Очередь для заявок на подписку/отписку."""

    def __init__(
        self,
        url: str,
        token: str,
        handlers_thread_amount=4,
        workers_thread_amount=6,
    ) -> None:
        channel = secure_channel(url, ssl_channel_credentials())
        super().__init__(channel=channel, token=token)
        self.__refresh_token_task: Thread | None = None
        self.__subscribe_handlers_pool: ThreadPoolExecutor | None = None
        self.__subscribe_workers_pool: Thread | None = None
        self.__background_tasks: ThreadPoolExecutor | None = None
        self.__on_quote = self.default_handler
        self.__on_order_book = self.default_handler
        self.__on_latest_trade = self.default_handler
        self.__on_bar = self.default_handler
        self.__on_order_trade = self.default_handler
        self.__workers_thread_amount = workers_thread_amount
        self.__handlers_thread_amount = handlers_thread_amount
        self.__types_handlers = {
            SubscribeQuoteRequest: "on_quote",
            SubscribeOrderBookRequest: "on_order_book",
            SubscribeLatestTradesRequest: "on_latest_trade",
            SubscribeBarsRequest: "on_bar",
        }

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()

    @property
    def metadata(self) -> tuple[tuple[str, str], ...]:
        return (("authorization", self.session_token),)

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

    def start(self):
        self._start()
        self._start_subscribe_workers()
        self._start_subscribe_handlers()
        self._get_session_token()
        if self.__refresh_token_task is None:
            self.__refresh_token_task = r = Thread(
                target=self.__session_token_job,
                name="RefreshToken",
                daemon=True,
            )
            r.start()
        details = self._get_session_token_details()
        self.account_ids = tuple(details.account_ids)

    def stop(self):
        self._stop()
        self._stop_subscribe_handlers()
        self._stop_subscribe_workers()
        self.channel.close()
        self.__on_quote = self.default_handler
        self.__on_order_book = self.default_handler
        self.__on_latest_trade = self.default_handler
        self.__on_bar = self.default_handler
        self.__on_order_trade = self.default_handler
        self.__refresh_token_task = None
        self.logger.info("Соединение закрыто")

    def _execute_request(
        self, method: UnaryUnaryMultiCallable, message: Message
    ):
        """
        Метод для отправки запросов к Api.

        :param method: Тип запроса.
        :param message: Тело запроса.

        :return: Модель ответа на запрос.
        """
        return self.__execute_request(method, message, self.metadata)

    def _get_session_token(self) -> None:
        """Получение токена сессии"""
        self.logger.info("Запрос токена сессии")
        response: AuthResponse = self.__execute_request(
            self._auth.Auth, AuthRequest(secret=self.token)
        )
        self.session_token = response.token
        self.logger.debug("Получен токен сессии: [\n%s\n]", self.session_token)

    def _get_session_token_details(self) -> TokenDetailsResponse:
        """Получение информации о токене сессии."""
        self.logger.info("Запрос информации о токене сессии")
        res: TokenDetailsResponse = self.__execute_request(
            self._auth.TokenDetails,
            TokenDetailsRequest(token=self.session_token),
        )
        self.logger.debug("Ответ на запрос информации о токене: [\n%s\n]", res)
        return res

    def _start_subscribe_workers(self):
        """Запуск обработки событий подписок."""
        self.logger.info("Запуск обработки событий подписок")
        if self.__subscribe_workers_pool:
            self.logger.warning("Обработка событий подписок уже запущена")
            return
        self.__background_tasks = ThreadPoolExecutor(
            max_workers=self.__workers_thread_amount,
            thread_name_prefix="BackgroundTask",
        )
        self.__subscribe_workers_pool = Thread(
            target=self.__order_trade_events_worker,
            name="OrderTradeEventsWorker",
            daemon=True,
        )

    def _start_subscribe_handlers(self):
        """Запуск получения событий подписок."""
        self.logger.info("Запуск получения событий подписок")
        if self.__subscribe_handlers_pool:
            self.logger.warning("Получение событий уже запущено")
            return
        self.__subscribe_handlers_pool = ThreadPoolExecutor(
            max_workers=self.__handlers_thread_amount,
            thread_name_prefix="SubscribeHandler",
        )

    def _stop_subscribe_workers(self):
        """Остановка обработки событий подписок."""
        self.logger.info("Остановка обработки событий подписок")
        if self.__subscribe_workers_pool is None:
            self.logger.warning("Обработка событий подписок уже остановлена")
            return
        while self.__subscribe_workers_pool.is_alive():
            self.logger.debug("Ожидание остановки обработки событий подписок")
            time.sleep(1)
        self.__subscribe_workers_pool = None
        self.__background_tasks.shutdown(cancel_futures=True)
        self.logger.info("Обработка событий подписок остановлена")

    def _stop_subscribe_handlers(self):
        """Остановка получения событий подписок."""
        self.logger.info("Остановка получения событий")
        if self.__subscribe_handlers_pool is None:
            self.logger.warning("Получение событий уже остановлено")
            return
        for e in self.__subscribe_events.values():
            e.set()
        self.__subscribe_handlers_pool.shutdown(cancel_futures=True)
        self.__subscribe_handlers_pool = None
        self.logger.info("Получение событий остановлено")

    def _subscribe_unary_stream(
        self, request, method: UnaryStreamMultiCallable
    ):
        handler = self.__types_handlers[type(request)]

        def subscribe_worker(flag: Event):
            for event in method(request=request, metadata=self.metadata):
                if flag.is_set():
                    break
                self.logger.debug("Получен новый event: [\n%s\n]", event)
                h = getattr(self, handler)
                self.__background_tasks.submit(h, event)

        e = Event()
        self.__subscribe_handlers_pool.submit(subscribe_worker, flag=e)
        key = getattr(request, "symbol", None) or tuple(
            getattr(request, "symbols")
        )
        timeframe = getattr(request, "timeframe", None)
        if timeframe:
            key = (key, timeframe)
        self.__subscribe_events[key] = e

    def _unsubscribe_unary_stream(self, request):
        key = getattr(request, "symbol", None) or tuple(
            getattr(request, "symbols")
        )
        timeframe = getattr(request, "timeframe", None)
        if timeframe:
            key = (key, timeframe)
        event = self.__subscribe_events.pop(key, None)
        if not event:
            return
        event.set()

    def _execute_order_trade_subscribe_request(
        self, request: OrderTradeRequest
    ) -> None:
        """Добавление запроса на подписку в очередь."""
        self.__order_trade_requests.put(request)

    def __session_token_job(self):
        self.logger.info("Запуск задачи по обновлению токена сессии")
        while self.state:
            time.sleep(
                self.session_lifetime - 10
            )  # За десять секунд до конца.
            self._get_session_token()
        self.logger.info("Завершение задачи по обновлению токена сессии")

    def __order_trade_events_worker(self) -> None:

        def request_iterator():
            while self.state:
                yield self.__order_trade_requests.get()

        for event in self._orders.SubscribeOrderTrade(
            request_iterator=request_iterator(),
            metadata=self.metadata,
        ):
            self.logger.debug("Получен новый event: [\n%s\n]", event)
            self.__background_tasks.submit(self.on_order_trade, event)

    @staticmethod
    def __execute_request(
        method: UnaryUnaryMultiCallable,
        message: Message,
        metadata: tuple[tuple[str, str], ...] | None = None,
    ):
        return method(request=message, metadata=metadata)
