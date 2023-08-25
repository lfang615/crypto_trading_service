import pytest
from httpx import AsyncClient
from .conftest import client, mock_redis_no_position, mock_redis_with_position, test_user_token, \
mock_get_user, mock_bitget_tpsl_order, mock_bitget_place_order_response, mock_bitget_close_position_order
from app.db.models import OrderStructure, OrderType
import json

@pytest.mark.asyncio
async def test_tpsl_no_open_position(client: AsyncClient, mock_get_user, test_user_token:str, mock_bitget_tpsl_order: json, mock_redis_no_position: json):
    headers = {"Authorization": f"Bearer {test_user_token}"} 
    response = await client.post("/position/tpsl_order/", json=mock_bitget_tpsl_order, headers=headers)
    assert response.status_code == 400
    assert response.json() == {"detail": "No open position for the given symbol."}

@pytest.mark.asyncio
async def test_tpsl_with_open_position(client: AsyncClient, test_user_token:str, mock_get_user, mock_bitget_tpsl_order: json, mock_bitget_place_order_response: OrderStructure, mock_redis_with_position: json):
    headers = {"Authorization": f"Bearer {test_user_token}"} 
    response = await client.post("/position/tpsl_order/", json=mock_bitget_tpsl_order, headers=headers)
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_tpsl_incorrect_order_type(client: AsyncClient, test_user_token:str, mock_get_user, mock_bitget_close_position_order: json, mock_bitget_place_order_response: OrderStructure, mock_redis_with_position: json):
    headers = {"Authorization": f"Bearer {test_user_token}"}     
    response = await client.post("/position/tpsl_order/", json=mock_bitget_close_position_order, headers=headers)
    assert response.status_code == 400
    assert response.json() == {"detail": "Order type is not a TP/SL order"}

