import logging

from finam_grpc_client.grpc.tradeapi.v1.accounts.accounts_service_pb2 import (
    GetAccountRequest,
    TradesRequest,
    TransactionsRequest,
)
from finam_grpc_client.grpc.tradeapi.v1.assets.assets_service_pb2 import (
    AssetsRequest,
    ClockRequest,
    ExchangesRequest,
    GetAssetParamsRequest,
    GetAssetRequest,
    OptionsChainRequest,
    ScheduleRequest,
)
from finam_grpc_client.grpc.tradeapi.v1.marketdata.marketdata_service_pb2 import (
    BarsRequest,
    LatestTradesRequest,
    OrderBookRequest,
    QuoteRequest,
    SubscribeBarsRequest,
    SubscribeLatestTradesRequest,
    SubscribeOrderBookRequest,
    SubscribeQuoteRequest,
)
from finam_grpc_client.grpc.tradeapi.v1.orders.orders_service_pb2 import (
    CancelOrderRequest,
    GetOrderRequest,
    Order,
    OrdersRequest,
    OrderTradeRequest,
)

from .base import BaseSyncClient


class FinamSyncClient(BaseSyncClient):
    """
    Класс для синхронного подключения к Api.

    Перед началом работы необходимо вызвать метод start().
    После окончания использования нужно вызвать метод stop().

    Либо можно воспользоваться менеджером контекста.

    :param token: Токен доступа к Api.
    :param handlers_thread_amount: Количество потоков для запуска получения событий.
    :param workers_thread_amount: Количество потоков для запуска обработчиков.
    """

    logger = logging.getLogger("finam_grpc_client.FinamSyncClient")

    def __init__(
        self, token: str, handlers_thread_amount=4, workers_thread_amount=6
    ):
        super().__init__(
            "api.finam.ru:443",
            token,
            handlers_thread_amount=handlers_thread_amount,
            workers_thread_amount=workers_thread_amount,
        )

    def get_account_info(self, account_id):
        self.logger.info(
            "Запрос информации по аккаунту: account_id=%s", account_id
        )
        response = self._execute_request(
            self._accounts.GetAccount,
            message=GetAccountRequest(account_id=account_id),
        )
        self.logger.debug(
            "Получена информация по аккаунту: account_id=%s [\n%s\n]",
            account_id,
            response,
        )
        return response

    def get_trades(
        self,
        account_id,
        limit,
        start_time,
        end_time,
    ):
        self.logger.info(
            "Запрос торговой истории: account_id=%s, limit=%s, start_time=%s, end_time=%s",
            account_id,
            limit,
            start_time,
            end_time,
        )
        response = self.__get_transactions_trades(
            account_id,
            limit,
            start_time,
            end_time,
            self._accounts.Trades,
            TradesRequest,
        )
        self.logger.debug(
            "Получена торговая история по аккаунту: account_id=%s [\n%s\n]",
            account_id,
            response,
        )
        return response

    def get_transactions(
        self,
        account_id,
        limit,
        start_time,
        end_time,
    ):
        self.logger.info(
            "Запрос истории транзакций: account_id=%s, limit=%s, start_time=%s, end_time=%s",
            account_id,
            limit,
            start_time,
            end_time,
        )
        response = self.__get_transactions_trades(
            account_id,
            limit,
            start_time,
            end_time,
            self._accounts.Transactions,
            TransactionsRequest,
        )
        self.logger.debug(
            "Получена история транзакций по аккаунту: account_id=%s [\n%s\n]",
            account_id,
            response,
        )
        return response

    def get_exchanges(self):
        self.logger.info("Запрос списка доступных бирж")
        response = self._execute_request(
            self._assets.Exchanges, ExchangesRequest()
        )
        self.logger.debug("Получен список доступных бирж: [\n%s\n]", response)
        return response

    def get_assets(self):
        self.logger.info("Запрос списка доступных инструментов")
        response = self._execute_request(self._assets.Assets, AssetsRequest())
        self.logger.debug(
            "Получен список доступных инструментов: [\n%s\n]", response
        )
        return response

    def get_asset_params(self, symbol, account_id):
        self.logger.info(
            "Запрос торговых параметров по инструменту: symbol=%s, account_id=%s",
            symbol,
            account_id,
        )
        response = self._execute_request(
            self._assets.GetAssetParams,
            message=GetAssetParamsRequest(
                symbol=symbol, account_id=account_id
            ),
        )
        self.logger.debug(
            "Получены торговые параметры по инструменту: symbol=%s, account_id=%s: [\n%s\n]",
            symbol,
            account_id,
            response,
        )
        return response

    def get_options_chain(self, underlying_symbol):
        self.logger.info("Запрос цепочки опционов для %s", underlying_symbol)
        response = self._execute_request(
            self._assets.OptionsChain,
            message=OptionsChainRequest(underlying_symbol=underlying_symbol),
        )
        self.logger.debug(
            "Получена цепочка опционов для %s: [\n%s\n]",
            underlying_symbol,
            response,
        )
        return response

    def get_schedule(self, symbol):
        self.logger.info("Запрос расписания торгов для %s", symbol)
        response = self._execute_request(
            self._assets.Schedule, message=ScheduleRequest(symbol=symbol)
        )
        self.logger.debug(
            "Получено расписание для %s: [\n%s\n]",
            symbol,
            response,
        )
        return response

    def place_order(
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
    ):
        self.logger.info(
            "Выставление заявки: account_id=%s, symbol=%s, quantity=%s, side=%s, type=%s, time_in_force=%s, limit_price=%s, stop_price=%s, stop_condition=%s, legs=%s, client_order_id=%s",
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
        )
        response = self._execute_request(
            self._orders.PlaceOrder,
            message=Order(
                account_id=account_id,
                symbol=symbol,
                quantity=quantity,
                side=side,
                type=type,
                time_in_force=time_in_force,
                limit_price=limit_price,
                stop_price=stop_price,
                stop_condition=stop_condition,
                legs=legs,
                client_order_id=client_order_id,
            ),
        )
        self.logger.debug(
            "Получен ответ на запрос выставления заявки: account_id=%s, symbol=%s, quantity=%s, side=%s, type=%s, time_in_force=%s, limit_price=%s, stop_price=%s, stop_condition=%s, legs=%s, client_order_id=%s: [\n%s\n]",
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
            response,
        )
        return response

    def cancel_order(self, account_id, order_id):
        self.logger.info(
            "Отмена заявки: account_id=%s, order_id=%s", account_id, order_id
        )
        response = self._execute_request(
            self._orders.CancelOrder,
            message=CancelOrderRequest(
                account_id=account_id, order_id=order_id
            ),
        )
        self.logger.debug(
            "Получен ответ на отмену заявки: account_id=%s, order_id=%s: [\n%s\n]",
            account_id,
            order_id,
            response,
        )
        return response

    def get_orders(self, account_id):
        self.logger.info(
            "Запрос списка активных заявок: account_id=%s", account_id
        )
        response = self._execute_request(
            self._orders.GetOrders,
            message=OrdersRequest(account_id=account_id),
        )
        self.logger.debug(
            "Получен ответ на запрос списка активных заявок account_id=%s: [\n%s\n]",
            account_id,
            response,
        )
        return response

    def get_order(self, account_id, order_id):
        self.logger.info(
            "Запрос информации об ордере: account_id=%s, order_id=%s",
            account_id,
            order_id,
        )
        response = self._execute_request(
            self._orders.GetOrder,
            message=GetOrderRequest(account_id=account_id, order_id=order_id),
        )
        self.logger.debug(
            "Получен ответ на запрос информации об ордере account_id=%s, order_id=%s: [\n%s\n]",
            account_id,
            order_id,
            response,
        )
        return response

    def get_bars(
        self,
        symbol,
        timeframe,
        start_time,
        end_time,
    ):
        self.logger.info(
            "Запрос баров: symbol=%s, timeframe=%s, start_time=%s, end_time=%s",
            symbol,
            timeframe,
            start_time,
            end_time,
        )
        response = self._execute_request(
            self._market_data.Bars,
            message=BarsRequest(
                symbol=symbol,
                timeframe=timeframe,
                interval=self._create_interval(
                    start_time=start_time, end_time=end_time
                ),
            ),
        )
        self.logger.debug(
            "Получен ответ на запрос баров symbol=%s, timeframe=%s, start_time=%s, end_time=%s: [\n%s\n]",
            symbol,
            timeframe,
            start_time,
            end_time,
            response,
        )
        return response

    def get_last_quote(self, symbol):
        self.logger.info("Запрос последней котировки: symbol=%s", symbol)
        response = self._execute_request(
            self._market_data.LastQuote, message=QuoteRequest(symbol=symbol)
        )
        self.logger.debug(
            "Получен ответ на запрос последней котировки symbol=%s: [\n%s\n]",
            symbol,
            response,
        )
        return response

    def get_order_book(self, symbol):
        self.logger.info("Запрос текущего стакана: symbol=%s", symbol)
        response = self._execute_request(
            self._market_data.OrderBook,
            message=OrderBookRequest(symbol=symbol),
        )
        self.logger.debug(
            "Получен ответ на запрос текущего стакана symbol=%s: [\n%s\n]",
            symbol,
            response,
        )
        return response

    def get_latest_trades(self, symbol):
        self.logger.info("Запрос списка последних сделок: symbol=%s", symbol)
        response = self._execute_request(
            self._market_data.LatestTrades,
            message=LatestTradesRequest(symbol=symbol),
        )
        self.logger.debug(
            "Получен ответ на запрос списка последних сделок symbol=%s: [\n%s\n]",
            symbol,
            response,
        )
        return response

    def get_clock(self):
        self.logger.info("Запрос времени сервера")
        response = self._execute_request(
            self._assets.Clock, message=ClockRequest()
        )
        self.logger.debug("Получено время сервера: [\n%s\n]", response)
        return response

    def get_asset(self, symbol, account_id):
        self.logger.info(
            "Запрос информации об инструменте: symbol=%s, account_id=%s",
            symbol,
            account_id,
        )
        response = self._execute_request(
            self._assets.GetAsset,
            message=GetAssetRequest(symbol=symbol, account_id=account_id),
        )
        self.logger.debug(
            "Получен ответ на запрос информации по инструменту symbol=%s, account_id=%s: [\n%s\n]",
            symbol,
            account_id,
            response,
        )
        return response

    def subscribe_quote(self, *symbol):
        self.logger.info("Подписка на котировки: symbols=%s", symbol)
        self._subscribe_unary_stream(
            SubscribeQuoteRequest(symbols=symbol),
            self._market_data.SubscribeQuote,
        )

    def unsubscribe_quote(self, *symbol):
        self.logger.info("Отмена подписки на котировки: symbols=%s", symbol)
        self._unsubscribe_unary_stream(SubscribeQuoteRequest(symbols=symbol))

    def subscribe_order_book(self, symbol):
        self.logger.info("Подписка на стакан: symbol=%s", symbol)
        self._subscribe_unary_stream(
            SubscribeOrderBookRequest(symbol=symbol),
            self._market_data.SubscribeOrderBook,
        )

    def unsubscribe_order_book(self, symbol):
        self.logger.info("Отмена подписки на стакан: symbol=%s", symbol)
        self._unsubscribe_unary_stream(
            SubscribeOrderBookRequest(symbol=symbol)
        )

    def subscribe_latest_trades(self, symbol):
        self.logger.info("Подписка на сделки: symbol=%s", symbol)
        self._subscribe_unary_stream(
            SubscribeLatestTradesRequest(symbol=symbol),
            self._market_data.SubscribeLatestTrades,
        )

    def unsubscribe_latest_trades(self, symbol):
        self.logger.info("Отмена подписки на сделки: symbol=%s", symbol)
        self._unsubscribe_unary_stream(
            SubscribeLatestTradesRequest(symbol=symbol)
        )

    def subscribe_bars(self, symbol, timeframe):
        self.logger.info(
            "Подписка на бары: symbol=%s, timeframe=%s", symbol, timeframe
        )
        self._subscribe_unary_stream(
            SubscribeBarsRequest(symbol=symbol, timeframe=timeframe),
            self._market_data.SubscribeBars,
        )

    def unsubscribe_bars(self, symbol, timeframe):
        self.logger.info(
            "Отмена подписки на бары: symbol=%s, timeframe=%s",
            symbol,
            timeframe,
        )
        self._unsubscribe_unary_stream(
            SubscribeBarsRequest(symbol=symbol, timeframe=timeframe)
        )

    # def subscribe_order_trade(self, account_id, data_type):
    #     self.logger.info(
    #         "Подписка на собственные заявки и сделки: account_id=%s, data_type=%s",
    #         account_id,
    #         data_type,
    #     )
    #     self._execute_order_trade_subscribe_request(
    #         OrderTradeRequest(
    #             action=OrderTradeRequest.Action.ACTION_SUBSCRIBE,
    #             data_type=data_type,
    #             account_id=account_id,
    #         )
    #     )
    #
    # def unsubscribe_order_trade(self, account_id, data_type):
    #     self.logger.info(
    #         "Отмена подписки на собственные заявки и сделки: account_id=%s, data_type=%s",
    #         account_id,
    #         data_type,
    #     )
    #     self._execute_order_trade_subscribe_request(
    #         OrderTradeRequest(
    #             action=OrderTradeRequest.Action.ACTION_UNSUBSCRIBE,
    #             data_type=data_type,
    #             account_id=account_id,
    #         )
    #     )

    def __get_transactions_trades(
        self, account_id, limit, start_time, end_time, method, request_type
    ):
        return self._execute_request(
            method,
            message=request_type(
                account_id=account_id,
                limit=limit,
                interval=self._create_interval(
                    start_time=start_time,
                    end_time=end_time,
                ),
            ),
        )
