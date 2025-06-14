import datetime
import threading
import time
from random import choice

import pytest
from grpc import RpcError

from finam_grpc_client.grpc.tradeapi.v1.marketdata.marketdata_service_pb2 import (
    Bar,
    SubscribeBarsResponse,
    TimeFrame,
)
from finam_grpc_client.tests.type_checker import TypeChecker


class TestsMarketDataService(TypeChecker):
    def test_get_bars(self, sync_client):
        end_time = datetime.datetime.now()
        start_time = end_time - datetime.timedelta(days=5)
        res = sync_client.get_bars(
            self.symbol, TimeFrame.TIME_FRAME_M1, start_time, end_time
        )
        assert isinstance(res.symbol, str)
        for b in res.bars:
            self.check_bar_type(b)

    @pytest.mark.parametrize(
        "days, timeframe",
        (
            (7, TimeFrame.TIME_FRAME_M1),
            (30, TimeFrame.TIME_FRAME_M5),
            (365, TimeFrame.TIME_FRAME_D),
            (365 * 5, TimeFrame.TIME_FRAME_QR),
        ),
    )
    def test_get_bars_max(self, sync_client, days, timeframe):
        end_time = datetime.datetime.now()
        start_time = end_time - datetime.timedelta(days=days)
        res = sync_client.get_bars(
            self.symbol, timeframe, start_time, end_time
        )
        assert res.symbol == self.symbol

    @pytest.mark.parametrize(
        "days, timeframe",
        (
            (7 + 1, TimeFrame.TIME_FRAME_M1),
            (30 + 2, TimeFrame.TIME_FRAME_M5),  # Выдает больше 30 дней
            (365 + 2, TimeFrame.TIME_FRAME_D),  # Выдает больше 365 дней
            (365 * 5 + 3, TimeFrame.TIME_FRAME_QR),
        ),  # Выдает больше 365 * 5 дней
    )
    def test_get_bars_max_negative(self, sync_client, days, timeframe):
        end_time = datetime.datetime.now()
        start_time = end_time - datetime.timedelta(days=days)
        with pytest.raises(RpcError) as exc:
            sync_client.get_bars(self.symbol, timeframe, start_time, end_time)
        assert "INVALID_ARGUMENT: Invalid date range" in exc.value.details()

    def test_get_last_quote(self, sync_client):
        assets = sync_client.get_assets()
        symbol = choice(assets.assets).symbol
        res = sync_client.get_last_quote(symbol)
        assert isinstance(res.symbol, str)
        self.check_quote_type(res.quote)
        assert res.symbol == symbol

    def test_get_order_book(self, sync_client):
        res = sync_client.get_order_book(self.symbol)
        assert isinstance(res.symbol, str)
        for r in res.orderbook.rows:
            self.check_order_book_row_type(r)
        assert res.symbol == self.symbol
        buys = filter(lambda x: x.buy_size.value != "", res.orderbook.rows)
        sells = filter(lambda x: x.sell_size.value != "", res.orderbook.rows)
        for b in buys:
            for s in sells:
                assert float(b.price.value) < float(s.price.value)

    def test_get_latest_trades(self, sync_client):
        res = sync_client.get_latest_trades(self.symbol)
        assert isinstance(res.symbol, str)
        for t in res.trades:
            self.check_trade_type(t)


class TestsSubscribes:
    symbol = TypeChecker.symbol

    @staticmethod
    def on_bar(store: list):
        last: Bar | None = None
        lock = threading.Lock()

        def wrapped_func(event: SubscribeBarsResponse):
            nonlocal last
            with lock:
                if not last:
                    last = event.bars[-1]
                    store.append(event.bars[-1])
                    return
                if last.timestamp.seconds == event.bars[-1].timestamp.seconds:
                    return
                store.append(event.bars[-1])
                last = event.bars[-1]

        return wrapped_func

    @staticmethod
    def on_event(store: list):

        def wrapped_func(event):
            store.append(event)

        return wrapped_func

    def test_subscribe_unsubscribe_bars(self, sync_client, account_id):
        store: list[SubscribeBarsResponse] = []
        sync_client.subscribe_bars(self.symbol, TimeFrame.TIME_FRAME_M1)
        sync_client.on_bar = self.on_bar(store)
        time.sleep(60)
        sync_client.unsubscribe_bars(self.symbol, TimeFrame.TIME_FRAME_M1)
        assert len(store) == 2
        store.clear()
        time.sleep(60)
        assert len(store) == 0
        sync_client.on_bar = sync_client.default_handler

    def test_subscribe_unsubscribe_order_book(self, sync_client, account_id):
        store = []
        sync_client.on_order_book = self.on_event(store)
        sync_client.subscribe_order_book(self.symbol)
        time.sleep(10)
        sync_client.unsubscribe_order_book(self.symbol)
        assert len(store) > 2
        store.clear()
        time.sleep(10)
        assert len(store) == 0
        sync_client.on_order_book = sync_client.default_handler

    def test_subscribe_unsubscribe_quote(self, sync_client, account_id):
        store = []
        sync_client.on_quote = self.on_event(store)
        sync_client.subscribe_quote(self.symbol)
        time.sleep(10)
        sync_client.unsubscribe_quote(self.symbol)
        assert len(store) > 2
        store.clear()
        time.sleep(10)
        assert len(store) == 0
        sync_client.on_quote = sync_client.default_handler

    def test_subscribe_unsubscribe_latest_trades(
        self, sync_client, account_id
    ):
        store = []
        sync_client.on_latest_trade = self.on_event(store)
        sync_client.subscribe_latest_trades(self.symbol)
        time.sleep(10)
        sync_client.unsubscribe_latest_trades(self.symbol)
        assert len(store) > 2
        store.clear()
        time.sleep(10)
        assert len(store) == 0
        sync_client.on_latest_trade = sync_client.default_handler
