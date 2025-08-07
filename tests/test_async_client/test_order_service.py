import asyncio
from random import choice

import pytest
from google.type.decimal_pb2 import Decimal
from grpc.aio import AioRpcError

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


@pytest.mark.anyio
class TestsOrdersService(TypeChecker):

    async def test_place_cancel_order_buy_limit(
        self, async_client, account_id
    ):
        if not await self.check_longable(async_client, account_id):
            pytest.skip(f"По {self.symbol} лонг не разрешен")
        place = await self.create_limit_order_buy(async_client, account_id)
        self.check_order_state_type(place)
        assert place.status == OrderStatus.ORDER_STATUS_NEW
        cancel = await async_client.cancel_order(account_id, place.order_id)
        self.check_order_state_type(cancel)
        assert cancel.status == OrderStatus.ORDER_STATUS_CANCELED

    async def test_place_cancel_order_sell_limit(
        self, async_client, account_id
    ):
        if not await self.check_shortable(async_client, account_id):
            pytest.skip(f"По {self.symbol} шорт не разрешен")
        limit_price = await self.get_max_order_book_price(async_client)
        if not limit_price:
            pytest.skip("Нет цены для выставления заявки")
        try:
            place = await async_client.place_order(
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
        except AioRpcError as exc:
            if "Не хватает собственных бумаг" in exc.details():
                pytest.fail(
                    "Ошибка в GetAssetParamsResponse. Шорт не разрешен.",
                    pytrace=False,
                )

        self.check_order_state_type(place)
        assert place.status == OrderStatus.ORDER_STATUS_NEW
        cancel = await async_client.cancel_order(account_id, place.order_id)
        self.check_order_state_type(cancel)
        assert cancel.status == OrderStatus.ORDER_STATUS_CANCELED

    async def test_place_cancel_order_buy_stop(self, async_client, account_id):
        if not await self.check_longable(async_client, account_id):
            pytest.skip(f"По {self.symbol} лонг не разрешен")
        place = await self.create_stop_order_by(async_client, account_id)
        self.check_order_state_type(place)
        assert place.status == OrderStatus.ORDER_STATUS_WATCHING
        cancel = await async_client.cancel_order(account_id, place.order_id)
        self.check_order_state_type(cancel)
        assert cancel.status == OrderStatus.ORDER_STATUS_CANCELED

    async def test_place_cancel_order_sell_stop(
        self, async_client, account_id
    ):
        if not await self.check_shortable(async_client, account_id):
            pytest.skip(f"По {self.symbol} шорт не разрешен")
        stop_price = await self.get_min_order_book_price(async_client)
        if not stop_price:
            pytest.skip("Нет цены для выставления заявки")
        place = await async_client.place_order(
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
        cancel = await async_client.cancel_order(account_id, place.order_id)
        self.check_order_state_type(cancel)
        assert cancel.status == OrderStatus.ORDER_STATUS_CANCELED

    async def test_place_cancel_order_buy_stop_limit(
        self, async_client, account_id
    ):
        if not await self.check_longable(async_client, account_id):
            pytest.skip(f"По {self.symbol} лонг не разрешен")
        stop_price = limit_price = await self.get_max_order_book_price(
            async_client
        )
        if not stop_price:
            pytest.skip("Нет цены для выставления заявки")
        place = await async_client.place_order(
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
        cancel = await async_client.cancel_order(account_id, place.order_id)
        self.check_order_state_type(cancel)
        assert cancel.status == OrderStatus.ORDER_STATUS_CANCELED

    async def test_place_cancel_order_sell_stop_limit(
        self, async_client, account_id
    ):
        if not await self.check_shortable(async_client, account_id):
            pytest.skip(f"По {self.symbol} лонг не разрешен")
        stop_price = limit_price = await self.get_min_order_book_price(
            async_client
        )
        if not stop_price:
            pytest.skip("Нет цены для выставления заявки")
        place = await async_client.place_order(
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
        cancel = await async_client.cancel_order(account_id, place.order_id)
        self.check_order_state_type(cancel)
        assert cancel.status == OrderStatus.ORDER_STATUS_CANCELED

    async def test_get_orders(self, async_client, account_id):
        res = await async_client.get_orders(account_id)
        for os in res.orders:
            self.check_order_state_type(os)
            assert os.order.account_id == account_id

    async def test_get_orders_negative(self, async_client):
        account_id = "111111"
        with pytest.raises(AioRpcError) as exc:
            await async_client.get_orders(account_id)
        assert (
            f"Account with id {account_id} is not found" in exc.value.details()
        )

    async def test_get_order(self, async_client, account_id):
        orders = await async_client.get_orders(account_id)
        if len(orders.orders) == 0:
            pytest.skip("Нет заявок")
        order_id = choice(orders.orders).order_id
        res = await async_client.get_order(account_id, order_id)
        self.check_order_state_type(res)
        assert res.order.account_id == account_id

    @classmethod
    async def check_longable(cls, client, acc_id):
        asset_params = await client.get_asset_params(cls.symbol, acc_id)
        return asset_params.longable.value == Longable.Status.AVAILABLE

    @classmethod
    async def check_shortable(cls, client, acc_id):
        asset_params = await client.get_asset_params(cls.symbol, acc_id)
        return asset_params.shortable.value == Shortable.Status.AVAILABLE

    @classmethod
    async def get_min_order_book_price(cls, client):
        try:
            order_book = await client.get_order_book(cls.symbol)
        except AioRpcError:
            return None
        min_row = min(
            order_book.orderbook.rows, key=lambda x: float(x.price.value)
        )
        return min_row.price

    @classmethod
    async def get_max_order_book_price(cls, client):
        try:
            order_book = await client.get_order_book(cls.symbol)
        except AioRpcError:
            return None
        max_row = max(
            order_book.orderbook.rows, key=lambda x: float(x.price.value)
        )
        return max_row.price

    @classmethod
    async def create_limit_order_buy(cls, client, acc_id):
        if not await cls.check_longable(client, acc_id):
            pytest.skip(f"По {cls.symbol} лонг не разрешен")
        limit_price = await cls.get_min_order_book_price(client)
        if not limit_price:
            pytest.skip("Нет цены для выставления заявки")
        return await client.place_order(
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
    async def create_stop_order_by(cls, client, acc_id):
        if not await cls.check_longable(client, acc_id):
            pytest.skip(f"По {cls.symbol} лонг не разрешен")
        stop_price = await cls.get_max_order_book_price(client)
        if not stop_price:
            pytest.skip("Нет цены для выставления заявки")
        return await client.place_order(
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


@pytest.mark.anyio
class TestSubscribe:
    async def test_subscribe_unsubscribe_order_limit(
        self, async_client, account_id
    ):
        await self.subscribe_order(
            async_client, account_id, TestsOrdersService.create_limit_order_buy
        )

    async def test_subscribe_unsubscribe_order_stop(
        self, async_client, account_id
    ):
        await self.subscribe_order(
            async_client, account_id, TestsOrdersService.create_stop_order_by
        )

    async def test_subscribe_unsubscribe_trade_buy_sell(
        self, async_client, account_id
    ):
        store = []
        await async_client.subscribe_order_trade(
            account_id, DataType.DATA_TYPE_TRADES
        )
        await asyncio.sleep(1)
        async_client.on_order_trade = self.on_event(store)
        buy = await self.buy_market(async_client, account_id)
        await asyncio.sleep(2)
        sell = await self.sell_market(async_client, account_id)
        await asyncio.sleep(2)
        await async_client.unsubscribe_order_trade(
            account_id, DataType.DATA_TYPE_TRADES
        )
        assert len(store) == 2
        assert store[0].trades[0].order_id == buy.order_id
        assert store[1].trades[0].order_id == sell.order_id

    async def test_subscribe_unsubscribe_order_trade_buy_sell(
        self, async_client, account_id
    ):
        store = []
        await async_client.subscribe_order_trade(
            account_id, DataType.DATA_TYPE_ALL
        )
        await asyncio.sleep(1)
        async_client.on_order_trade = self.on_event(store)
        buy = await self.buy_market(async_client, account_id)
        await asyncio.sleep(2)
        sell = await self.sell_market(async_client, account_id)
        await asyncio.sleep(2)
        await async_client.unsubscribe_order_trade(
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

    @classmethod
    async def subscribe_order(cls, client, acc_id, func):
        store: list[OrderTradeResponse] = []
        await client.subscribe_order_trade(acc_id, DataType.DATA_TYPE_ORDERS)
        await asyncio.sleep(1)
        client.on_order_trade = cls.on_event(store)
        place = await func(client, acc_id)
        await asyncio.sleep(2)
        cancel = await client.cancel_order(acc_id, place.order_id)
        await asyncio.sleep(2)
        await client.unsubscribe_order_trade(acc_id, DataType.DATA_TYPE_ORDERS)
        assert len(store) == 2
        for e, order in zip(store, (place, cancel)):
            o = next(
                filter(lambda x: x.order_id == order.order_id, e.orders), None
            )
            assert o is not None
            assert order.status == o.status

    @staticmethod
    async def buy_market(client, acc_id):
        return await client.place_order(
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
    async def sell_market(client, acc_id):
        return await client.place_order(
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

    @staticmethod
    def on_event(store: list):
        lock = asyncio.Lock()

        async def handler(event: OrderTradeResponse):
            async with lock:
                store.append(event)

        return handler
