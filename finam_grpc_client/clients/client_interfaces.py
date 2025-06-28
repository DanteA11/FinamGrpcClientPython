from abc import ABC, abstractmethod
from datetime import datetime
from enum import IntEnum
from typing import Any, Callable, Coroutine, Iterable

from google.type.decimal_pb2 import Decimal
from grpc import Channel
from grpc.aio import Channel as AsyncChannel

from finam_grpc_client.grpc.tradeapi.v1.accounts.accounts_service_pb2 import (
    GetAccountResponse,
    TradesResponse,
    TransactionsResponse,
)
from finam_grpc_client.grpc.tradeapi.v1.assets.assets_service_pb2 import (
    AssetsResponse,
    ClockResponse,
    ExchangesResponse,
    GetAssetParamsResponse,
    GetAssetResponse,
    OptionsChainResponse,
    ScheduleResponse,
)
from finam_grpc_client.grpc.tradeapi.v1.marketdata.marketdata_service_pb2 import (
    BarsResponse,
    LatestTradesResponse,
    OrderBookResponse,
    QuoteResponse,
    SubscribeBarsResponse,
    SubscribeLatestTradesResponse,
    SubscribeOrderBookResponse,
    SubscribeQuoteResponse,
    TimeFrame,
)
from finam_grpc_client.grpc.tradeapi.v1.orders.orders_service_pb2 import (
    Leg,
    OrdersResponse,
    OrderState,
    OrderTradeRequest,
    OrderTradeResponse,
    OrderType,
    StopCondition,
    TimeInForce,
)
from finam_grpc_client.grpc.tradeapi.v1.side_pb2 import Side


class State(IntEnum):
    Stopped = 0
    Started = 1


class SyncClientInterface(ABC):
    """Интерфейс синхронного клиента."""

    @abstractmethod
    def __enter__(self) -> "SyncClientInterface":
        """Вход в менеджер контекста."""

    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Выход из менеджера контекста."""

    @property
    @abstractmethod
    def state(self) -> State:
        """Состояние клиента."""

    @property
    @abstractmethod
    def session_token(self) -> str:
        """Токен сессии."""

    @property
    @abstractmethod
    def channel(self) -> Channel:
        """Соединение."""

    @property
    @abstractmethod
    def account_ids(self) -> tuple[str, ...]:
        """Идентификаторы аккаунта."""

    @property
    @abstractmethod
    def on_quote(self) -> Callable[[SubscribeQuoteResponse], Any]:
        """Обработчик подписки на котировки."""

    @on_quote.setter
    @abstractmethod
    def on_quote(self, value: Callable[[SubscribeQuoteResponse], Any]) -> None:
        """Обработчик подписки на котировки."""

    @property
    @abstractmethod
    def on_order_book(self) -> Callable[[SubscribeOrderBookResponse], Any]:
        """Обработчик подписки на стакан."""

    @on_order_book.setter
    @abstractmethod
    def on_order_book(
        self, value: Callable[[SubscribeOrderBookResponse], Any]
    ) -> None:
        """Обработчик подписки на стакан."""

    @property
    @abstractmethod
    def on_latest_trade(
        self,
    ) -> Callable[[SubscribeLatestTradesResponse], Any]:
        """Обработчик подписки на сделки."""

    @on_latest_trade.setter
    @abstractmethod
    def on_latest_trade(
        self, value: Callable[[SubscribeLatestTradesResponse], Any]
    ) -> None:
        """Обработчик подписки на сделки."""

    @property
    @abstractmethod
    def on_bar(self) -> Callable[[SubscribeBarsResponse], Any]:
        """Обработчик подписки на бары."""

    @on_bar.setter
    @abstractmethod
    def on_bar(self, value: Callable[[SubscribeBarsResponse], Any]) -> None:
        """Обработчик подписки на бары."""

    @property
    @abstractmethod
    def on_order_trade(self) -> Callable[[OrderTradeResponse], Any]:
        """Обработчик подписки на собственные заявки и сделки."""

    @on_order_trade.setter
    @abstractmethod
    def on_order_trade(
        self, value: Callable[[OrderTradeResponse], Any]
    ) -> None:
        """Обработчик подписки на собственные заявки и сделки."""

    @abstractmethod
    def start(self) -> None:
        """Выполняет действия, необходимые для начала работы."""

    @abstractmethod
    def stop(self) -> None:
        """Выполняет действия, необходимые при завершении работы."""

    @abstractmethod
    def get_account_info(self, account_id: str) -> GetAccountResponse:
        """
        Получение информации по конкретному аккаунту.

        :param account_id: Идентификатор аккаунта.
        """

    @abstractmethod
    def get_trades(
        self,
        account_id: str,
        limit: int,
        start_time: datetime,
        end_time: datetime,
    ) -> TradesResponse:
        """
        Получение истории по сделкам аккаунта.

        :param account_id: Идентификатор аккаунта.
        :param limit: Лимит количества сделок.
        :param start_time: Начало интервала.
        :param end_time: Конец интервала.
        """

    @abstractmethod
    def get_transactions(
        self,
        account_id: str,
        limit: int,
        start_time: datetime,
        end_time: datetime,
    ) -> TransactionsResponse:
        """
        Получение списка транзакций.

        :param account_id: Идентификатор аккаунта.
        :param limit: Лимит количества транзакций.
        :param start_time: Начало интервала.
        :param end_time: Конец интервала.
        """

    @abstractmethod
    def get_exchanges(self) -> ExchangesResponse:
        """Получение списка доступных бирж, названия и mic коды."""

    @abstractmethod
    def get_assets(self) -> AssetsResponse:
        """Получение списка доступных инструментов, их описание."""

    @abstractmethod
    def get_asset_params(
        self, symbol: str, account_id: str
    ) -> GetAssetParamsResponse:
        """
        Получение торговых параметров по инструменту.

        :param symbol: Символ инструмента.
        :param account_id: ID аккаунта для которого
          будут подбираться торговые параметры.
        """

    @abstractmethod
    def get_options_chain(
        self, underlying_symbol: str
    ) -> OptionsChainResponse:
        """
        Получение цепочки опционов для базового актива.

        :param underlying_symbol: Символ базового актива опциона.
        """

    @abstractmethod
    def get_schedule(self, symbol: str) -> ScheduleResponse:
        """
        Получение расписания торгов для инструмента.

        :param symbol: Символ инструмента.
        """

    @abstractmethod
    def place_order(
        self,
        account_id: str,
        symbol: str,
        quantity: Decimal,
        side: Side.ValueType,
        type: OrderType.ValueType,
        time_in_force: TimeInForce.ValueType,
        limit_price: Decimal | None,
        stop_price: Decimal | None,
        stop_condition: StopCondition.ValueType | None,
        legs: Iterable[Leg] | None,
        client_order_id: str | None,
    ) -> OrderState:
        """
        Выставление биржевой заявки.

        :param account_id: Идентификатор аккаунта.
        :param symbol: Символ инструмента.
        :param quantity: Количество в шт.
        :param side: Сторона (long или short).
        :param type: Тип заявки.
        :param time_in_force: Срок действия заявки.
        :param limit_price: Необходимо для лимитной и стоп лимитной заявки.
        :param stop_price: 	Необходимо для стоп рыночной и стоп лимитной
          заявки.
        :param stop_condition: Необходимо для стоп рыночной и стоп
          лимитной заявки.
        :param legs: Необходимо для мульти лег заявки.
        :param client_order_id: Уникальный идентификатор заявки. Автоматически
          генерируется, если не отправлен. (максимум 20 символов).
        """

    @abstractmethod
    def cancel_order(self, account_id: str, order_id: str) -> OrderState:
        """
        Отмена биржевой заявки.

        :param account_id: Идентификатор аккаунта.
        :param order_id: Идентификатор заявки.
        """

    @abstractmethod
    def get_orders(self, account_id: str) -> OrdersResponse:
        """
        Получение списка активных заявок для аккаунта.

        :param account_id: Идентификатор аккаунта.
        """

    @abstractmethod
    def get_order(self, account_id: str, order_id: str) -> OrderState:
        """
        Получение информации о конкретном ордере.

        :param account_id: Идентификатор аккаунта.
        :param order_id: Идентификатор заявки.
        """

    @abstractmethod
    def get_bars(
        self,
        symbol: str,
        timeframe: TimeFrame.ValueType,
        start_time: datetime,
        end_time: datetime,
    ) -> BarsResponse:
        """
        Получение исторических данных по инструменту (агрегированные свечи).

        :param symbol: Символ инструмента.
        :param timeframe: Необходимый таймфрейм.
        :param start_time: Начало интервала.
        :param end_time: Конец интервала.
        """

    @abstractmethod
    def get_last_quote(self, symbol: str) -> QuoteResponse:
        """
        Получение последней котировки по инструменту.

        :param symbol: Символ инструмента.
        """

    @abstractmethod
    def get_order_book(self, symbol: str) -> OrderBookResponse:
        """
        Получение текущего стакана по инструменту.

        :param symbol: Символ инструмента.
        """

    @abstractmethod
    def get_latest_trades(self, symbol: str) -> LatestTradesResponse:
        """
        Получение списка последних сделок по инструменту.

        :param symbol: Символ инструмента.
        """

    @abstractmethod
    def get_clock(self) -> ClockResponse:
        """Запрос получения времени на сервере."""

    @abstractmethod
    def get_asset(self, symbol: str, account_id: str) -> GetAssetResponse:
        """
        Запрос информации по конкретному инструменту.

        :param symbol: Символ инструмента.
        :param account_id: ID аккаунта для которого
          будет подбираться информация по инструменту.
        """

    @abstractmethod
    def subscribe_quote(self, *symbol: str) -> None:
        """
        Подписка на котировки по инструменту.

        :param symbol: Символ инструмента.
        """

    @abstractmethod
    def unsubscribe_quote(self, *symbol: str) -> None:
        """
        Отмена подписки на котировки по инструменту.

        Важно:
        - Необходимо указывать те же symbols, что и при подписке.

        :param symbol: Символ инструмента.
        """

    @abstractmethod
    def subscribe_order_book(self, symbol: str) -> None:
        """
        Подписка на стакан по инструменту.

        :param symbol: Символ инструмента.
        """

    @abstractmethod
    def unsubscribe_order_book(self, symbol: str) -> None:
        """
        Отмена подписки на стакан по инструменту.

        :param symbol: Символ инструмента.
        """

    @abstractmethod
    def subscribe_latest_trades(self, symbol: str) -> None:
        """
        Подписка на сделки по инструменту.

        :param symbol: Символ инструмента.
        """

    @abstractmethod
    def unsubscribe_latest_trades(self, symbol: str) -> None:
        """
        Отмена подписки на сделки по инструменту.

        :param symbol: Символ инструмента.
        """

    @abstractmethod
    def subscribe_bars(
        self, symbol: str, timeframe: TimeFrame.ValueType
    ) -> None:
        """
        Подписка на бары.

        :param symbol: Символ инструмента.
        :param timeframe: Необходимый таймфрейм.
        """

    @abstractmethod
    def unsubscribe_bars(
        self, symbol: str, timeframe: TimeFrame.ValueType
    ) -> None:
        """
        Отмена подписки на бары.

        :param symbol: Символ инструмента.
        :param timeframe: Необходимый таймфрейм.
        """

    @abstractmethod
    def subscribe_order_trade(
        self, account_id: str, data_type: OrderTradeRequest.DataType.ValueType
    ) -> None:
        """
        Подписка на собственные заявки и сделки.

        :param account_id: Идентификатор аккаунта.
        :param data_type: Подписка только на заявки/ордера или на все сразу.
        """

    @abstractmethod
    def unsubscribe_order_trade(
        self, account_id: str, data_type: OrderTradeRequest.DataType.ValueType
    ) -> None:
        """
        Отмена подписки на собственные заявки и сделки.

        :param account_id: Идентификатор аккаунта.
        :param data_type: Подписка только на заявки/ордера или на все сразу.
        """

    def default_handler(self, event) -> None:
        """Обработчик по умолчанию."""


class AsyncClientInterface(SyncClientInterface, ABC):
    """Интерфейс асинхронного клиента."""

    @abstractmethod
    async def __aenter__(self) -> "AsyncClientInterface":
        """Вход в асинхронный менеджер контекста."""

    @abstractmethod
    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Выход из асинхронного менеджера контекста."""

    def __enter__(self):
        raise NotImplementedError()

    def __exit__(self, exc_type, exc_val, exc_tb):
        raise NotImplementedError()

    @property
    @abstractmethod
    def channel(self) -> AsyncChannel: ...

    @property
    @abstractmethod
    def on_quote(self) -> Callable[[SubscribeQuoteResponse], Coroutine]:
        """Обработчик подписки на котировки."""

    @on_quote.setter
    @abstractmethod
    def on_quote(
        self, value: Callable[[SubscribeQuoteResponse], Coroutine]
    ) -> None:
        """Обработчик подписки на котировки."""

    @property
    @abstractmethod
    def on_order_book(
        self,
    ) -> Callable[[SubscribeOrderBookResponse], Coroutine]:
        """Обработчик подписки на стакан."""

    @on_order_book.setter
    @abstractmethod
    def on_order_book(
        self, value: Callable[[SubscribeOrderBookResponse], Coroutine]
    ) -> None:
        """Обработчик подписки на стакан."""

    @property
    @abstractmethod
    def on_latest_trade(
        self,
    ) -> Callable[[SubscribeLatestTradesResponse], Coroutine]:
        """Обработчик подписки на сделки."""

    @on_latest_trade.setter
    @abstractmethod
    def on_latest_trade(
        self, value: Callable[[SubscribeLatestTradesResponse], Coroutine]
    ) -> None:
        """Обработчик подписки на сделки."""

    @property
    @abstractmethod
    def on_bar(self) -> Callable[[SubscribeBarsResponse], Coroutine]:
        """Обработчик подписки на бары."""

    @on_bar.setter
    @abstractmethod
    def on_bar(
        self, value: Callable[[SubscribeBarsResponse], Coroutine]
    ) -> None:
        """Обработчик подписки на бары."""

    @property
    @abstractmethod
    def on_order_trade(self) -> Callable[[OrderTradeResponse], Coroutine]:
        """Обработчик подписки на собственные заявки и сделки."""

    @on_order_trade.setter
    @abstractmethod
    def on_order_trade(
        self, value: Callable[[OrderTradeResponse], Coroutine]
    ) -> None:
        """Обработчик подписки на собственные заявки и сделки."""

    @abstractmethod
    async def start(self) -> None: ...

    @abstractmethod
    async def stop(self) -> None: ...

    @abstractmethod
    async def get_account_info(self, account_id) -> GetAccountResponse: ...

    @abstractmethod
    async def get_trades(
        self,
        account_id,
        limit,
        start_time,
        end_time,
    ) -> TradesResponse: ...

    @abstractmethod
    async def get_transactions(
        self,
        account_id,
        limit,
        start_time,
        end_time,
    ) -> TransactionsResponse: ...

    @abstractmethod
    async def get_exchanges(self) -> ExchangesResponse: ...

    @abstractmethod
    async def get_assets(self) -> AssetsResponse: ...

    @abstractmethod
    async def get_asset_params(
        self, symbol, account_id
    ) -> GetAssetParamsResponse: ...

    @abstractmethod
    async def get_options_chain(
        self, underlying_symbol
    ) -> OptionsChainResponse: ...

    @abstractmethod
    async def get_schedule(self, symbol) -> ScheduleResponse: ...

    @abstractmethod
    async def place_order(
        self,
        account_id,
        symbol,
        quantity,
        side,
        type,
        time_in_force,
        limit_price,
        stop_price,
        stop_condition,
        legs,
        client_order_id,
    ) -> OrderState: ...

    @abstractmethod
    async def cancel_order(self, account_id, order_id) -> OrderState: ...

    @abstractmethod
    async def get_orders(self, account_id) -> OrdersResponse: ...

    @abstractmethod
    async def get_order(self, account_id, order_id) -> OrderState: ...

    @abstractmethod
    async def get_bars(
        self, symbol, timeframe, start_time, end_time
    ) -> BarsResponse: ...

    @abstractmethod
    async def get_last_quote(self, symbol) -> QuoteResponse: ...

    @abstractmethod
    async def get_order_book(self, symbol) -> OrderBookResponse: ...

    @abstractmethod
    async def get_latest_trades(self, symbol) -> LatestTradesResponse: ...

    @abstractmethod
    async def get_clock(self) -> ClockResponse: ...

    @abstractmethod
    async def get_asset(
        self, symbol: str, account_id: str
    ) -> GetAssetResponse: ...

    @abstractmethod
    async def subscribe_quote(self, *symbol) -> None: ...

    @abstractmethod
    async def unsubscribe_quote(self, *symbol) -> None: ...

    @abstractmethod
    async def subscribe_order_book(self, symbol) -> None: ...

    @abstractmethod
    async def unsubscribe_order_book(self, symbol) -> None: ...

    @abstractmethod
    async def subscribe_latest_trades(self, symbol) -> None: ...

    @abstractmethod
    async def unsubscribe_latest_trades(self, symbol) -> None: ...

    @abstractmethod
    async def subscribe_bars(self, symbol, timeframe) -> None: ...

    @abstractmethod
    def unsubscribe_bars(self, symbol, timeframe) -> None: ...

    @abstractmethod
    async def subscribe_order_trade(self, account_id, data_type) -> None: ...

    @abstractmethod
    async def unsubscribe_order_trade(self, account_id, data_type) -> None: ...

    async def default_handler(self, event) -> None: ...
