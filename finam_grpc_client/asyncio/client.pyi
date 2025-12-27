from typing import Any, AsyncIterator, Callable, Self

from grpc import StatusCode
from grpc.aio import Metadata

from finam_grpc_client.proto.grpc.tradeapi.v1.accounts.accounts_service_pb2 import (
    GetAccountRequest,
    GetAccountResponse,
    TradesRequest,
    TradesResponse,
    TransactionsRequest,
    TransactionsResponse,
)
from finam_grpc_client.proto.grpc.tradeapi.v1.assets.assets_service_pb2 import (
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
from finam_grpc_client.proto.grpc.tradeapi.v1.auth.auth_service_pb2 import (
    AuthRequest,
    AuthResponse,
    SubscribeJwtRenewalRequest,
    SubscribeJwtRenewalResponse,
    TokenDetailsRequest,
    TokenDetailsResponse,
)
from finam_grpc_client.proto.grpc.tradeapi.v1.marketdata.marketdata_service_pb2 import (
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
from finam_grpc_client.proto.grpc.tradeapi.v1.metrics.usage_metrics_service_pb2 import (
    GetUsageMetricsRequest,
    GetUsageMetricsResponse,
)
from finam_grpc_client.proto.grpc.tradeapi.v1.orders.orders_service_pb2 import (
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

class UnaryStreamCall[R]:
    """
    Интерфейс для grpc.aio.UnaryStreamCall.

    Используется, так как нельзя импортировать оригинал.
    """

    def __aiter__(self) -> AsyncIterator[R]: ...
    async def read(self) -> object | R: ...
    async def initial_metadata(self) -> Metadata: ...
    async def trailing_metadata(self) -> Metadata: ...
    async def code(self) -> StatusCode: ...
    async def details(self) -> str: ...
    async def wait_for_connection(self) -> None: ...
    def cancelled(self) -> bool: ...
    def done(self) -> bool: ...
    def time_remaining(self) -> float | None: ...
    def cancel(self) -> bool: ...
    def add_done_callback(self, callback: Callable[[Any], None]) -> None: ...

class FinamClient:
    def __init__(self, secret: str, *, url: str = "api.finam.ru:443"):
        """
        Клиент для асинхронного взаимодействия с Api Finam.

        https://tradeapi.finam.ru/docs/guides/grpc

        Автоматически обновляет токен сессии.

        Перед использованием необходимо вызвать метод start(),
        после использования - stop().

        Также можно воспользоваться асинхронным контекстным менеджером.

        :param secret: Токен, полученный на сайте Finam (https://tradeapi.finam.ru/docs/tokens/).
        :param url: Адрес для подключения к API.
        """

    async def __aenter__(self) -> Self: ...
    async def __aexit__(self, exc_type, exc_val, exc_tb): ...
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

    async def start(self) -> None:
        """Создание нового канала и подключение сервисов."""

    async def stop(self) -> None:
        """Закрытие канала и отключение сервисов."""
    ######################### Auth #########################
    async def auth(self, request: AuthRequest) -> AuthResponse:
        """Получение JWT токена из API токена."""

    async def token_details(
        self, request: TokenDetailsRequest
    ) -> TokenDetailsResponse:
        """Получение информации о токене сессии."""

    def subscribe_jwt_renewal(
        self, request: SubscribeJwtRenewalRequest
    ) -> UnaryStreamCall[SubscribeJwtRenewalResponse]:
        """Подписка на обновление JWT токена. Стрим метод."""

    async def get_account(
        self, request: GetAccountRequest
    ) -> GetAccountResponse:
        """Получение информации по конкретному аккаунту."""

    async def trades(self, request: TradesRequest) -> TradesResponse:
        """Получение истории по сделкам аккаунта."""

    async def transactions(
        self, request: TransactionsRequest
    ) -> TransactionsResponse:
        """Получение списка транзакций аккаунта."""
    ######################## Assets ########################
    async def assets(self, request: AssetsRequest) -> AssetsResponse:
        """Получение списка доступных инструментов, их описание."""

    async def clock(self, request: ClockRequest) -> ClockResponse:
        """Получение времени на сервере."""

    async def exchanges(self, request: ExchangesRequest) -> ExchangesResponse:
        """Получение списка доступных бирж, названия и mic коды."""

    async def get_asset(self, request: GetAssetRequest) -> GetAssetResponse:
        """Получение информации по конкретному инструменту."""

    async def get_asset_params(
        self, request: GetAssetParamsRequest
    ) -> GetAssetParamsResponse:
        """Получение торговых параметров по инструменту."""

    async def options_chain(
        self, request: OptionsChainRequest
    ) -> OptionsChainResponse:
        """Получение цепочки опционов для базового актива."""

    async def schedule(self, request: ScheduleRequest) -> ScheduleResponse:
        """Получение расписания торгов для инструмента."""
    ######################## Orders ########################
    async def cancel_order(self, request: CancelOrderRequest) -> OrderState:
        """Отмена биржевой заявки."""

    async def get_order(self, request: GetOrderRequest) -> OrderState:
        """Получение информации о конкретном ордере."""

    async def get_orders(self, request: OrdersRequest) -> OrdersResponse:
        """Получение списка заявок для аккаунта."""

    async def place_order(self, request: Order) -> OrderState:
        """Выставление биржевой заявки."""

    def subscribe_orders(
        self, request: SubscribeOrdersRequest
    ) -> UnaryStreamCall[SubscribeOrdersResponse]:
        """Подписка на собственные заявки. Стрим метод."""

    def subscribe_trades(
        self, request: SubscribeTradesRequest
    ) -> UnaryStreamCall[SubscribeTradesResponse]:
        """Подписка на собственные сделки. Стрим метод."""
    ###################### Market Data ######################
    async def bars(self, request: BarsRequest) -> BarsResponse:
        """Получение исторических данных по инструменту (агрегированные свечи)."""

    async def last_quote(self, request: QuoteRequest) -> QuoteResponse:
        """Получение последней котировки по инструменту."""

    async def latest_trades(
        self, request: LatestTradesRequest
    ) -> LatestTradesResponse:
        """Получение списка последних сделок по инструменту."""

    async def order_book(self, request: OrderBookRequest) -> OrderBookResponse:
        """Получение текущего стакана по инструменту."""

    def subscribe_bars(
        self, request: SubscribeBarsRequest
    ) -> UnaryStreamCall[SubscribeBarsResponse]:
        """Подписка на агрегированные свечи. Стрим метод."""

    def subscribe_latest_trades(
        self, request: SubscribeLatestTradesRequest
    ) -> UnaryStreamCall[SubscribeLatestTradesResponse]:
        """Подписка на сделки по инструменту. Стрим метод."""

    def subscribe_order_book(
        self, request: SubscribeOrderBookRequest
    ) -> UnaryStreamCall[SubscribeOrderBookResponse]:
        """Подписка на стакан по инструменту. Стрим метод."""

    def subscribe_quote(
        self, request: SubscribeQuoteRequest
    ) -> UnaryStreamCall[SubscribeQuoteResponse]:
        """Подписка на котировки по инструменту. Стрим метод."""
    ######################## Metrics ########################
    async def get_usage_metrics(
        self, request: GetUsageMetricsRequest
    ) -> GetUsageMetricsResponse:
        """Получение текущих метрик использования для пользователя."""
