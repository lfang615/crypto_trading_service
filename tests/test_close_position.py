import pytest
from httpx import AsyncClient
from .conftest import client, mock_redis_no_position, mock_redis_with_position, test_user_token, \
mock_get_user, mock_bitget_close_position_order, mock_bitget_place_order_response
from app.db.models import OrderStructure, PlaceOrderBase
import json

@pytest.mark.asyncio
async def test_close_position_no_open_position(client: AsyncClient, mock_get_user, test_user_token:str, mock_bitget_close_position_order: json, mock_redis_no_position: json):
    headers = {"Authorization": f"Bearer {test_user_token}"} 
    response = await client.post("/position/close_position/", json=mock_bitget_close_position_order, headers=headers)
    assert response.status_code == 400
    assert response.json() == {"detail": "No open position for the given symbol."}

@pytest.mark.asyncio
async def test_close_position_with_open_position(client: AsyncClient, test_user_token:str, mock_get_user, mock_bitget_close_position_order: json, mock_bitget_place_order_response: OrderStructure, mock_redis_with_position: json):
    headers = {"Authorization": f"Bearer {test_user_token}"} 
    
    response = await client.post("/position/close_position/", json=mock_bitget_close_position_order, headers=headers)
    assert response.status_code == 200
    # Add more assertions based on the successful response's expected structure

@pytest.mark.asyncio
async def test_close_position_unauthenticated(client: AsyncClient, mock_redis_with_position: json, mock_get_user, mock_bitget_close_position_order: json, mock_bitget_place_order_response: OrderStructure):
    
    response = await client.post("/position/close_position/", json=mock_bitget_close_position_order)
    assert response.status_code == 401    

