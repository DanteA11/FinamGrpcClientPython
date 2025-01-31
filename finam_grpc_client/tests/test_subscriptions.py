import asyncio
from datetime import datetime

import pytest

from finam_grpc_client.models.proto.candles_pb2 import GetIntradayCandlesResult
from finam_grpc_client.models.proto.common_pb2 import BuySell, ResponseEvent
from finam_grpc_client.models.proto.events_pb2 import (
    OrderBookEvent,
    OrderEvent,
    TradeEvent,
)
from finam_grpc_client.models.proto.orders_pb2 import (
    OrderCondition,
    OrderStatus,
)
from finam_grpc_client.tests.conftest import test_trades


@pytest.mark.anyio
async def test_order_book_one_subscribe_unsubscribe(client):
    events_order_book: list[OrderBookEvent] = []
    events_response: list[ResponseEvent] = []

    async def handler_order_book(event: OrderBookEvent):
        events_order_book.append(event)

    async def handler_response(event: ResponseEvent):
        if event.request_id != "keep_alive":
            events_response.append(event)

    client.on_order_book = handler_order_book
    client.on_response = handler_response

    security_board = "TQBR"
    security_code = "VTBR"
    request_id = "test_1"

    await client.subscribe_order_book(
        request_id=request_id,
        security_board=security_board,
        security_code=security_code,
    )
    for i in range(6):
        if events_response:
            break
        await asyncio.sleep(1)
    else:
        assert False
    assert len(events_response) == 1

    for r in events_response:
        assert r.request_id == request_id
        assert r.success is True
    await asyncio.sleep(5)

    assert len(events_response) == 1  # еще раз проверяю.
    assert len(events_order_book) > 0
    for e in events_order_book:
        assert e.security_board == security_board
        assert e.security_code == security_code
        assert isinstance(e.bids[0].price, float)

    await client.unsubscribe_book(
        request_id=request_id,
        security_board=security_board,
        security_code=security_code,
    )

    for i in range(6):
        if len(events_response) == 2:
            break
        await asyncio.sleep(1)
    else:
        assert len(events_response) == 2

    for r in events_response:
        assert r.request_id == request_id
        assert r.success is True

    events_order_book.clear()
    await asyncio.sleep(3)
    assert len(events_order_book) == 0


@pytest.mark.anyio
async def test_order_book_several_subscribe_unsubscribe(client):
    events_order_book: list[OrderBookEvent] = []
    events_response: list[ResponseEvent] = []

    async def handler_order_book(event: OrderBookEvent):
        events_order_book.append(event)

    async def handler_response(event: ResponseEvent):
        if event.request_id != "keep_alive":
            events_response.append(event)

    client.on_order_book = handler_order_book
    client.on_response = handler_response

    security_board = "TQBR"
    security_code = "VTBR"
    request_id = "test_2_vtb"

    security_code_1 = "SBER"
    request_id_1 = "test_2_sber"

    await asyncio.gather(
        client.subscribe_order_book(
            request_id=request_id,
            security_board=security_board,
            security_code=security_code,
        ),
        client.subscribe_order_book(
            request_id=request_id_1,
            security_board=security_board,
            security_code=security_code_1,
        ),
    )
    for i in range(6):
        if len(events_response) == 2:
            break
        await asyncio.sleep(1)
    else:
        assert len(events_response) == 2

    check_vtb = False
    check_sber = False
    for r in events_response:
        if r.request_id == request_id:
            check_vtb = True
        elif r.request_id == request_id_1:
            check_sber = True
        assert r.success is True
    assert check_vtb
    assert check_sber
    await asyncio.sleep(5)

    assert len(events_response) == 2  # еще раз проверяю.
    assert len(events_order_book) > 0
    check_vtb = False
    check_sber = False
    for e in events_order_book:
        assert e.security_board == security_board
        if e.security_code == security_code:
            check_vtb = True
        elif e.security_code == security_code_1:
            check_sber = True
        assert isinstance(e.bids[0].price, float)
    assert check_vtb
    assert check_sber

    await asyncio.gather(
        client.unsubscribe_book(
            request_id=request_id,
            security_board=security_board,
            security_code=security_code,
        ),
        client.unsubscribe_book(
            request_id=request_id_1,
            security_board=security_board,
            security_code=security_code_1,
        ),
    )

    for i in range(6):
        if len(events_response) == 4:
            break
        await asyncio.sleep(1)
    else:
        assert len(events_response) == 4

    check_vtb = False
    check_sber = False
    for r in events_response[-2:]:
        if r.request_id == request_id:
            check_vtb = True
        elif r.request_id == request_id_1:
            check_sber = True
        assert r.success is True
    assert check_vtb
    assert check_sber
    events_order_book.clear()
    await asyncio.sleep(5)

    assert len(events_order_book) == 0


@pytest.mark.anyio
async def test_orders_subscribe_unsubscribe(client, client_id):
    events_order: list[OrderEvent] = []
    events_response: list[ResponseEvent] = []

    async def handler_order(event: OrderEvent):
        events_order.append(event)

    async def handler_response(event: ResponseEvent):
        if event.request_id != "keep_alive":
            events_response.append(event)

    client.on_order = handler_order
    client.on_response = handler_response

    request_id = "test_3"

    await client.subscribe_orders_trades(
        request_id=request_id, client_ids=[client_id]
    )

    for _ in range(6):
        if events_response:
            break
        await asyncio.sleep(1)
    else:
        assert False
    assert len(events_response) == 1

    for r in events_response:
        assert r.request_id == request_id
        assert r.success is True

    candles = await client.get_candles(
        security_board="TQBR",
        security_code="VTBR",
        time_frame="M1",
        count=1,
        to=datetime.now(),
    )

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

    for _ in range(6):
        if len(events_order) == 3:  # приходит три уведомления.
            break
        await asyncio.sleep(1)
    else:
        assert len(events_order) == 3

    checks = [False, False, False]
    for i, o in enumerate(events_order):
        assert o.transaction_id == new_order.transaction_id
        match o.status:
            case OrderStatus.ORDER_STATUS_NONE:
                checks[i] = True
            case OrderStatus.ORDER_STATUS_ACTIVE:
                checks[i] = True
            case OrderStatus.ORDER_STATUS_ACTIVE if isinstance(
                o.order_no, int
            ):
                checks[i] = True
    assert all(checks)
    events_order.clear()

    await client.cancel_order(
        client_id=client_id, transaction_id=new_order.transaction_id
    )
    for _ in range(6):
        if len(events_order) == 2:  # приходит два уведомления.
            break
        await asyncio.sleep(1)
    else:
        assert len(events_order) == 2

    for o in events_order:
        assert o.transaction_id == new_order.transaction_id
        assert o.status == OrderStatus.ORDER_STATUS_CANCELLED

    await client.unsubscribe_orders_trades(request_id=request_id)

    for i in range(6):
        if len(events_response) == 2:
            break
        await asyncio.sleep(1)
    else:
        assert len(events_response) == 2

    for r in events_response:
        assert r.request_id == request_id
        assert r.success is True


@pytest.mark.skipif(
    test_trades is False, reason="Пропуск тестов с открытием сделок."
)
@pytest.mark.anyio
async def test_orders_trades_subscribe_unsubscribe(client, client_id):
    events_order: list[OrderEvent] = []
    events_response: list[ResponseEvent] = []
    events_trade: list[TradeEvent] = []

    async def handler_order(event: OrderEvent):
        events_order.append(event)

    async def handler_trade(event: TradeEvent):
        events_trade.append(event)

    async def handler_response(event: ResponseEvent):
        if event.request_id != "keep_alive":
            events_response.append(event)

    client.on_order = handler_order
    client.on_response = handler_response
    client.on_trade = handler_trade

    request_id = "test_4"
    security_code = "VTBR"

    await client.subscribe_orders_trades(
        request_id=request_id, client_ids=[client_id]
    )

    for _ in range(6):
        if events_response:
            break
        await asyncio.sleep(1)
    else:
        assert False
    assert len(events_response) == 1

    for r in events_response:
        assert r.request_id == request_id
        assert r.success is True

    open_order = await client.create_order(  # По рынку.
        client_id=client_id,
        security_board="TQBR",
        security_code=security_code,
        buy_sell="BUY_SELL_BUY",
        quantity=1,
        price=None,
    )
    assert open_order is not None
    assert open_order.client_id == client_id

    for _ in range(6):
        if len(events_order) == 3:  # приходит три уведомления.
            break
        await asyncio.sleep(1)
    else:
        assert len(events_order) == 3

    checks = [False, False, False]
    for i, o in enumerate(events_order):
        assert o.transaction_id == open_order.transaction_id
        match o.status:
            case OrderStatus.ORDER_STATUS_NONE:
                checks[i] = True
            case OrderStatus.ORDER_STATUS_ACTIVE:
                checks[i] = True
            case OrderStatus.ORDER_STATUS_MATCHED if isinstance(
                o.order_no, int
            ):
                checks[i] = True
    assert all(checks)

    order_no = events_order[-1].order_no
    events_order.clear()

    for _ in range(3):
        if len(events_trade) == 1:
            break
        await asyncio.sleep(1)
    else:
        assert len(events_trade) == 1

    for t in events_trade:
        assert t.order_no == order_no
        assert t.security_code == security_code
        assert t.buy_sell == BuySell.BUY_SELL_BUY
    events_trade.clear()

    close_order = await client.create_order(  # Закрываем по рынку.
        client_id=client_id,
        security_board="TQBR",
        security_code=security_code,
        buy_sell="BUY_SELL_SELL",
        quantity=1,
        price=None,
    )
    assert close_order is not None
    assert close_order.client_id == client_id

    for _ in range(6):
        if len(events_order) == 3:  # приходит три уведомления.
            break
        await asyncio.sleep(1)
    else:
        assert len(events_order) == 3

    checks = [False, False, False]
    for i, o in enumerate(events_order):
        assert o.transaction_id == close_order.transaction_id
        match o.status:
            case OrderStatus.ORDER_STATUS_NONE:
                checks[i] = True
            case OrderStatus.ORDER_STATUS_ACTIVE:
                checks[i] = True
            case OrderStatus.ORDER_STATUS_MATCHED if isinstance(
                o.order_no, int
            ):
                checks[i] = True
    assert all(checks)

    order_no = events_order[-1].order_no

    for _ in range(3):
        if len(events_trade) == 1:
            break
        await asyncio.sleep(1)
    else:
        assert len(events_trade) == 1

    for t in events_trade:
        assert t.order_no == order_no
        assert t.security_code == security_code
        assert t.buy_sell == BuySell.BUY_SELL_SELL

    await client.unsubscribe_orders_trades(request_id=request_id)

    for i in range(6):
        if len(events_response) == 2:
            break
        await asyncio.sleep(1)
    else:
        assert len(events_response) == 2

    for r in events_response:
        assert r.request_id == request_id
        assert r.success is True
