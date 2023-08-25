from fastapi import APIRouter, Body, Depends
from fastapi.responses import JSONResponse
from app.db.models import UserInDB, PlaceOrderBase, OrderStatus, ExchangeCredentials, OrderStructure
from app.exchanges.integrations import AbstractExchange
from app.dependencies import get_exchange_credentials, get_current_user, has_open_position, is_tpsl_order_type

router = APIRouter()

@router.post("/close_position/", response_model=OrderStructure)
async def close_position(order: PlaceOrderBase = Body(...),
                        current_user: UserInDB = Depends(get_current_user),                      
                        exchange_credentials: ExchangeCredentials = Depends(get_exchange_credentials),
                        has_open_position: bool = Depends(has_open_position)):
    
    exchange_name = order.exchange.value
    exchange: AbstractExchange = AbstractExchange.create(exchange_name, exchange_credentials.api_key, exchange_credentials.api_secret)

    # 2. Place the order using the exchange's implementation
    order_response = await exchange.place_order(order)
    return JSONResponse(status_code=200, content={"status": OrderStatus.CLOSED})


@router.post("/tpsl_order/", response_model=OrderStructure)
async def take_profit_stop_loss(order: PlaceOrderBase = Body(...),
                                current_user: UserInDB = Depends(get_current_user),                      
                                exchange_credentials: ExchangeCredentials = Depends(get_exchange_credentials),
                                has_open_position: bool = Depends(has_open_position),
                                is_tpsl_order_type: bool = Depends(is_tpsl_order_type)):
    
    exchange_name = order.exchange.value
    exchange: AbstractExchange = AbstractExchange.create(exchange_name, exchange_credentials.api_key, exchange_credentials.api_secret)

    # 2. Place the order using the exchange's implementation
    order_response = await exchange.place_order(order)
    return JSONResponse(status_code=200, content={"status": OrderStatus.OPEN})