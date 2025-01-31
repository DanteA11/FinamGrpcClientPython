import asyncio
from datetime import datetime

import pytest

from finam_grpc_client.models.proto.candles_pb2 import GetIntradayCandlesResult
from finam_grpc_client.models.proto.orders_pb2 import (
    OrderCondition,
    OrderStatus,
)


@pytest.mark.anyio
async def test_create_conditional_order_buy(client, client_id):
    orders_task = asyncio.create_task(client.get_orders(client_id=client_id))
    candles_task = asyncio.create_task(
        client.get_candles(
            security_board="TQBR",
            security_code="VTBR",
            time_frame="M1",
            count=1,
            to=datetime.now(),
        )
    )
    orders = await orders_task
    assert orders is not None
    amount = len(orders.orders)

    candles = await candles_task
    assert candles is not None
    assert isinstance(candles, GetIntradayCandlesResult)
    high_price_finam = candles.candles[0].high
    high_price = high_price_finam.num * 10**-high_price_finam.scale
    price = round(high_price * 1.03, high_price_finam.scale)

    new_order = await client.create_order(
        client_id=client_id,
        security_board="TQBR",
        security_code="VTBR",
        buy_sell="BUY_SELL_BUY",
        quantity=1,
        condition=OrderCondition(
            type="ORDER_CONDITION_TYPE_LAST_UP", price=price
        ),
    )
    assert new_order is not None
    assert new_order.client_id == client_id
    await asyncio.sleep(1)  # Чтобы успела обработаться информация о заявках.

    orders = await client.get_orders(client_id=client_id)
    assert orders is not None
    assert len(orders.orders) == amount + 1


@pytest.mark.anyio
async def test_cancel_conditional_order_buy(client, client_id):
    orders_task = asyncio.create_task(client.get_orders(client_id=client_id))
    candles_task = asyncio.create_task(
        client.get_candles(
            security_board="TQBR",
            security_code="VTBR",
            time_frame="M1",
            count=1,
            to=datetime.now(),
        )
    )
    orders_res = await orders_task
    assert orders_res is not None
    amount = len(orders_res.orders)
    idx = [
        order.transaction_id
        for order in orders_res.orders
        if order.status == OrderStatus.ORDER_STATUS_ACTIVE
    ]
    length = len(idx)
    candles = await candles_task
    assert isinstance(candles, GetIntradayCandlesResult)
    high_price_finam = candles.candles[0].high
    high_price = high_price_finam.num * 10**-high_price_finam.scale
    price = round(high_price * 1.03, high_price_finam.scale)

    new_order = await client.create_order(
        client_id=client_id,
        security_board="TQBR",
        security_code="VTBR",
        buy_sell="BUY_SELL_BUY",
        quantity=1,
        condition=OrderCondition(
            type="ORDER_CONDITION_TYPE_LAST_UP", price=price
        ),
    )
    assert new_order is not None
    assert new_order.client_id == client_id
    await asyncio.sleep(1)  # Чтобы успела обработаться информация о заявках.

    orders_res = await client.get_orders(client_id=client_id)
    assert orders_res is not None
    assert len(orders_res.orders) == amount + 1

    result = await client.cancel_order(
        client_id=client_id, transaction_id=new_order.transaction_id
    )
    assert result is not None
    assert result.client_id == client_id
    assert result.transaction_id == new_order.transaction_id

    await asyncio.sleep(1)  # Чтобы успела обработаться информация о заявках.
    orders_res = await client.get_orders(client_id=client_id)
    assert orders_res is not None
    idx = [
        order.transaction_id
        for order in orders_res.orders
        if order.status == OrderStatus.ORDER_STATUS_ACTIVE
    ]
    assert len(idx) == length


@pytest.mark.anyio
async def test_create_limit_order_buy(client, client_id):
    orders_task = asyncio.create_task(client.get_orders(client_id=client_id))
    candles_task = asyncio.create_task(
        client.get_candles(
            security_board="TQBR",
            security_code="VTBR",
            time_frame="M1",
            count=1,
            to=datetime.now(),
        )
    )
    orders = await orders_task
    assert orders is not None
    amount = len(orders.orders)

    candles = await candles_task
    assert isinstance(candles, GetIntradayCandlesResult)
    high_price_finam = candles.candles[0].high
    high_price = high_price_finam.num * 10**-high_price_finam.scale
    price = round(high_price * 0.97, high_price_finam.scale)

    new_order = await client.create_order(
        client_id=client_id,
        security_board="TQBR",
        security_code="VTBR",
        buy_sell="BUY_SELL_BUY",
        quantity=1,
        price=price,
    )
    assert new_order is not None
    assert new_order.client_id == client_id
    await asyncio.sleep(1)  # Чтобы успела обработаться информация о заявках.

    orders = await client.get_orders(client_id=client_id)
    assert orders is not None
    assert len(orders.orders) == amount + 1


@pytest.mark.anyio
async def test_cancel_limit_order_buy(client, client_id):
    orders_task = asyncio.create_task(client.get_orders(client_id=client_id))
    candles_task = asyncio.create_task(
        client.get_candles(
            security_board="TQBR",
            security_code="VTBR",
            time_frame="M1",
            count=1,
            to=datetime.now(),
        )
    )
    orders = await orders_task
    assert orders is not None
    amount = len(orders.orders)
    idx = [
        order.transaction_id
        for order in orders.orders
        if order.status == OrderStatus.ORDER_STATUS_ACTIVE
    ]
    length = len(idx)
    candles = await candles_task
    assert isinstance(candles, GetIntradayCandlesResult)
    high_price_finam = candles.candles[0].high
    high_price = high_price_finam.num * 10**-high_price_finam.scale
    price = round(high_price * 0.97, high_price_finam.scale)

    new_order = await client.create_order(
        client_id=client_id,
        security_board="TQBR",
        security_code="VTBR",
        buy_sell="BUY_SELL_BUY",
        quantity=1,
        price=price,
    )
    assert new_order is not None
    assert new_order.client_id == client_id
    await asyncio.sleep(1)  # Чтобы успела обработаться информация о заявках.

    orders = await client.get_orders(client_id=client_id)
    assert orders is not None
    assert len(orders.orders) == amount + 1

    result = await client.cancel_order(
        client_id=client_id, transaction_id=new_order.transaction_id
    )
    assert result is not None
    assert result.client_id == client_id
    assert result.transaction_id == new_order.transaction_id

    await asyncio.sleep(1)  # Чтобы успела обработаться информация о заявках.
    orders = await client.get_orders(client_id=client_id)
    assert orders is not None
    idx = [
        order.transaction_id
        for order in orders.orders
        if order.status == OrderStatus.ORDER_STATUS_ACTIVE
    ]
    assert len(idx) == length


@pytest.mark.anyio
async def test_create_conditional_order_sell(client, client_id):
    orders_task = asyncio.create_task(client.get_orders(client_id=client_id))
    candles_task = asyncio.create_task(
        client.get_candles(
            security_board="TQBR",
            security_code="VTBR",
            time_frame="M1",
            count=1,
            to=datetime.now(),
        )
    )
    orders = await orders_task
    assert orders is not None
    amount = len(orders.orders)

    candles = await candles_task
    assert isinstance(candles, GetIntradayCandlesResult)
    high_price_finam = candles.candles[0].high
    high_price = high_price_finam.num * 10**-high_price_finam.scale
    price = round(high_price * 0.97, high_price_finam.scale)

    new_order = await client.create_order(
        client_id=client_id,
        security_board="TQBR",
        security_code="VTBR",
        buy_sell="BUY_SELL_SELL",
        quantity=1,
        condition=OrderCondition(
            type="ORDER_CONDITION_TYPE_LAST_DOWN", price=price
        ),
    )
    assert new_order is not None
    assert new_order.client_id == client_id
    await asyncio.sleep(1)  # Чтобы успела обработаться информация о заявках.

    orders = await client.get_orders(client_id=client_id)
    assert orders is not None
    assert len(orders.orders) == amount + 1


@pytest.mark.anyio
async def test_cancel_conditional_order_sell(client, client_id):
    orders_task = asyncio.create_task(client.get_orders(client_id=client_id))
    candles_task = asyncio.create_task(
        client.get_candles(
            security_board="TQBR",
            security_code="VTBR",
            time_frame="M1",
            count=1,
            to=datetime.now(),
        )
    )
    orders = await orders_task
    assert orders is not None
    amount = len(orders.orders)
    idx = [
        order.transaction_id
        for order in orders.orders
        if order.status == OrderStatus.ORDER_STATUS_ACTIVE
    ]
    length = len(idx)
    candles = await candles_task
    assert isinstance(candles, GetIntradayCandlesResult)
    high_price_finam = candles.candles[0].high
    high_price = high_price_finam.num * 10**-high_price_finam.scale
    price = round(high_price * 0.97, high_price_finam.scale)

    new_order = await client.create_order(
        client_id=client_id,
        security_board="TQBR",
        security_code="VTBR",
        buy_sell="BUY_SELL_SELL",
        quantity=1,
        condition=OrderCondition(
            type="ORDER_CONDITION_TYPE_LAST_DOWN", price=price
        ),
    )
    assert new_order is not None
    assert new_order.client_id == client_id
    await asyncio.sleep(1)  # Чтобы успела обработаться информация о заявках.

    orders = await client.get_orders(client_id=client_id)
    assert orders is not None
    assert len(orders.orders) == amount + 1

    result = await client.cancel_order(
        client_id=client_id, transaction_id=new_order.transaction_id
    )
    assert result is not None
    assert result.client_id == client_id
    assert result.transaction_id == new_order.transaction_id

    await asyncio.sleep(1)  # Чтобы успела обработаться информация о заявках.
    orders = await client.get_orders(client_id=client_id)
    assert orders is not None
    idx = [
        order.transaction_id
        for order in orders.orders
        if order.status == OrderStatus.ORDER_STATUS_ACTIVE
    ]
    assert len(idx) == length


@pytest.mark.anyio
async def test_create_limit_order_sell(client, client_id):
    orders_task = asyncio.create_task(client.get_orders(client_id=client_id))
    candles_task = asyncio.create_task(
        client.get_candles(
            security_board="TQBR",
            security_code="VTBR",
            time_frame="M1",
            count=1,
            to=datetime.now(),
        )
    )
    orders = await orders_task
    assert orders is not None
    amount = len(orders.orders)

    candles = await candles_task
    assert isinstance(candles, GetIntradayCandlesResult)
    high_price_finam = candles.candles[0].high
    high_price = high_price_finam.num * 10**-high_price_finam.scale
    price = round(high_price * 1.03, high_price_finam.scale)

    new_order = await client.create_order(
        client_id=client_id,
        security_board="TQBR",
        security_code="VTBR",
        buy_sell="BUY_SELL_SELL",
        quantity=1,
        price=price,
    )
    assert new_order is not None
    assert new_order.client_id == client_id
    await asyncio.sleep(1)  # Чтобы успела обработаться информация о заявках.

    orders = await client.get_orders(client_id=client_id)
    assert orders is not None
    assert len(orders.orders) == amount + 1


@pytest.mark.anyio
async def test_cancel_limit_order_sell(client, client_id):
    orders_task = asyncio.create_task(client.get_orders(client_id=client_id))
    candles_task = asyncio.create_task(
        client.get_candles(
            security_board="TQBR",
            security_code="VTBR",
            time_frame="M1",
            count=1,
            to=datetime.now(),
        )
    )
    orders = await orders_task
    assert orders is not None
    amount = len(orders.orders)
    idx = [
        order.transaction_id
        for order in orders.orders
        if order.status == OrderStatus.ORDER_STATUS_ACTIVE
    ]
    length = len(idx)
    candles = await candles_task
    assert isinstance(candles, GetIntradayCandlesResult)
    high_price_finam = candles.candles[0].high
    high_price = high_price_finam.num * 10**-high_price_finam.scale
    price = round(high_price * 1.03, high_price_finam.scale)

    new_order = await client.create_order(
        client_id=client_id,
        security_board="TQBR",
        security_code="VTBR",
        buy_sell="BUY_SELL_SELL",
        quantity=1,
        price=price,
    )
    assert new_order is not None
    assert new_order.client_id == client_id
    await asyncio.sleep(1)  # Чтобы успела обработаться информация о заявках.

    orders = await client.get_orders(client_id=client_id)
    assert orders is not None
    assert len(orders.orders) == amount + 1

    result = await client.cancel_order(
        client_id=client_id, transaction_id=new_order.transaction_id
    )
    assert result is not None
    assert result.client_id == client_id
    assert result.transaction_id == new_order.transaction_id

    await asyncio.sleep(1)  # Чтобы успела обработаться информация о заявках.
    orders = await client.get_orders(client_id=client_id)
    assert orders is not None
    idx = [
        order.transaction_id
        for order in orders.orders
        if order.status == OrderStatus.ORDER_STATUS_ACTIVE
    ]
    assert len(idx) == length


@pytest.mark.anyio
async def test_cancel_all_orders(client, client_id):
    orders = await client.get_orders(client_id=client_id)
    assert orders is not None
    idx = [
        order.transaction_id
        for order in orders.orders
        if order.status == OrderStatus.ORDER_STATUS_ACTIVE
    ]
    tasks = []
    for id_ in idx:
        tasks.append(
            client.cancel_order(client_id=client_id, transaction_id=id_)
        )
    results = await asyncio.gather(*tasks)
    for result in results:
        assert result is not None
        assert result.client_id == client_id
        assert result.transaction_id in idx
    await asyncio.sleep(1)  # Чтобы успела обработаться информация о заявках.
    orders = await client.get_orders(client_id=client_id)
    assert orders is not None
    idx = [
        order.transaction_id
        for order in orders.orders
        if order.status == OrderStatus.ORDER_STATUS_ACTIVE
    ]
    assert len(idx) == 0
