import time
from random import choice

import pytest
from google.type.date_pb2 import Date
from google.type.decimal_pb2 import Decimal
from google.type.interval_pb2 import Interval
from grpc.aio import AioRpcError

from finam_grpc_client.grpc.tradeapi.v1.assets.assets_service_pb2 import (
    Longable,
    Shortable,
)
from finam_grpc_client.tests.type_checker import TypeChecker


@pytest.mark.anyio
class TestsAssetsService(TypeChecker):
    async def test_get_exchanges(self, async_client):
        res = await async_client.get_exchanges()
        for e in res.exchanges:
            assert isinstance(e.mic, str)
            assert isinstance(e.name, str)
        assert len(res.exchanges) > 0

    async def test_get_assets(self, async_client):
        res = await async_client.get_assets()
        for a in res.assets:
            assert isinstance(a.symbol, str)
            assert isinstance(a.id, str)
            assert isinstance(a.ticker, str)
            assert isinstance(a.mic, str)
            assert isinstance(a.isin, str)
            assert isinstance(a.type, str)
            assert isinstance(a.name, str)
        assert len(res.assets) > 0

    async def test_get_asset_params(self, async_client, account_id):
        assets = await async_client.get_assets()
        symbol = choice(assets.assets).symbol
        res = await async_client.get_asset_params(symbol, account_id)
        assert isinstance(res.symbol, str)
        assert isinstance(res.account_id, str)
        assert isinstance(res.tradeable, bool)
        assert isinstance(res.longable, Longable)
        assert isinstance(res.shortable, Shortable)
        assert isinstance(res.long_risk_rate, Decimal)
        self.check_money_type(res.long_collateral)
        assert isinstance(res.short_risk_rate, Decimal)
        self.check_money_type(res.short_collateral)
        assert res.account_id == account_id
        assert res.symbol == symbol

    async def test_get_asset_params_negative(self, async_client, account_id):
        symbol = "LKOH"
        with pytest.raises(AioRpcError) as exc:
            await async_client.get_asset_params(symbol, account_id)
        assert "Mic must not be empty" in exc.value.details()

    async def test_get_options_chain(self, async_client):
        symbol = "LKOH@RTSX"
        res = await async_client.get_options_chain(symbol)
        assert isinstance(res.symbol, str)
        for o in res.options:
            assert o.symbol == symbol
            assert isinstance(o.symbol, str)
            assert isinstance(o.contract_size, Decimal)
            assert isinstance(o.trade_first_day, Date)
            assert isinstance(o.trade_last_day, Date)
            assert isinstance(o.strike, Decimal)
            assert isinstance(o.multiplier, Decimal)
        assert len(res.options) > 0

    async def test_get_options_chain_negative(self, async_client):
        symbol = "asdasd@RTSX"
        res = await async_client.get_options_chain(symbol)
        assert len(res.options) == 0

    async def test_get_schedule(self, async_client):
        assets = await async_client.get_assets()
        symbol = choice(assets.assets).symbol
        res = await async_client.get_schedule(symbol)
        assert isinstance(res.symbol, str)
        for s in res.sessions:
            assert isinstance(s.type, str)
            assert isinstance(s.interval, Interval)
        assert res.symbol == symbol

    async def test_get_clock(self, async_client):
        lag = 100  # Максимальное допустимое различие во времени
        res = await async_client.get_clock()
        assert abs(res.timestamp.ToMilliseconds() - time.time() * 1000) < lag

    async def test_get_asset(self, async_client, account_id):
        assets = await async_client.get_assets()
        symbol = choice(assets.assets).symbol
        res = await async_client.get_asset(symbol, account_id)
        assert isinstance(res.board, str)
        assert isinstance(res.id, str)
        assert isinstance(res.ticker, str)
        assert isinstance(res.mic, str)
        assert isinstance(res.isin, str)
        assert isinstance(res.type, str)
        assert isinstance(res.name, str)
        assert isinstance(res.decimals, int)
        assert isinstance(res.min_step, int)
        assert isinstance(res.lot_size, Decimal)
        assert isinstance(res.expiration_date, Date)
