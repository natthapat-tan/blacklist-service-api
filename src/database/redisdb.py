import json
import logging
import os
import redis.asyncio as redis
from redis.exceptions import RedisError
from typing import Any, Dict, Optional

from src.config import get_env

logger = logging.getLogger(__name__)
env = get_env()


class RedisConnector:

    client: Optional[redis.Redis] = None

    async def connect_to_redis(self, host: str, port: str, db: str, password: str):
        logger.info("Connecting to Redis ...")
        try:

            pool = redis.ConnectionPool(host = host,
                                        port = port,
                                        password = password,
                                        db = db,
                                        max_connections = 20,         # 20 workers concurrently
                                        health_check_interval = 30,   # auto-remove dead connections
                                        socket_timeout = 5,           # timeout if Redis does not respond
                                        socket_connect_timeout = 3,   # timeout for connecting
                                        decode_responses = True)   

            self.client = redis.Redis(connection_pool = pool)
            
            pong = await self.client.ping()
            if pong:
                logger.info("Connected to Redis")
        except Exception as e:
            logger.error(f"Failed to connect to Redis: {e}")
            raise RedisError(e)

    async def close_redis_connection(self):
        logger.info("Closing Redis connection ...")
        if self.client:
            await self.client.aclose()
            logger.info("Redis - connection closed")

    async def check_health(self) -> bool:
        """Check if Redis is reachable and responsive."""
        if not self.client:
            logger.warning("Redis client is not initialized.")
            return False
        try:
            pong = await self.client.ping()
            return bool(pong)
        except Exception as e:
            logger.error(f"Redis health check failed: {e}")
            return False

    # --------------------------------------------------------
    # Key Management
    # --------------------------------------------------------

    async def check_key_exists(self, key: str) -> bool:
        logger.info(f"Start check_key_exists of {key}")
        try:
            exists = await self.client.exists(key)
            if exists:
                logger.info(f"Found key: {key}")
                return True
            else:
                logger.info(f"Not Found key: {key}")
                return False
        except Exception as e:
            logger.error(f"Redis error: {e}")
            raise RedisError(e)

    async def get_value_from_key(self, key: str) -> Optional[Any]:
        logger.info(f"Start get_value_from_key of {key}")
        try:
            values = await self.client.get(key)
            if values is None:
                logger.info(f"Redis checking status - not found of {key}")
                return None

            data = json.loads(values)
            value = data.get(key)
            logger.info(f"Value of '{key}' from is {value}")
            return value
        except Exception as e:
            logger.error(f"Redis error: {e}")
            raise RedisError(e)

    async def create_or_update_value(self, key: str, value: str | int | dict, expire_seconds: int = 3600):
        logger.info(f"Start create_or_update_value of {key}")
        try:
            await self.client.set(key, value, ex=expire_seconds)
            logger.info(f"Created/Updated session for {key} : {value}")
            return True
        except Exception as e:
            logger.error(f"Redis error: {e}")
            raise RedisError(e)