import asyncio
import pytest

from tests.conftest import client
from httpx import AsyncClient


# async def test_runs_in_asyncio_event_loop():
#     assert asyncio.get_running_loop()


def test_create_user():
    response = client.post("/users/", json={"email": "user@example.com", "password": "123"})
    assert response.status_code == 200


# @pytest.mark.asyncio
async def test_get_users(async_client: AsyncClient):
    response = await async_client.get("/users/")
    assert response.status_code == 200
    assert response.json() == []