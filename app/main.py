from fastapi import FastAPI
from app.api.endpoints import auth, order
from app.core.logging import AsyncLogger
from app.db.services.redisservice import AsyncRedisService

app = FastAPI()


app.include_router(auth.router, prefix="/auth", tags=["authentication"])
app.include_router(order.router, prefix="/order", tags=["orders"])

@app.on_event("startup")
async def startup_event():
    logger_instance = AsyncLogger()    
    logger_instance.info("Starting up the application...")

    global async_redis_service
    async_redis_service = AsyncRedisService()
    await async_redis_service.initialize()

@app.on_event("shutdown")
async def shutdown_event():
    AsyncLogger().info("Shutting down the application...")
    await async_redis_service.close()