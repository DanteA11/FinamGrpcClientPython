import pytest

from finam_grpc_client import FinamAsyncClient, FinamSyncClient

token = ""
acc_id = ""

if not token or not acc_id:
    pytest.exit(
        "Не установлен token или acc_id. Установите их в файле conftest.py"
    )


@pytest.fixture(scope="session")
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture(scope="session")
async def async_client():
    async with FinamAsyncClient(token) as client:
        yield client


@pytest.fixture(scope="session")
def sync_client():
    with FinamSyncClient(token) as client:
        yield client


@pytest.fixture
def account_id():
    return acc_id
