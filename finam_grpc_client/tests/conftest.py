import pytest

from finam_grpc_client.clients import FinamGrpcClient

token = ""
c_id = ""
test_trades = False  # Запускать тесты с открытием сделок.

if not token or not c_id:
    pytest.exit(
        "Не установлен token или client_id. Установите их в файле conftest.py"
    )


@pytest.fixture(scope="session")
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture(scope="session")
async def client():
    async with FinamGrpcClient(token) as client:
        yield client


@pytest.fixture(scope="session")
async def client_id():
    return c_id
