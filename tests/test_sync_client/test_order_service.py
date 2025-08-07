import threading
import time
from random import choice

import pytest
from google.type.decimal_pb2 import Decimal
from grpc import RpcError

from finam_grpc_client.grpc.tradeapi.v1.assets.assets_service_pb2 import (
    Longable,
    Shortable,
)
from finam_grpc_client.grpc.tradeapi.v1.orders.orders_service_pb2 import (
    OrderStatus,
    OrderTradeResponse,
    OrderType,
    StopCondition,
    TimeInForce,
)
from finam_grpc_client.grpc.tradeapi.v1.side_pb2 import Side
from finam_grpc_client.types import DataType
from tests.type_checker import TypeChecker


class TestsOrdersService(TypeChecker):

    def test_place_cancel_order_buy_limit(self, sync_client, account_id):
        if not self.check_longable(sync_client, account_id):
            pytest.skip(f"По {self.symbol} лонг не разрешен")
        place = self.create_limit_order_buy(sync_client, account_id)
        self.check_order_state_type(place)
        assert place.status == OrderStatus.ORDER_STATUS_NEW
        cancel = sync_client.cancel_order(account_id, place.order_id)
        self.check_order_state_type(cancel)
        assert cancel.status == OrderStatus.ORDER_STATUS_CANCELED

    def test_place_cancel_order_sell_limit(self, sync_client, account_id):
        if not self.check_shortable(sync_client, account_id):
            pytest.skip(f"По {self.symbol} шорт не разрешен")
        limit_price = self.get_max_order_book_price(sync_client)
        if not limit_price:
            pytest.skip("Нет цены для выставления заявки")
        try:
            place = sync_client.place_order(
                account_id,
                self.symbol,
                quantity=Decimal(value="1"),
                side=Side.SIDE_SELL,
                type=OrderType.ORDER_TYPE_LIMIT,
                time_in_force=TimeInForce.TIME_IN_FORCE_DAY,
                limit_price=limit_price,
                stop_price=None,
                stop_condition=None,
                legs=None,
                client_order_id=None,
            )
        except RpcError as exc:
            if "Не хватает собственных бумаг" in exc.details():
                pytest.fail(
                    "Ошибка в GetAssetParamsResponse. Шорт не разрешен.",
                    pytrace=False,
                )

        self.check_order_state_type(place)
        assert place.status == OrderStatus.ORDER_STATUS_NEW
        cancel = sync_client.cancel_order(account_id, place.order_id)
        self.check_order_state_type(cancel)
        assert cancel.status == OrderStatus.ORDER_STATUS_CANCELED

    def test_place_cancel_order_buy_stop(self, sync_client, account_id):
        if not self.check_longable(sync_client, account_id):
            pytest.skip(f"По {self.symbol} лонг не разрешен")
        place = self.create_stop_order_by(sync_client, account_id)
        self.check_order_state_type(place)
        assert place.status == OrderStatus.ORDER_STATUS_WATCHING
        cancel = sync_client.cancel_order(account_id, place.order_id)
        self.check_order_state_type(cancel)
        assert cancel.status == OrderStatus.ORDER_STATUS_CANCELED

    def test_place_cancel_order_sell_stop(self, sync_client, account_id):
        if not self.check_shortable(sync_client, account_id):
            pytest.skip(f"По {self.symbol} шорт не разрешен")
        stop_price = self.get_min_order_book_price(sync_client)
        if not stop_price:
            pytest.skip("Нет цены для выставления заявки")
        place = sync_client.place_order(
            account_id,
            self.symbol,
            quantity=Decimal(value="1"),
            side=Side.SIDE_SELL,
            type=OrderType.ORDER_TYPE_STOP,
            time_in_force=TimeInForce.TIME_IN_FORCE_DAY,
            limit_price=None,
            stop_price=stop_price,
            stop_condition=StopCondition.STOP_CONDITION_LAST_DOWN,
            legs=None,
            client_order_id=None,
        )
        self.check_order_state_type(place)
        assert place.status == OrderStatus.ORDER_STATUS_WATCHING
        cancel = sync_client.cancel_order(account_id, place.order_id)
        self.check_order_state_type(cancel)
        assert cancel.status == OrderStatus.ORDER_STATUS_CANCELED

    def test_place_cancel_order_buy_stop_limit(self, sync_client, account_id):
        if not self.check_longable(sync_client, account_id):
            pytest.skip(f"По {self.symbol} лонг не разрешен")
        stop_price = limit_price = self.get_max_order_book_price(sync_client)
        if not stop_price:
            pytest.skip("Нет цены для выставления заявки")
        place = sync_client.place_order(
            account_id,
            self.symbol,
            quantity=Decimal(value="1"),
            side=Side.SIDE_BUY,
            type=OrderType.ORDER_TYPE_STOP,
            time_in_force=TimeInForce.TIME_IN_FORCE_DAY,
            limit_price=limit_price,
            stop_price=stop_price,
            stop_condition=StopCondition.STOP_CONDITION_LAST_UP,
            legs=None,
            client_order_id=None,
        )
        self.check_order_state_type(place)
        assert place.status == OrderStatus.ORDER_STATUS_WATCHING
        cancel = sync_client.cancel_order(account_id, place.order_id)
        self.check_order_state_type(cancel)
        assert cancel.status == OrderStatus.ORDER_STATUS_CANCELED

    def test_place_cancel_order_sell_stop_limit(self, sync_client, account_id):
        if not self.check_shortable(sync_client, account_id):
            pytest.skip(f"По {self.symbol} лонг не разрешен")
        stop_price = limit_price = self.get_min_order_book_price(sync_client)
        if not stop_price:
            pytest.skip("Нет цены для выставления заявки")
        place = sync_client.place_order(
            account_id,
            self.symbol,
            quantity=Decimal(value="1"),
            side=Side.SIDE_SELL,
            type=OrderType.ORDER_TYPE_STOP,
            time_in_force=TimeInForce.TIME_IN_FORCE_DAY,
            limit_price=limit_price,
            stop_price=stop_price,
            stop_condition=StopCondition.STOP_CONDITION_LAST_DOWN,
            legs=None,
            client_order_id=None,
        )
        self.check_order_state_type(place)
        assert place.status == OrderStatus.ORDER_STATUS_WATCHING
        cancel = sync_client.cancel_order(account_id, place.order_id)
        self.check_order_state_type(cancel)
        assert cancel.status == OrderStatus.ORDER_STATUS_CANCELED

    def test_get_orders(self, sync_client, account_id):
        res = sync_client.get_orders(account_id)
        for os in res.orders:
            self.check_order_state_type(os)
            assert os.order.account_id == account_id

    def test_get_orders_negative(self, sync_client):
        account_id = "111111"
        with pytest.raises(RpcError) as exc:
            sync_client.get_orders(account_id)
        assert (
            f"Account with id {account_id} is not found" in exc.value.details()
        )

    def test_get_order(self, sync_client, account_id):
        orders = sync_client.get_orders(account_id)
        if len(orders.orders) == 0:
            pytest.skip("Нет заявок")
        order_id = choice(orders.orders).order_id
        res = sync_client.get_order(account_id, order_id)
        self.check_order_state_type(res)
        assert res.order.account_id == account_id

    @classmethod
    def check_longable(cls, client, acc_id):
        asset_params = client.get_asset_params(cls.symbol, acc_id)
        return asset_params.longable.value == Longable.Status.AVAILABLE

    @classmethod
    def check_shortable(cls, client, acc_id):
        asset_params = client.get_asset_params(cls.symbol, acc_id)
        return asset_params.shortable.value == Shortable.Status.AVAILABLE

    @classmethod
    def get_min_order_book_price(cls, client):
        try:
            order_book = client.get_order_book(cls.symbol)
        except RpcError:
            return None
        min_row = min(
            order_book.orderbook.rows, key=lambda x: float(x.price.value)
        )
        return min_row.price

    @classmethod
    def get_max_order_book_price(cls, client):
        try:
            order_book = client.get_order_book(cls.symbol)
        except RpcError:
            return None
        max_row = max(
            order_book.orderbook.rows, key=lambda x: float(x.price.value)
        )
        return max_row.price

    @classmethod
    def create_limit_order_buy(cls, client, acc_id):
        if not cls.check_longable(client, acc_id):
            pytest.skip(f"По {cls.symbol} лонг не разрешен")
        limit_price = cls.get_min_order_book_price(client)
        if not limit_price:
            pytest.skip("Нет цены для выставления заявки")
        return client.place_order(
            acc_id,
            cls.symbol,
            quantity=Decimal(value="1"),
            side=Side.SIDE_BUY,
            type=OrderType.ORDER_TYPE_LIMIT,
            time_in_force=TimeInForce.TIME_IN_FORCE_DAY,
            limit_price=limit_price,
            stop_price=None,
            stop_condition=None,
            legs=None,
            client_order_id=None,
        )

    @classmethod
    def create_stop_order_by(cls, client, acc_id):
        if not cls.check_longable(client, acc_id):
            pytest.skip(f"По {cls.symbol} лонг не разрешен")
        stop_price = cls.get_max_order_book_price(client)
        if not stop_price:
            pytest.skip("Нет цены для выставления заявки")
        return client.place_order(
            acc_id,
            cls.symbol,
            quantity=Decimal(value="1"),
            side=Side.SIDE_BUY,
            type=OrderType.ORDER_TYPE_STOP,
            time_in_force=TimeInForce.TIME_IN_FORCE_DAY,
            limit_price=None,
            stop_price=stop_price,
            stop_condition=StopCondition.STOP_CONDITION_LAST_UP,
            legs=None,
            client_order_id=None,
        )


class TestSubscribe:
    def test_subscribe_unsubscribe_order_limit(self, sync_client, account_id):
        self.subscribe_order(
            sync_client, account_id, TestsOrdersService.create_limit_order_buy
        )

    def test_subscribe_unsubscribe_order_stop(self, sync_client, account_id):
        self.subscribe_order(
            sync_client, account_id, TestsOrdersService.create_stop_order_by
        )

    def test_subscribe_unsubscribe_trade_buy_sell(
        self, sync_client, account_id
    ):
        store = []
        sync_client.subscribe_order_trade(
            account_id, DataType.DATA_TYPE_TRADES
        )
        time.sleep(1)
        sync_client.on_order_trade = self.on_event(store)
        buy = self.buy_market(sync_client, account_id)
        time.sleep(2)
        sell = self.sell_market(sync_client, account_id)
        time.sleep(2)
        sync_client.unsubscribe_order_trade(
            account_id, DataType.DATA_TYPE_TRADES
        )
        assert len(store) == 2
        assert store[0].trades[0].order_id == buy.order_id
        assert store[1].trades[0].order_id == sell.order_id

    def test_subscribe_unsubscribe_order_trade_buy_sell(
        self, sync_client, account_id
    ):
        store = []
        sync_client.subscribe_order_trade(account_id, DataType.DATA_TYPE_ALL)
        time.sleep(1)
        sync_client.on_order_trade = self.on_event(store)
        buy = self.buy_market(sync_client, account_id)
        time.sleep(2)
        sell = self.sell_market(sync_client, account_id)
        time.sleep(2)
        sync_client.unsubscribe_order_trade(
            account_id, DataType.DATA_TYPE_TRADES
        )

        assert len(store) == 6
        assert store[0].orders[0].order_id == buy.order_id
        assert store[0].orders[0].status == OrderStatus.ORDER_STATUS_NEW
        assert store[1].orders[0].order_id == buy.order_id
        assert store[1].orders[0].status == OrderStatus.ORDER_STATUS_FILLED
        assert store[2].trades[0].order_id == buy.order_id

        assert store[3].orders[0].order_id == sell.order_id
        assert store[3].orders[0].status == OrderStatus.ORDER_STATUS_NEW
        assert store[4].orders[0].order_id == sell.order_id
        assert store[4].orders[0].status == OrderStatus.ORDER_STATUS_FILLED
        assert store[5].trades[0].order_id == sell.order_id

    @staticmethod
    def buy_market(client, acc_id):
        return client.place_order(
            acc_id,
            TestsOrdersService.symbol,
            quantity=Decimal(value="1"),
            side=Side.SIDE_BUY,
            type=OrderType.ORDER_TYPE_MARKET,
            time_in_force=TimeInForce.TIME_IN_FORCE_DAY,
            limit_price=None,
            stop_price=None,
            stop_condition=None,
            legs=None,
            client_order_id=None,
        )

    @staticmethod
    def sell_market(client, acc_id):
        return client.place_order(
            acc_id,
            TestsOrdersService.symbol,
            quantity=Decimal(value="1"),
            side=Side.SIDE_SELL,
            type=OrderType.ORDER_TYPE_MARKET,
            time_in_force=TimeInForce.TIME_IN_FORCE_DAY,
            limit_price=None,
            stop_price=None,
            stop_condition=None,
            legs=None,
            client_order_id=None,
        )

    @classmethod
    def subscribe_order(cls, client, acc_id, func):
        store: list[OrderTradeResponse] = []
        client.subscribe_order_trade(acc_id, DataType.DATA_TYPE_ORDERS)
        time.sleep(1)
        client.on_order_trade = cls.on_event(store)
        place = func(client, acc_id)
        time.sleep(2)
        cancel = client.cancel_order(acc_id, place.order_id)
        time.sleep(2)
        client.unsubscribe_order_trade(acc_id, DataType.DATA_TYPE_ORDERS)
        assert len(store) == 2
        for e, order in zip(store, (place, cancel)):
            o = next(
                filter(lambda x: x.order_id == order.order_id, e.orders), None
            )
            assert o is not None
            assert order.status == o.status

    @staticmethod
    def on_event(store: list):
        lock = threading.Lock()

        def handler(event: OrderTradeResponse):
            with lock:
                store.append(event)

        return handler
