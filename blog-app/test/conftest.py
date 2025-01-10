import typing
import pytest_asyncio, pytest
from databases import Database
from fastapi.testclient import TestClient
from database import get_database
from settings import get_settings

from main import app
from scripts.create_table import create_table

client = TestClient(app)
setting = get_settings()


class TestDababase(Database):
    def __init__(self, url, *, force_rollback=False, **options):
        super().__init__(url, force_rollback=force_rollback, **options)


@pytest_asyncio.fixture(
    scope="session",
)
async def test_db() -> typing.AsyncGenerator[TestDababase, None]:
    async with TestDababase(setting.test_database_url) as db:

        async def get_test_database() -> typing.AsyncGenerator[TestDababase, None]:
            yield db

        app.dependency_overrides[get_database] = get_test_database
        yield db


@pytest_asyncio.fixture(scope="function", autouse=True)
async def scope_function(test_db):
    await create_table(test_db)
    yield


client = TestClient(app)


@pytest.fixture
def test_client():
    return client
