import asyncio
from datetime import datetime

import pytest

from finam_grpc_client.models.proto.candles_pb2 import GetIntradayCandlesResult
from finam_grpc_client.models.proto.common_pb2 import (
    OrderValidBefore,
    OrderValidBeforeType,
)
from finam_grpc_client.models.proto.stops_pb2 import (
    StopLoss,
    StopQuantity,
    StopQuantityUnits,
    TakeProfit,
)


@pytest.mark.anyio
async def test_create_stop_loss_sell(client, client_id):
    stops_task = asyncio.create_task(client.get_stops(client_id=client_id))
    candles_task = asyncio.create_task(
        client.get_candles(
            security_board="TQBR",
            security_code="VTBR",
            time_frame="M1",
            count=1,
            to=datetime.now(),
        )
    )

    stops = await stops_task
    assert stops is not None
    amount = len(stops.stops)

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

    orders = await client.get_orders(
        client_id=client_id, include_matched=False, include_canceled=False
    )
    assert orders is not None
    order_ = next(iter(orders.orders), None)
    assert order_ is not None
    order_no = order_.order_no
    await asyncio.sleep(1)  # Чтобы успела обработаться информация о заявках.

    stop_act_price = round(price * 0.99, high_price_finam.scale)
    new_stop = await client.create_stop(
        client_id=client_id,
        security_board="TQBR",
        security_code="VTBR",
        buy_sell="BUY_SELL_SELL",
        link_order=order_no,
        stop_loss=StopLoss(
            activation_price=stop_act_price,
            market_price=True,
            quantity=StopQuantity(
                value=1, units=StopQuantityUnits.STOP_QUANTITY_UNITS_LOTS
            ),
            use_credit=True,
        ),
        valid_before=OrderValidBefore(
            type=OrderValidBeforeType.ORDER_VALID_BEFORE_TYPE_TILL_END_SESSION
        ),
    )
    assert new_stop is not None
    await asyncio.sleep(1)  # Чтобы успела обработаться информация о заявках.

    stops = await client.get_stops(client_id=client_id)
    assert stops is not None
    assert len(stops.stops) == amount + 1


@pytest.mark.anyio
async def test_create_stop_loss_buy(client, client_id):
    stops_task = asyncio.create_task(client.get_stops(client_id=client_id))
    candles_task = asyncio.create_task(
        client.get_candles(
            security_board="TQBR",
            security_code="VTBR",
            time_frame="M1",
            count=1,
            to=datetime.now(),
        )
    )

    stops = await stops_task
    assert stops is not None
    amount = len(stops.stops)

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

    orders = await client.get_orders(
        client_id=client_id, include_matched=False, include_canceled=False
    )
    assert orders is not None
    order_ = next(iter(orders.orders), None)
    assert order_ is not None
    order_no = order_.order_no
    await asyncio.sleep(1)  # Чтобы успела обработаться информация о заявках.

    stop_act_price = round(price * 1.01, high_price_finam.scale)
    new_stop = await client.create_stop(
        client_id=client_id,
        security_board="TQBR",
        security_code="VTBR",
        buy_sell="BUY_SELL_BUY",
        link_order=order_no,
        stop_loss=StopLoss(
            activation_price=stop_act_price,
            market_price=True,
            quantity=StopQuantity(
                value=1, units=StopQuantityUnits.STOP_QUANTITY_UNITS_LOTS
            ),
            use_credit=True,
        ),
        valid_before=OrderValidBefore(
            type=OrderValidBeforeType.ORDER_VALID_BEFORE_TYPE_TILL_END_SESSION
        ),
    )
    assert new_stop is not None
    await asyncio.sleep(1)  # Чтобы успела обработаться информация о заявках.

    stops = await client.get_stops(client_id=client_id)
    assert stops is not None
    assert len(stops.stops) == amount + 1


@pytest.mark.anyio
async def test_cancel_stop_order(client, client_id):
    stops_task = asyncio.create_task(
        client.get_stops(
            client_id=client_id, include_executed=False, include_canceled=False
        )
    )
    candles_task = asyncio.create_task(
        client.get_candles(
            security_board="TQBR",
            security_code="VTBR",
            time_frame="M1",
            count=1,
            to=datetime.now(),
        )
    )

    stops = await stops_task
    assert stops is not None
    amount = len(stops.stops)

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

    orders = await client.get_orders(
        client_id=client_id, include_matched=False, include_canceled=False
    )
    assert orders.orders
    amount_orders = len(orders.orders)
    order_ = next(iter(orders.orders), None)
    assert order_ is not None
    order_no = order_.order_no
    await asyncio.sleep(1)  # Чтобы успела обработаться информация о заявках.

    stop_act_price = round(price * 0.99, high_price_finam.scale)
    new_stop = await client.create_stop(
        client_id=client_id,
        security_board="TQBR",
        security_code="VTBR",
        buy_sell="BUY_SELL_SELL",
        link_order=order_no,
        stop_loss=StopLoss(
            activation_price=stop_act_price,
            market_price=True,
            quantity=StopQuantity(
                value=1, units=StopQuantityUnits.STOP_QUANTITY_UNITS_LOTS
            ),
            use_credit=True,
        ),
        valid_before=OrderValidBefore(
            type=OrderValidBeforeType.ORDER_VALID_BEFORE_TYPE_TILL_END_SESSION
        ),
    )
    assert new_stop is not None
    await asyncio.sleep(1)  # Чтобы успела обработаться информация о заявках.

    stops = await client.get_stops(
        client_id=client_id, include_executed=False, include_canceled=False
    )
    assert stops is not None
    assert len(stops.stops) == amount + 1
    await asyncio.sleep(1)  # Чтобы успела обработаться информация о заявках.

    stop_cancel = await client.cancel_stop(
        client_id=client_id, stop_id=new_stop.stop_id
    )
    assert stop_cancel is not None
    await asyncio.sleep(1)  # Чтобы успела обработаться информация о заявках.

    stops = await client.get_stops(
        client_id=client_id, include_executed=False, include_canceled=False
    )
    assert stops is not None
    assert len(stops.stops) == amount
    await asyncio.sleep(1)  # Чтобы успела обработаться информация о заявках.

    orders = await client.get_orders(
        client_id=client_id, include_matched=False, include_canceled=False
    )
    assert len(orders.orders) == amount_orders
    cancel_order = await client.cancel_order(
        client_id=client_id, transaction_id=new_order.transaction_id
    )
    assert cancel_order is not None


@pytest.mark.anyio
async def test_create_take_profit_sell(client, client_id):
    stops_task = asyncio.create_task(
        client.get_stops(
            client_id=client_id, include_executed=False, include_canceled=False
        )
    )
    candles_task = asyncio.create_task(
        client.get_candles(
            security_board="TQBR",
            security_code="VTBR",
            time_frame="M1",
            count=1,
            to=datetime.now(),
        )
    )

    stops = await stops_task
    assert stops is not None
    amount = len(stops.stops)

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

    orders = await client.get_orders(
        client_id=client_id, include_matched=False, include_canceled=False
    )
    assert orders is not None
    order_ = next(iter(orders.orders), None)
    assert order_ is not None
    order_no = order_.order_no
    await asyncio.sleep(1)  # Чтобы успела обработаться информация о заявках.

    take_act_price = round(price * 1.01, high_price_finam.scale)
    new_stop = await client.create_stop(
        client_id=client_id,
        security_board="TQBR",
        security_code="VTBR",
        buy_sell="BUY_SELL_SELL",
        link_order=order_no,
        take_profit=TakeProfit(
            activation_price=take_act_price,
            market_price=True,
            quantity=StopQuantity(
                value=1, units=StopQuantityUnits.STOP_QUANTITY_UNITS_LOTS
            ),
            use_credit=True,
        ),
        valid_before=OrderValidBefore(
            type=OrderValidBeforeType.ORDER_VALID_BEFORE_TYPE_TILL_END_SESSION
        ),
    )
    assert new_stop is not None
    await asyncio.sleep(1)  # Чтобы успела обработаться информация о заявках.

    stops = await client.get_stops(
        client_id=client_id, include_executed=False, include_canceled=False
    )
    assert stops is not None
    assert len(stops.stops) == amount + 1


@pytest.mark.anyio
async def test_create_take_profit_buy(client, client_id):
    stops_task = asyncio.create_task(
        client.get_stops(
            client_id=client_id, include_executed=False, include_canceled=False
        )
    )
    candles_task = asyncio.create_task(
        client.get_candles(
            security_board="TQBR",
            security_code="VTBR",
            time_frame="M1",
            count=1,
            to=datetime.now(),
        )
    )

    stops = await stops_task
    assert stops is not None
    amount = len(stops.stops)

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

    orders = await client.get_orders(
        client_id=client_id, include_matched=False, include_canceled=False
    )
    assert orders is not None
    order_ = next(iter(orders.orders), None)
    assert order_ is not None
    order_no = order_.order_no
    await asyncio.sleep(1)  # Чтобы успела обработаться информация о заявках.

    take_act_price = round(price * 0.99, high_price_finam.scale)
    new_stop = await client.create_stop(
        client_id=client_id,
        security_board="TQBR",
        security_code="VTBR",
        buy_sell="BUY_SELL_BUY",
        link_order=order_no,
        take_profit=TakeProfit(
            activation_price=take_act_price,
            market_price=True,
            quantity=StopQuantity(
                value=1, units=StopQuantityUnits.STOP_QUANTITY_UNITS_LOTS
            ),
            use_credit=True,
        ),
        valid_before=OrderValidBefore(
            type=OrderValidBeforeType.ORDER_VALID_BEFORE_TYPE_TILL_END_SESSION
        ),
    )
    assert new_stop is not None
    await asyncio.sleep(1)  # Чтобы успела обработаться информация о заявках.

    stops = await client.get_stops(
        client_id=client_id, include_executed=False, include_canceled=False
    )
    assert stops is not None
    assert len(stops.stops) == amount + 1


@pytest.mark.anyio
async def test_cancel_order_with_stop_order(client, client_id):
    stops_task = asyncio.create_task(
        client.get_stops(
            client_id=client_id, include_executed=False, include_canceled=False
        )
    )
    candles_task = asyncio.create_task(
        client.get_candles(
            security_board="TQBR",
            security_code="VTBR",
            time_frame="M1",
            count=1,
            to=datetime.now(),
        )
    )

    stops = await stops_task
    assert stops is not None
    amount = len(stops.stops)

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

    orders = await client.get_orders(
        client_id=client_id, include_matched=False, include_canceled=False
    )
    assert orders is not None
    amount_orders = len(orders.orders)
    order_ = next(iter(orders.orders), None)
    assert order_ is not None
    order_no = order_.order_no
    await asyncio.sleep(1)  # Чтобы успела обработаться информация о заявках.

    stop_act_price = round(price * 0.99, high_price_finam.scale)
    new_stop = await client.create_stop(
        client_id=client_id,
        security_board="TQBR",
        security_code="VTBR",
        buy_sell="BUY_SELL_SELL",
        link_order=order_no,
        stop_loss=StopLoss(
            activation_price=stop_act_price,
            market_price=True,
            quantity=StopQuantity(
                value=1, units=StopQuantityUnits.STOP_QUANTITY_UNITS_LOTS
            ),
            use_credit=True,
        ),
        valid_before=OrderValidBefore(
            type=OrderValidBeforeType.ORDER_VALID_BEFORE_TYPE_TILL_END_SESSION
        ),
    )
    assert new_stop is not None
    await asyncio.sleep(1)  # Чтобы успела обработаться информация о заявках.

    stops = await client.get_stops(
        client_id=client_id, include_executed=False, include_canceled=False
    )
    assert stops is not None
    assert len(stops.stops) == amount + 1
    await asyncio.sleep(1)  # Чтобы успела обработаться информация о заявках.

    orders = await client.get_orders(
        client_id=client_id, include_matched=False, include_canceled=False
    )
    assert len(orders.orders) == amount_orders
    cancel_order = await client.cancel_order(
        client_id=client_id, transaction_id=new_order.transaction_id
    )
    assert cancel_order is not None
    await asyncio.sleep(1)  # Чтобы успела обработаться информация о заявках.

    stops = await client.get_stops(
        client_id=client_id, include_executed=False, include_canceled=False
    )
    idx = [stop.stop_id for stop in stops.stops]
    # Стоп остается на месте, пока не будут сняты все ордера по инструменту.
    assert new_stop.stop_id in idx


@pytest.mark.anyio
async def test_cancel_all_stops(client, client_id):
    stops = await client.get_stops(
        client_id=client_id, include_executed=False, include_canceled=False
    )
    idx = [stop.stop_id for stop in stops.stops]
    tasks = []
    for id_ in idx:
        tasks.append(client.cancel_stop(client_id=client_id, stop_id=id_))
    results = await asyncio.gather(*tasks)
    for result in results:
        assert result is not None
        assert result.client_id == client_id
        assert result.stop_id in idx
    await asyncio.sleep(1)  # Чтобы успела обработаться информация о заявках.
    stops = await client.get_stops(
        client_id=client_id, include_executed=False, include_canceled=False
    )
    assert stops is not None
    assert len(stops.stops) == 0


@pytest.mark.anyio
async def test_cancel_all_orders(client, client_id):
    orders = await client.get_orders(
        client_id=client_id, include_matched=False, include_canceled=False
    )
    idx = [order.transaction_id for order in orders.orders]
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
    orders = await client.get_orders(
        client_id=client_id, include_matched=False, include_canceled=False
    )
    assert len(orders.orders) == 0
