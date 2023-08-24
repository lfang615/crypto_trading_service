from fastapi import FastAPI
from app.api.endpoints import auth, order, position
from app.core.logging import AsyncLogger
from app.db.services.redisservice import AsyncRedisService

app = FastAPI()


app.include_router(auth.router, prefix="/auth", tags=["authentication"])
app.include_router(order.router, prefix="/order", tags=["orders"])
app.include_router(position.router, prefix="/position", tags=["positions"])

@app.on_event("startup")
async def startup_event():
    logger_instance = AsyncLogger()    
    logger_instance.info("Starting up the application...")

    await AsyncRedisService().get_connection()
    

@app.on_event("shutdown")
async def shutdown_event():
    AsyncLogger().info("Shutting down the application...")
    await AsyncRedisService.close()