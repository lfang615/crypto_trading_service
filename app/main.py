from fastapi import FastAPI
from app.api.endpoints import auth, order
from app.core.logging import AsyncLogger

app = FastAPI()

logger_instance: ArithmeticError = None

app.include_router(auth.router, prefix="/auth", tags=["authentication"])
app.include_router(order.router, prefix="/order", tags=["orders"])

@app.on_event("startup")
async def startup_event():
    global logger_instance
    logger_instance = AsyncLogger().get_logger(__name__)
    logger_instance.info("Starting up the application...")

@app.on_event("shutdown")
async def shutdown_event():    
    pass