import os
import pathlib

import pytest
from dotenv import load_dotenv

from finam_grpc_client import FinamAsyncClient, FinamSyncClient

load_dotenv(pathlib.Path(__file__).parent.parent.parent.joinpath(".env"))
token = os.getenv("TOKEN")
acc_id = os.getenv("ACCOUNT_ID")


@pytest.fixture(scope="session")
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture(scope="session")
async def async_client():
    x = FinamAsyncClient(token)
    async with FinamAsyncClient(token) as client:
        yield client


@pytest.fixture(scope="session")
def sync_client():
    with FinamSyncClient(token) as client:
        yield client


@pytest.fixture()
async def async_client_new():
    async with FinamAsyncClient(token) as client:
        yield client


@pytest.fixture()
def sync_client_new():
    with FinamSyncClient(token) as client:
        yield client


@pytest.fixture
def account_id():
    return acc_id
