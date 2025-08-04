import asyncio
import datetime
from random import choice

import pytest
from grpc.aio import AioRpcError

from finam_grpc_client.grpc.tradeapi.v1.marketdata.marketdata_service_pb2 import (
    Bar,
    SubscribeBarsResponse,
    TimeFrame,
)
from tests.type_checker import TypeChecker


@pytest.mark.anyio
class TestsMarketDataService(TypeChecker):
    async def test_get_bars(self, async_client):
        end_time = datetime.datetime.now()
        start_time = end_time - datetime.timedelta(days=5)
        res = await async_client.get_bars(
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
    async def test_get_bars_max(self, async_client, days, timeframe):
        end_time = datetime.datetime.now()
        start_time = end_time - datetime.timedelta(days=days)
        res = await async_client.get_bars(
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
    async def test_get_bars_max_negative(self, async_client, days, timeframe):
        end_time = datetime.datetime.now()
        start_time = end_time - datetime.timedelta(days=days)
        with pytest.raises(AioRpcError) as exc:
            await async_client.get_bars(
                self.symbol, timeframe, start_time, end_time
            )
        assert "INVALID_ARGUMENT: Invalid date range" in exc.value.details()

    async def test_get_last_quote(self, async_client):
        assets = await async_client.get_assets()
        symbol = choice(assets.assets).symbol
        res = await async_client.get_last_quote(symbol)
        assert isinstance(res.symbol, str)
        self.check_quote_type(res.quote)
        assert res.symbol == symbol

    async def test_get_order_book(self, async_client):
        try:
            res = await async_client.get_order_book(self.symbol)
        except AioRpcError:
            pytest.skip("Нет стакана")
        assert isinstance(res.symbol, str)
        for r in res.orderbook.rows:
            self.check_order_book_row_type(r)
        assert res.symbol == self.symbol
        buys = filter(lambda x: x.buy_size.value != "", res.orderbook.rows)
        sells = filter(lambda x: x.sell_size.value != "", res.orderbook.rows)
        for b in buys:
            for s in sells:
                assert float(b.price.value) < float(s.price.value)

    async def test_get_latest_trades(self, async_client):
        res = await async_client.get_latest_trades(self.symbol)
        assert isinstance(res.symbol, str)
        for t in res.trades:
            self.check_trade_type(t)


@pytest.mark.anyio
class TestsSubscribes:
    symbol = TypeChecker.symbol

    async def test_subscribe_unsubscribe_bars(self, async_client):
        store: list[SubscribeBarsResponse] = []
        async_client.on_bar = self.on_bar(store)
        await async_client.subscribe_bars(self.symbol, TimeFrame.TIME_FRAME_M1)
        await asyncio.sleep(60)
        await async_client.unsubscribe_bars(
            self.symbol, TimeFrame.TIME_FRAME_M1
        )
        assert len(store) == 2
        store.clear()
        await asyncio.sleep(60)
        assert len(store) == 0
        async_client.on_bar = async_client.default_handler

    async def test_subscribe_unsubscribe_several_bars(self, async_client):
        store: list[SubscribeBarsResponse] = []
        sym = "SBER@MISX"
        async_client.on_bar = self.on_bar(store)
        await async_client.subscribe_bars(self.symbol, TimeFrame.TIME_FRAME_M1)
        await async_client.subscribe_bars(sym, TimeFrame.TIME_FRAME_M1)
        await asyncio.sleep(60)
        await async_client.unsubscribe_bars(
            self.symbol, TimeFrame.TIME_FRAME_M1
        )
        await async_client.unsubscribe_bars(sym, TimeFrame.TIME_FRAME_M1)
        assert len(store) == 4
        store.clear()
        await asyncio.sleep(60)
        assert len(store) == 0
        async_client.on_bar = async_client.default_handler

    async def test_subscribe_unsubscribe_several_bars_with_separate_handlers(
        self, async_client
    ):
        store_1: list[SubscribeBarsResponse] = []
        store_2: list[SubscribeBarsResponse] = []
        sym = "SBER@MISX"
        async_client.on_bar = self.on_bar(store_1)
        await async_client.subscribe_bars(self.symbol, TimeFrame.TIME_FRAME_M1)
        await async_client.subscribe_bars(
            sym, TimeFrame.TIME_FRAME_M1, handler=self.on_bar(store_2)
        )
        await asyncio.sleep(60)
        await async_client.unsubscribe_bars(
            self.symbol, TimeFrame.TIME_FRAME_M1
        )
        await async_client.unsubscribe_bars(sym, TimeFrame.TIME_FRAME_M1)
        assert len(store_1) == 2
        assert len(store_2) == 2
        store_1.clear()
        store_2.clear()
        await asyncio.sleep(60)
        assert len(store_1) == 0
        assert len(store_2) == 0
        async_client.on_bar = async_client.default_handler

    async def test_subscribe_unsubscribe_order_book(self, async_client):
        store = []
        async_client.on_order_book = self.on_event(store)
        await async_client.subscribe_order_book(self.symbol)
        await asyncio.sleep(10)
        await async_client.unsubscribe_order_book(self.symbol)
        assert len(store) > 2
        store.clear()
        await asyncio.sleep(10)
        assert len(store) == 0
        async_client.on_order_book = async_client.default_handler

    async def test_subscribe_unsubscribe_order_book_with_not_default_handler(
        self, async_client
    ):
        store = []
        await async_client.subscribe_order_book(
            self.symbol, handler=self.on_event(store)
        )
        await asyncio.sleep(10)
        await async_client.unsubscribe_order_book(self.symbol)
        assert len(store) > 2
        store.clear()
        await asyncio.sleep(10)
        assert len(store) == 0

    async def test_subscribe_unsubscribe_quote(self, async_client):
        store = []
        async_client.on_quote = self.on_event(store)
        await async_client.subscribe_quote(self.symbol)
        await asyncio.sleep(10)
        await async_client.unsubscribe_quote(self.symbol)
        assert len(store) > 2
        store.clear()
        await asyncio.sleep(10)
        assert len(store) == 0
        async_client.on_quote = async_client.default_handler

    async def test_subscribe_unsubscribe_latest_trades(self, async_client):
        store = []
        async_client.on_latest_trade = self.on_event(store)
        await async_client.subscribe_latest_trades(self.symbol)
        await asyncio.sleep(10)
        await async_client.unsubscribe_latest_trades(self.symbol)
        assert len(store) > 2
        store.clear()
        await asyncio.sleep(10)
        assert len(store) == 0
        async_client.on_latest_trade = async_client.default_handler

    async def test_double_subscribe(self, async_client, caplog):
        store = []
        async_client.on_quote = self.on_event(store)
        await async_client.subscribe_quote(self.symbol)
        await asyncio.sleep(5)
        await async_client.subscribe_quote(self.symbol)
        await asyncio.sleep(5)
        check = False
        for record in caplog.records:
            if record.levelname != "WARNING":
                continue
            assert "Подписка уже существует" in record.message
            check = True
        else:
            if not check:
                pytest.fail("Не найдено логов уровня WARNING")
        await async_client.unsubscribe_quote(self.symbol)
        assert len(store) > 2
        store.clear()
        await asyncio.sleep(10)
        assert len(store) == 0
        async_client.on_quote = async_client.default_handler

    @staticmethod
    def on_bar(store: list):
        last: dict[str, Bar] = {}

        async def wrapped_func(event: SubscribeBarsResponse):
            l = last.get(event.symbol)
            r = event.bars[-1]
            if not l:
                last[event.symbol] = r
                store.append(r)
                return
            if l.timestamp.seconds == r.timestamp.seconds:
                return
            last[event.symbol] = r
            store.append(r)

        return wrapped_func

    @staticmethod
    def on_event(store: list):

        async def wrapped_func(event):
            store.append(event)

        return wrapped_func
