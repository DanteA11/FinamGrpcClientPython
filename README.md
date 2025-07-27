# finam-grpc-client
Клиенты для взаимодействия с [GRPC API Finam](https://tradeapi.finam.ru/docs/about/).

---
## Требования
Python >= 3.12

---
## Зависимости
В директории dist находятся дистрибутивы, которые можно установить, используя ваш пакетный менеджер:
```shell
  poetry add FinamGrpcClientPython/dist/finam_grpc_client-3.2.0.tar.gz
```
```shell
  pip install FinamGrpcClientPython/dist/finam_grpc_client-3.2.0.tar.gz
```
___
## Использование
### Получение исторических баров:
Синхронно
```python
import datetime

from finam_grpc_client import FinamSyncClient
from finam_grpc_client.types import TimeFrame

token = "Токен авторизации"

def main():
    with FinamSyncClient(token=token) as client:
        symbol = "VTBR@MISX"
        to_ = datetime.datetime.now()
        from_ = to_ - datetime.timedelta(days=5)
        bars = client.get_bars(symbol, TimeFrame.TIME_FRAME_D, from_, to_)
        print(bars)

        
if __name__ == "__main__":
    main()
```
Асинхронно
```python
import datetime
import asyncio

from finam_grpc_client import FinamAsyncClient
from finam_grpc_client.types import TimeFrame

token = "Токен авторизации"

async def main():
    async with FinamAsyncClient(token=token) as client:
        symbol = "VTBR@MISX"
        to_ = datetime.datetime.now()
        from_ = to_ - datetime.timedelta(days=5)
        bars = await client.get_bars(symbol, TimeFrame.TIME_FRAME_D, from_, to_)
        print(bars)

if __name__ == "__main__":
    asyncio.run(main())
```
### Выставление заявки:
Синхронно
```python
from google.type.decimal_pb2 import Decimal

from finam_grpc_client import FinamSyncClient
from finam_grpc_client.types import Side, OrderType, TimeInForce

token = "Токен авторизации"
account_id = "Идентификатор аккаунта"

def main():
    with FinamSyncClient(token=token) as client:
        symbol = "VTBR@MISX"
        price = Decimal(value="Цена")
        # Выставляем
        place = client.place_order(
            account_id,
            symbol,
            quantity=Decimal(value="1"),
            side=Side.SIDE_BUY,
            type=OrderType.ORDER_TYPE_LIMIT,
            time_in_force=TimeInForce.TIME_IN_FORCE_DAY,
            limit_price=price,
            stop_price=None,
            stop_condition=None,
            legs=None,
            client_order_id=None,
        )
        print(place)
        # Отменяем
        cancel = client.cancel_order(account_id, place.order_id)
        print(cancel)

        
if __name__ == "__main__":
    main()
```
Асинхронно
```python
import asyncio

from google.type.decimal_pb2 import Decimal

from finam_grpc_client import FinamAsyncClient
from finam_grpc_client.types import Side, OrderType, TimeInForce

token = "Токен авторизации"
account_id = "Идентификатор аккаунта"

async def main():
    async with FinamAsyncClient(token=token) as client:
        symbol = "VTBR@MISX"
        price = Decimal(value="Цена")
        # Выставляем
        place = await client.place_order(
            account_id,
            symbol,
            quantity=Decimal(value="1"),
            side=Side.SIDE_BUY,
            type=OrderType.ORDER_TYPE_LIMIT,
            time_in_force=TimeInForce.TIME_IN_FORCE_DAY,
            limit_price=price,
            stop_price=None,
            stop_condition=None,
            legs=None,
            client_order_id=None,
        )
        print(place)
        # Отменяем
        cancel = await client.cancel_order(account_id, place.order_id)
        print(cancel)

if __name__ == "__main__":
    asyncio.run(main())
```
### Подписка на стакан:
Синхронно
```python
import time
import logging

from finam_grpc_client import FinamSyncClient

token = "Токен авторизации"

def on_order_book(event):
    logging.warning(event)

def main():
    with FinamSyncClient(token=token) as client:
        symbol = "VTBR@MISX"
        # Назначаем обработчик
        client.on_order_book = on_order_book
        # Оформляем подписку
        client.subscribe_order_book(symbol)
        time.sleep(10)
        # Отменяем подписку
        client.unsubscribe_order_book(symbol)
        logging.warning("Отмена подписки")
        time.sleep(5)
        logging.warning("Завершено")

        
if __name__ == "__main__":
    main()
```
Асинхронно
```python
import asyncio
import logging

from finam_grpc_client import FinamAsyncClient

token = "Токен авторизации"

async def on_order_book(event):
    logging.warning(event)

async def main():
    async with FinamAsyncClient(token=token) as client:
        symbol = "VTBR@MISX"
        # Назначаем обработчик
        client.on_order_book = on_order_book
        # Оформляем подписку
        await client.subscribe_order_book(symbol)
        await asyncio.sleep(10)
        # Отменяем подписку
        await client.unsubscribe_order_book(symbol)
        logging.warning("Отмена подписки")
        await asyncio.sleep(5)
        logging.warning("Завершено")

        
if __name__ == "__main__":
    asyncio.run(main())
```