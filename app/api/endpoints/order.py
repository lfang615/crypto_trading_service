from fastapi import APIRouter, Body, Depends
from fastapi.responses import JSONResponse
from app.db.models import PlaceOrderBase, OrderStatus, ExchangeCredentials, OrderStructure
from app.db.repositories.orderrepository import OrderRepository
from app.exchanges.integrations import AbstractExchange
from app.dependencies import get_exchange_credentials, get_order_repository
from app.db.services.kafkaproducer import KafkaProducer

router = APIRouter()

@router.post("/place_order/", response_model=OrderStructure)
async def place_order(order: PlaceOrderBase = Body(...),                      
                      exchange_credentials: ExchangeCredentials = Depends(get_exchange_credentials),
                      order_repository: OrderRepository = Depends(get_order_repository)):
    # 1. Determine the exchange to use. 
    # This can be from `order.exchangeSpecificParams` or another dedicated field.
    exchange_name = order.exchange.value
    exchange: AbstractExchange = AbstractExchange.create(exchange_name, exchange_credentials.api_key, exchange_credentials.api_secret)

    # 2. Place the order using the exchange's implementation
    order_response = await exchange.place_order(order)
    order_id = order_response.id
    client_oid = order_response.clientOrderId
    if order_id and client_oid:
        # 2.1. Store the order in the database
        order_repository.create(OrderStructure(clientOrderId=client_oid, id=order_id))
        # 2.2. Produce the order to the Kafka topic        
        await KafkaProducer().send_order("orders_submitted", order_id, client_oid)
        return JSONResponse(status_code=200, content={"status": OrderStatus.OPEN})
    else:
        return JSONResponse(status_code=400, content={"message": 'Order could not be placed.'})