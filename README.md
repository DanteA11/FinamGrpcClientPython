# finam-grpc-client
Клиенты для взаимодействия с [GRPC API Finam](https://tradeapi.finam.ru/docs/about/).

---
## Требования
Python >= 3.12

---
## Зависимости
Установить зависимости можно через [poetry](https://python-poetry.org/docs/) или pip:
```shell
  poetry install --without test,dev
```
```shell
  pip install -r requirements.txt
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

from finam_grpc_client import FinamSyncClient

token = "Токен авторизации"

def on_order_book(event):
    print(event)

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
        time.sleep(5)
        print("Завершено")

        
if __name__ == "__main__":
    main()
```
Асинхронно
```python
import asyncio

from finam_grpc_client import FinamAsyncClient

token = "Токен авторизации"

async def on_order_book(event):
    print(event)

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
        await asyncio.sleep(5)
        print("Завершено")

        
if __name__ == "__main__":
    asyncio.run(main())
```