from fastapi import APIRouter, Depends
from app.auth.jwt import get_current_user
from app.db.models import User, PlaceOrderBase, OrderStatus
from app.exchanges.integrations import AbstractExchange

router = APIRouter()

@router.post("/place_order/", response_model=OrderStatus)
async def place_order(order: PlaceOrderBase, current_user: User = Depends(get_current_user)):
    # 1. Determine the exchange to use. 
    # This can be from `order.exchangeSpecificParams` or another dedicated field.
    exchange_name = order.exchangeSpecificParams.get("exchange", "default_exchange_name")
    exchange: AbstractExchange = AbstractExchange.create(exchange_name, current_user.api_key, current_user.api_secret)

    # 2. Place the order using the exchange's implementation
    order_response = exchange.place_order(order)

    # 3. Return the order status. This can be further detailed depending on the exchange's response.
    return order_response["status"]