from fastapi import APIRouter, Body, Depends
from fastapi.responses import JSONResponse
from app.db.models import User, PlaceOrderBase, OrderStatus, ExchangeCredentials, OrderStructure
from app.exchanges.integrations import AbstractExchange
from app.dependencies import get_exchange_credentials, get_current_user

router = APIRouter()

@router.post("/place_order/", response_model=OrderStructure)
async def place_order(order: PlaceOrderBase = Body(...),                      
                      exchange_credentials: ExchangeCredentials = Depends(get_exchange_credentials)):
    # 1. Determine the exchange to use. 
    # This can be from `order.exchangeSpecificParams` or another dedicated field.
    exchange_name = order.exchange.value
    exchange: AbstractExchange = AbstractExchange.create(exchange_name, exchange_credentials.api_key, exchange_credentials.api_secret)

    # 2. Place the order using the exchange's implementation
    order_response = await exchange.place_order(order)

    # 3. Return the order status. This can be further detailed depending on the exchange's response.
    return JSONResponse(status_code=200, content={"status": OrderStatus.OPEN})