from fastapi import FastAPI
from app.api.endpoints import auth, order
from app.core.logging import AsyncLogger

app = FastAPI()


app.include_router(auth.router, prefix="/auth", tags=["authentication"])
app.include_router(order.router, prefix="/order", tags=["orders"])

@app.on_event("startup")
async def startup_event():
    logger_instance = AsyncLogger()    
    logger_instance.info("Starting up the application...")

@app.on_event("shutdown")
async def shutdown_event():
    AsyncLogger().info("Shutting down the application...")