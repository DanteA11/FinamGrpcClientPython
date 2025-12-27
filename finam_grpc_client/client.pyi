from typing import Callable, Iterator, Self

from grpc import StatusCode

from .proto.grpc.tradeapi.v1.accounts.accounts_service_pb2 import (
    GetAccountRequest,
    GetAccountResponse,
    TradesRequest,
    TradesResponse,
    TransactionsRequest,
    TransactionsResponse,
)
from .proto.grpc.tradeapi.v1.assets.assets_service_pb2 import (
    AssetsRequest,
    AssetsResponse,
    ClockRequest,
    ClockResponse,
    ExchangesRequest,
    ExchangesResponse,
    GetAssetParamsRequest,
    GetAssetParamsResponse,
    GetAssetRequest,
    GetAssetResponse,
    OptionsChainRequest,
    OptionsChainResponse,
    ScheduleRequest,
    ScheduleResponse,
)
from .proto.grpc.tradeapi.v1.auth.auth_service_pb2 import (
    AuthRequest,
    AuthResponse,
    SubscribeJwtRenewalRequest,
    SubscribeJwtRenewalResponse,
    TokenDetailsRequest,
    TokenDetailsResponse,
)
from .proto.grpc.tradeapi.v1.marketdata.marketdata_service_pb2 import (
    BarsRequest,
    BarsResponse,
    LatestTradesRequest,
    LatestTradesResponse,
    OrderBookRequest,
    OrderBookResponse,
    QuoteRequest,
    QuoteResponse,
    SubscribeBarsRequest,
    SubscribeBarsResponse,
    SubscribeLatestTradesRequest,
    SubscribeLatestTradesResponse,
    SubscribeOrderBookRequest,
    SubscribeOrderBookResponse,
    SubscribeQuoteRequest,
    SubscribeQuoteResponse,
)
from .proto.grpc.tradeapi.v1.metrics.usage_metrics_service_pb2 import (
    GetUsageMetricsRequest,
    GetUsageMetricsResponse,
)
from .proto.grpc.tradeapi.v1.orders.orders_service_pb2 import (
    CancelOrderRequest,
    GetOrderRequest,
    Order,
    OrdersRequest,
    OrdersResponse,
    OrderState,
    SubscribeOrdersRequest,
    SubscribeOrdersResponse,
    SubscribeTradesRequest,
    SubscribeTradesResponse,
)

class CallIterator[R]:
    """
    Интерфейс для grpc.CallIterator.

    Используется, так как нельзя импортировать оригинал.
    """

    def __iter__(self) -> Iterator[R]: ...
    def code(self) -> StatusCode: ...
    def details(self) -> str: ...
    def initial_metadata(self) -> tuple[tuple[str, str | bytes], ...]: ...
    def trailing_metadata(self) -> tuple[tuple[str, str | bytes], ...]: ...
    def add_callback(self, callback: Callable[[], None]) -> bool: ...
    def cancel(self): ...
    def is_active(self) -> bool: ...
    def time_remaining(self) -> float: ...

class FinamClient:
    def __init__(self, secret: str, *, url: str = "api.finam.ru:443"):
        """
        Клиент для взаимодействия с Api Finam.

        https://tradeapi.finam.ru/docs/guides/grpc

        Автоматически обновляет токен сессии.

        Перед использованием необходимо вызвать метод start(),
        после использования - stop().

        Также можно воспользоваться контекстным менеджером.

        :param secret: Токен, полученный на сайте Finam (https://tradeapi.finam.ru/docs/tokens/).
        :param url: Адрес для подключения к API.
        """

    def __enter__(self) -> Self: ...
    def __exit__(self, exc_type, exc_val, exc_tb): ...
    @property
    def stopped(self) -> bool:
        """Остановлен ли клиент."""

    @property
    def started(self) -> bool:
        """Запущен ли клиент."""

    @property
    def secret(self) -> str:
        """Токен пользователя."""

    @property
    def url(self) -> str:
        """Адрес для отправки запросов."""

    def start(self) -> None:
        """Создание нового канала и подключение сервисов."""

    def stop(self) -> None:
        """Закрытие канала и отключение сервисов."""
    ######################### Auth #########################
    def auth(self, request: AuthRequest) -> AuthResponse:
        """Получение JWT токена из API токена."""

    def token_details(
        self, request: TokenDetailsRequest
    ) -> TokenDetailsResponse:
        """Получение информации о токене сессии."""

    def subscribe_jwt_renewal(
        self, request: SubscribeJwtRenewalRequest
    ) -> CallIterator[SubscribeJwtRenewalResponse]:
        """Подписка на обновление JWT токена. Стрим метод."""

    def get_account(self, request: GetAccountRequest) -> GetAccountResponse:
        """Получение информации по конкретному аккаунту."""

    def trades(self, request: TradesRequest) -> TradesResponse:
        """Получение истории по сделкам аккаунта."""

    def transactions(
        self, request: TransactionsRequest
    ) -> TransactionsResponse:
        """Получение списка транзакций аккаунта."""
    ######################## Assets ########################
    def assets(self, request: AssetsRequest) -> AssetsResponse:
        """Получение списка доступных инструментов, их описание."""

    def clock(self, request: ClockRequest) -> ClockResponse:
        """Получение времени на сервере."""

    def exchanges(self, request: ExchangesRequest) -> ExchangesResponse:
        """Получение списка доступных бирж, названия и mic коды."""

    def get_asset(self, request: GetAssetRequest) -> GetAssetResponse:
        """Получение информации по конкретному инструменту."""

    def get_asset_params(
        self, request: GetAssetParamsRequest
    ) -> GetAssetParamsResponse:
        """Получение торговых параметров по инструменту."""

    def options_chain(
        self, request: OptionsChainRequest
    ) -> OptionsChainResponse:
        """Получение цепочки опционов для базового актива."""

    def schedule(self, request: ScheduleRequest) -> ScheduleResponse:
        """Получение расписания торгов для инструмента."""
    ######################## Orders ########################
    def cancel_order(self, request: CancelOrderRequest) -> OrderState:
        """Отмена биржевой заявки."""

    def get_order(self, request: GetOrderRequest) -> OrderState:
        """Получение информации о конкретном ордере."""

    def get_orders(self, request: OrdersRequest) -> OrdersResponse:
        """Получение списка заявок для аккаунта."""

    def place_order(self, request: Order) -> OrderState:
        """Выставление биржевой заявки."""

    def subscribe_orders(
        self, request: SubscribeOrdersRequest
    ) -> CallIterator[SubscribeOrdersResponse]:
        """Подписка на собственные заявки. Стрим метод."""

    def subscribe_trades(
        self, request: SubscribeTradesRequest
    ) -> CallIterator[SubscribeTradesResponse]:
        """Подписка на собственные сделки. Стрим метод."""
    ###################### Market Data ######################
    def bars(self, request: BarsRequest) -> BarsResponse:
        """Получение исторических данных по инструменту (агрегированные свечи)."""

    def last_quote(self, request: QuoteRequest) -> QuoteResponse:
        """Получение последней котировки по инструменту."""

    def latest_trades(
        self, request: LatestTradesRequest
    ) -> LatestTradesResponse:
        """Получение списка последних сделок по инструменту."""

    def order_book(self, request: OrderBookRequest) -> OrderBookResponse:
        """Получение текущего стакана по инструменту."""

    def subscribe_bars(
        self, request: SubscribeBarsRequest
    ) -> CallIterator[SubscribeBarsResponse]:
        """Подписка на агрегированные свечи. Стрим метод."""

    def subscribe_latest_trades(
        self, request: SubscribeLatestTradesRequest
    ) -> CallIterator[SubscribeLatestTradesResponse]:
        """Подписка на сделки по инструменту. Стрим метод."""

    def subscribe_order_book(
        self, request: SubscribeOrderBookRequest
    ) -> CallIterator[SubscribeOrderBookResponse]:
        """Подписка на стакан по инструменту. Стрим метод."""

    def subscribe_quote(
        self, request: SubscribeQuoteRequest
    ) -> CallIterator[SubscribeQuoteResponse]:
        """Подписка на котировки по инструменту. Стрим метод."""
    ######################## Metrics ########################
    def get_usage_metrics(
        self, request: GetUsageMetricsRequest
    ) -> GetUsageMetricsResponse:
        """Получение текущих метрик использования для пользователя."""
