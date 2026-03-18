from src.database.mongodb import MongoConnector
from src.database.postgresdb import PostgresConnector
from src.database.redisdb import RedisConnector
from src.database.mockdb import MockConnector

mongodb = MongoConnector()
postgresdb = PostgresConnector()
redisdb = RedisConnector()
mockdb = MockConnector()

async def mongo_database():
    return mongodb

async def postgres_database():
    return postgresdb

async def redis_database():
    return redisdb

async def mock_database():
    return mockdb