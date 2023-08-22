from httpx import AsyncClient
from .conftest import client, limit_order, test_user_token, mock_get_user
from app.db.models import PlaceOrderBase
import pytest
import json

@pytest.mark.asyncio
async def test_place_order_unauthenticated(client: AsyncClient, limit_order: json):
    response = await client.post(url="/order/place_order/", json=json.dumps(limit_order))  # Replace '...' with your test data
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_place_order_authenticated(client: AsyncClient, test_user_token: str, mock_get_user, limit_order: json):
    headers = {"Authorization": f"Bearer {test_user_token}"}
    response = await client.post("/order/place_order/", data=json.dumps(limit_order), headers=headers)
    print(response.json())
    assert response.status_code == 200  # Or whatever status code you expect for a successful order placement
