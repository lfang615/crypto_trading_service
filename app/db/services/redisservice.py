import aioredis
from app.core import config
from app.core.logging import AsyncLogger

class AsyncRedisService:
    def __init__(self):
        self.redis = None
        self.logger = AsyncLogger("RedisWrapper").get_logger()

    async def initialize(self):
        try:
            self.redis = await aioredis.create_redis_pool("redis://localhost")  # Adjust this according to your Redis setup
            self.logger.info("Successfully initialized Redis connection.")
        except Exception as e:
            self.logger.error(f"Error initializing Redis: {str(e)}")

    async def close(self):
        try:
            if self.redis:
                self.redis.close()
                await self.redis.wait_closed()
                self.logger.info("Successfully closed Redis connection.")
        except Exception as e:
            self.logger.error(f"Error closing Redis connection: {str(e)}")

    def _format_key(self, exchange: str, symbol: str, side: str) -> str:
        return config.CACHE_KEY_FORMAT.format(exchange=exchange, symbol=symbol, side=side)

    async def set_position(self, exchange: str, symbol: str, side: str, data: dict):
        key = self._format_key(exchange, symbol, side)
        try:
            await self.redis.set(key, data)
            self.logger.info(f"Successfully set position for key: {key}")
        except Exception as e:
            self.logger.error(f"Error setting position for key {key}: {str(e)}")

    async def get_position(self, exchange: str, symbol: str, side: str) -> dict:
        key = self._format_key(exchange, symbol, side)
        try:
            data = await self.redis.get(key)
            self.logger.info(f"Successfully retrieved position for key: {key}")
            return data
        except Exception as e:
            self.logger.error(f"Error retrieving position for key {key}: {str(e)}")
            return None