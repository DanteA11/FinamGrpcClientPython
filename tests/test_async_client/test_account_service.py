import datetime

import pytest
from google.protobuf.timestamp_pb2 import Timestamp
from google.type.decimal_pb2 import Decimal
from grpc.aio import AioRpcError

from tests.type_checker import TypeChecker


@pytest.mark.anyio
class TestsAccountService(TypeChecker):
    async def test_get_account_info(self, async_client, account_id):
        assert account_id in async_client.account_ids
        res = await async_client.get_account_info(account_id)
        assert isinstance(res.account_id, str)
        assert isinstance(res.type, str)
        assert isinstance(res.status, str)
        assert isinstance(res.equity, Decimal)
        assert isinstance(res.unrealized_profit, Decimal)
        for p in res.positions:
            self.check_position_type(p)
        for c in res.cash:
            self.check_money_type(c)
        assert res.account_id == account_id
        assert res.status == "ACCOUNT_ACTIVE"

    async def test_get_account_info_negative(self, async_client):
        account_id = "111111"
        assert account_id not in async_client.account_ids
        with pytest.raises(AioRpcError) as exc:
            await async_client.get_account_info(account_id)
        assert (
            f"Account with id {account_id} is not found" in exc.value.details()
        )

    @pytest.mark.xfail(
        reason="Нет сделок на аккаунте за последние 52 недели", run=True
    )
    async def test_get_trades(self, async_client, account_id):
        end_time = datetime.datetime.now()
        start_time = end_time - datetime.timedelta(weeks=52)
        res = await async_client.get_trades(
            account_id, 1, start_time, end_time
        )
        for t in res.trades:
            self.check_account_trade_type(t)
        assert len(res.trades) > 0
        assert len(res.trades) == 1

    async def test_get_trades_negative(self, async_client, account_id):
        end_time = datetime.datetime.now()
        start_time = end_time - datetime.timedelta(weeks=52)
        with pytest.raises(AioRpcError) as exc:
            await async_client.get_trades(account_id, 1, end_time, start_time)
        assert "'StartTime' must be less then 'endTime'" in exc.value.details()

    @pytest.mark.xfail(
        reason="Нет транзакций на аккаунте за последние 52 недели", run=True
    )
    async def test_get_transactions(self, async_client, account_id):
        end_time = datetime.datetime.now()
        start_time = end_time - datetime.timedelta(weeks=52)
        res = await async_client.get_transactions(
            account_id, 1, start_time, end_time
        )
        for t in res.transactions:
            assert isinstance(t.id, str)
            assert isinstance(t.category, str)
            assert isinstance(t.timestamp, Timestamp)
            assert isinstance(t.symbol, str)
            self.check_money_type(t.change)
            assert isinstance(t.trade.size, Decimal)
            assert isinstance(t.trade.price, Decimal)
            assert isinstance(t.trade.accrued_interest, Decimal)

        assert len(res.transactions) > 0
        assert len(res.transactions) == 1

    async def test_get_transactions_negative(self, async_client, account_id):
        end_time = datetime.datetime.now()
        start_time = end_time - datetime.timedelta(weeks=52)
        with pytest.raises(AioRpcError) as exc:
            await async_client.get_transactions(
                account_id, 1, end_time, start_time
            )
        assert "'StartTime' must be less then 'endTime'" in exc.value.details()
