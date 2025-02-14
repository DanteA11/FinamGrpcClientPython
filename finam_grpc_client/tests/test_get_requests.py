from datetime import date, datetime, timedelta
from random import randint

import pytest

from finam_grpc_client.models.proto.candles_pb2 import (
    GetDayCandlesResult,
    GetIntradayCandlesResult,
)
from finam_grpc_client.models.proto.orders_pb2 import Order
from finam_grpc_client.models.proto.security_pb2 import Security
from finam_grpc_client.models.proto.stops_pb2 import Stop


@pytest.mark.anyio
@pytest.mark.parametrize(
    "code, time_frame",
    (
        ("SBER", "D1"),
        ("SBER", "W1"),
        ("VTBR", "D1"),
        ("VTBR", "W1"),
    ),
)
async def test_get_day_candles(client, code, time_frame):
    random_date = date.today() - timedelta(days=randint(1, 20))
    count = randint(1, 20)
    if randint(0, 1):
        from_ = None
        to = random_date
    else:
        from_ = random_date
        to = None

    result = await client.get_candles(
        security_board="TQBR",
        security_code=code,
        time_frame=time_frame,
        count=count,
        from_=from_,
        to=to,
    )
    assert result is not None
    assert isinstance(result, GetDayCandlesResult)
    assert len(result.candles) <= count


@pytest.mark.anyio
async def test_get_day_candles_with_bad_code(client):
    random_date = date.today() - timedelta(days=randint(1, 20))
    count = randint(1, 20)
    to = random_date
    result = await client.get_candles(
        security_board="TQBR",
        security_code="code",
        time_frame="D1",
        count=count,
        to=to,
    )
    assert result is None


@pytest.mark.anyio
@pytest.mark.parametrize(
    "code, time_frame",
    (
        ("SBER", "M1"),
        ("SBER", "M5"),
        ("VTBR", "M15"),
        ("VTBR", "H1"),
    ),
)
async def test_get_intraday_candles(client, code, time_frame):
    random_datetime = datetime.now() - timedelta(hours=randint(1, 20))
    count = randint(1, 20)
    if randint(0, 1):
        from_ = None
        to = random_datetime
    else:
        from_ = random_datetime
        to = None
    result = await client.get_candles(
        security_board="TQBR",
        security_code=code,
        time_frame=time_frame,
        count=count,
        from_=from_,
        to=to,
    )
    assert result is not None
    assert isinstance(result, GetIntradayCandlesResult)
    assert len(result.candles) <= count


@pytest.mark.anyio
async def test_get_portfolio(client, client_id):
    result = await client.get_portfolio(client_id=client_id)
    assert result is not None
    assert result.client_id == client_id


@pytest.mark.anyio
async def test_get_portfolio_without_client_id(client):
    result = await client.get_portfolio(client_id="")
    assert result is None


@pytest.mark.anyio
async def test_get_portfolio_with_bad_client_id(client):
    result = await client.get_portfolio(client_id="asd")
    assert result is None


@pytest.mark.anyio
async def test_get_orders(client, client_id):
    result = await client.get_orders(client_id=client_id)
    assert result is not None
    assert result.client_id == client_id
    for order in result.orders:
        assert isinstance(order, Order)


@pytest.mark.anyio
async def test_get_orders_with_bad_client_id(client):
    result = await client.get_orders(client_id="client_id")
    assert result is None


@pytest.mark.anyio
async def test_get_stops(client, client_id):
    result = await client.get_stops(client_id=client_id)
    assert result is not None
    assert result.client_id == client_id
    for stop in result.stops:
        assert isinstance(stop, Stop)


@pytest.mark.anyio
async def test_get_stops_with_bad_client_id(client):
    result = await client.get_stops(client_id="client_id")
    assert result is None


@pytest.mark.anyio
async def test_get_securities_from_api(client):
    code = "GAZP"
    result = await client.get_securities(seccode=code)
    assert result is not None
    for security in result.securities:
        assert isinstance(security, Security)
        assert security.code == code


@pytest.mark.anyio
async def test_get_many_request_securities_from_api(client):
    await client.get_securities(seccode="qwerty")
    result = await client.get_securities(seccode="qwerty")
    assert result is None
