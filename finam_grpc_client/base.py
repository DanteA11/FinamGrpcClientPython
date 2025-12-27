from abc import ABC, abstractmethod
from functools import partial
from typing import Any

from grpc import Channel, UnaryStreamMultiCallable, UnaryUnaryMultiCallable
from grpc.aio import Channel as AsyncChannel
from grpc.aio import UnaryStreamMultiCallable as AsyncUnaryStreamMultiCallable
from grpc.aio import UnaryUnaryMultiCallable as AsyncUnaryUnaryMultiCallable

from .proto.grpc.tradeapi.v1.accounts.accounts_service_pb2_grpc import (
    AccountsServiceStub,
)
from .proto.grpc.tradeapi.v1.assets.assets_service_pb2_grpc import (
    AssetsServiceStub,
)
from .proto.grpc.tradeapi.v1.auth.auth_service_pb2_grpc import AuthServiceStub
from .proto.grpc.tradeapi.v1.marketdata.marketdata_service_pb2_grpc import (
    MarketDataServiceStub,
)
from .proto.grpc.tradeapi.v1.metrics.usage_metrics_service_pb2_grpc import (
    UsageMetricsServiceStub,
)
from .proto.grpc.tradeapi.v1.orders.orders_service_pb2_grpc import (
    OrdersServiceStub,
)


class AbstractFinamClient[
    C: Channel | AsyncChannel,
    UU: UnaryUnaryMultiCallable | AsyncUnaryUnaryMultiCallable,
    US: UnaryStreamMultiCallable | AsyncUnaryStreamMultiCallable,
](ABC):

    def __init__(self, secret: str, url: str) -> None:
        self.__secret = secret
        self.__url = url
        self.__channel: C | None = None
        self.session_token: str | None = None
        self._auth_stub: AuthServiceStub | None = None
        self._accounts_stub: AccountsServiceStub | None = None
        self._assets_stub: AssetsServiceStub | None = None
        self._orders_stub: OrdersServiceStub | None = None
        self._market_data_stub: MarketDataServiceStub | None = None
        self._metrics_stub: UsageMetricsServiceStub | None = None

    @property
    @abstractmethod
    def metadata(self) -> Any: ...

    @abstractmethod
    def _create_channel(self) -> C: ...

    def start(self) -> None:
        channel = self._create_channel()
        self._auth_stub = AuthServiceStub(channel)
        self._accounts_stub = AccountsServiceStub(channel)
        self._assets_stub = AssetsServiceStub(channel)
        self._orders_stub = OrdersServiceStub(channel)
        self._market_data_stub = MarketDataServiceStub(channel)
        self._metrics_stub = UsageMetricsServiceStub(channel)
        self.__channel = channel

    def stop(self):
        channel = self.__channel
        self.__channel = None
        self._auth_stub = None
        self._accounts_stub = None
        self._assets_stub = None
        self._orders_stub = None
        self._market_data_stub = None
        self._metrics_stub = None
        self.session_token = None
        if channel:
            return None
        return channel.close()

    @property
    def stopped(self) -> bool:
        return self.__channel is None

    @property
    def started(self) -> bool:
        return not self.stopped

    @property
    def url(self) -> str:
        return self.__url

    @property
    def secret(self) -> str:
        return self.__secret

    ######################### Auth #########################
    @property
    def auth(self) -> UU:
        return self._auth_stub.Auth

    @property
    def token_details(self) -> UU:
        return self._auth_stub.TokenDetails

    @property
    def subscribe_jwt_renewal(self) -> US:
        return self._auth_stub.SubscribeJwtRenewal

    ####################### Accounts #######################
    @property
    def get_account(self) -> partial[UU]:
        return self._prepare_call(self._accounts_stub.GetAccount)

    @property
    def trades(self) -> partial[UU]:
        return self._prepare_call(self._accounts_stub.Trades)

    @property
    def transactions(self) -> partial[UU]:
        return self._prepare_call(self._accounts_stub.Transactions)

    ######################## Assets ########################
    @property
    def assets(self) -> partial[UU]:
        return self._prepare_call(self._assets_stub.Assets)

    @property
    def clock(self) -> partial[UU]:
        return self._prepare_call(self._assets_stub.Clock)

    @property
    def exchanges(self) -> partial[UU]:
        return self._prepare_call(self._assets_stub.Exchanges)

    @property
    def get_asset(self) -> partial[UU]:
        return self._prepare_call(self._assets_stub.GetAsset)

    @property
    def get_asset_params(self) -> partial[UU]:
        return self._prepare_call(self._assets_stub.GetAssetParams)

    @property
    def options_chain(self) -> partial[UU]:
        return self._prepare_call(self._assets_stub.OptionsChain)

    @property
    def schedule(self) -> partial[UU]:
        return self._prepare_call(self._assets_stub.Schedule)

    ######################## Orders ########################
    @property
    def cancel_order(self) -> partial[UU]:
        return self._prepare_call(self._orders_stub.CancelOrder)

    @property
    def get_order(self) -> partial[UU]:
        return self._prepare_call(self._orders_stub.GetOrder)

    @property
    def get_orders(self) -> partial[UU]:
        return self._prepare_call(self._orders_stub.GetOrders)

    @property
    def place_order(self) -> partial[UU]:
        return self._prepare_call(self._orders_stub.PlaceOrder)

    @property
    def subscribe_orders(self) -> partial[US]:
        return self._prepare_call(self._orders_stub.SubscribeOrders)

    @property
    def subscribe_trades(self) -> partial[US]:
        return self._prepare_call(self._orders_stub.SubscribeTrades)

    ###################### Market Data ######################

    @property
    def bars(self) -> partial[UU]:
        return self._prepare_call(self._market_data_stub.Bars)

    @property
    def last_quote(self) -> partial[UU]:
        return self._prepare_call(self._market_data_stub.LastQuote)

    @property
    def latest_trades(self) -> partial[UU]:
        return self._prepare_call(self._market_data_stub.LatestTrades)

    @property
    def order_book(self) -> partial[UU]:
        return self._prepare_call(self._market_data_stub.OrderBook)

    @property
    def subscribe_bars(self) -> partial[US]:
        return self._prepare_call(self._market_data_stub.SubscribeBars)

    @property
    def subscribe_latest_trades(self) -> partial[US]:
        return self._prepare_call(self._market_data_stub.SubscribeLatestTrades)

    @property
    def subscribe_order_book(self) -> partial[US]:
        return self._prepare_call(self._market_data_stub.SubscribeOrderBook)

    @property
    def subscribe_quote(self) -> partial[US]:
        return self._prepare_call(self._market_data_stub.SubscribeQuote)

    ######################## Metrics ########################
    @property
    def get_usage_metrics(self) -> partial[UU]:
        return self._prepare_call(self._metrics_stub.GetUsageMetrics)

    def _prepare_call(self, method):
        return partial(method, metadata=self.metadata)
