import logging
import os
import asyncpg
from typing import List, Dict, Any

from src.config import get_env

logger = logging.getLogger(__name__)
env = get_env()


class PostgresConnector:

    pool: asyncpg.Pool = None

    async def connect_to_database(self, path: str):
        logger.info("Connecting to PostgreSQL ...")

        try:
            self.pool = await asyncpg.create_pool(
                dsn=path,
                min_size=10,
                max_size=100,
                command_timeout=60,
            )
            logger.info("Connected to PostgreSQL")

        except Exception as e:
            logger.error(f"Failed to connect to PostgreSQL: {e}")
            raise

    async def close_database_connection(self):
        logger.info("Closing PostgreSQL connection pool")
        if self.pool:
            await self.pool.close()
            logger.info("PostgreSQL - connection closed")

    async def check_health(self) -> bool:
        if not self.pool:
            logger.warning("Postgres pool is not initialized.")
            return False
        try:
            async with self.pool.acquire() as conn:
                value = await conn.fetchval("SELECT 1;")
                return value == 1
        except Exception as e:
            logger.error(f"Postgres health check failed: {e}")
            return False
        
    # --------------------------------------------------------
    # Database Utilities
    # --------------------------------------------------------

    async def fetch_all(self, query: str, *args) -> List[asyncpg.Record]:
        try:
            logger.debug("PostgreSQL - Start fetching all ...")

            async with self.pool.acquire() as conn:
                result = await conn.fetch(query, *args)
                logger.debug("PostgreSQL - Fetching all complete !")
                return result
        except Exception as e:
            logger.error(f"PostgreSQL - fetch_all error : {e}")
            raise e

    async def fetch_one(self, query: str, *args) -> asyncpg.Record:
        try:
            logger.debug("PostgreSQL - Start fetching one ...")
            
            async with self.pool.acquire() as conn:
                result = await conn.fetchrow(query, *args)
                logger.debug("PostgreSQL - Fetching one complete !")
                return result
        except Exception as e:
            logger.error(f"PostgreSQL - fetch_one error : {e}")
            raise e

    async def execute_query(self, query: str, *args):
        try:
            logger.debug("PostgreSQL - Start executing query ...")

            async with self.pool.acquire() as conn:
                await conn.execute(query, *args)
                logger.debug("PostgreSQL - Query execution complete !")
        except Exception as e:
            logger.error(f"PostgreSQL - execute_query error : {e}")
            raise e
        
    async def execute_transaction(self, queries: List[Dict[str, Any]]):
        """
        Execute multiple SQL statements in a single transaction.
        Each item in `queries` should be a dict with keys:
        {
            "query": str,
            "params": tuple
        }

        EXAMPLE :
        queries = [
                    {
                        "query": "INSERT INTO users (id, name) VALUES ($1, $2)",
                        "params": (1, "Alice")
                    },
                    {
                        "query": "UPDATE accounts SET balance = balance - $1 WHERE id = $2",
                        "params": (100, 1)
                    }
                ]
        USAGE :
        await postgres_db.execute_transaction(queries)
        """
        try:
            logger.debug("PostgreSQL - Transaction start ...")

            async with self.pool.acquire() as conn:
                async with conn.transaction():
                    for item in queries:
                        await conn.execute(item["query"], *item.get("params", []))
            logger.debug("PostgreSQL - Transaction committed successfully.")
        except Exception as e:
            logger.error(f"PostgreSQL - Transaction failed and rolled back : {e}")
            raise e