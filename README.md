# finam-grpc-client
Синхронный и асинхронный клиенты для взаимодействия с [GRPC API Finam](https://tradeapi.finam.ru/docs/about/).

Представляют собой обертку над методами GRPC с автоматическим обновлением токена сессии.
___
## Требования
Python >= 3.12
___
## Установка:
`pip install git+https://github.com/DanteA11/FinamGrpcClientPython.git`
___
## Использование
### Синхронно:
**Запросы:**
```python
from finam_grpc_client import FinamClient
from finam_grpc_client.proto.grpc.tradeapi.v1.assets.assets_service_pb2 import (
    ClockRequest,
)

secret = "Ваш токен"


def main():
    with FinamClient(secret=secret) as client:
        clock = client.clock(request=ClockRequest())
        print(clock)

            
if __name__ == "__main__":
    main()
```
**Стримы:**
```python
from finam_grpc_client import FinamClient
from finam_grpc_client.proto.grpc.tradeapi.v1.marketdata.marketdata_service_pb2 import (
    SubscribeQuoteRequest,
)

secret = "Ваш токен"


def main():
    with FinamClient(secret=secret) as client:
        for e in client.subscribe_quote(
                request=SubscribeQuoteRequest(symbols=("YDEX@MISX",))
        ):
            print(e)


if __name__ == "__main__":
    main()
```
### Асинхронно:
**Запросы:**
```python
import asyncio

from finam_grpc_client.asyncio import FinamClient
from finam_grpc_client.proto.grpc.tradeapi.v1.assets.assets_service_pb2 import (
    ClockRequest,
)

secret = "Ваш токен"


async def main():
    async with FinamClient(secret=secret) as client:
        clock = await client.clock(request=ClockRequest())
        print(clock)

            
if __name__ == "__main__":
    asyncio.run(main())
```
**Стримы:**
```python
import asyncio

from finam_grpc_client.asyncio import FinamClient
from finam_grpc_client.proto.grpc.tradeapi.v1.marketdata.marketdata_service_pb2 import (
    SubscribeQuoteRequest,
)

secret = "Ваш токен"


async def main():
    async with FinamClient(secret=secret) as client:
        async for e in client.subscribe_quote(
            request=SubscribeQuoteRequest(symbols=("YDEX@MISX",))
        ):
            print(e)

            
if __name__ == "__main__":
    asyncio.run(main())
```