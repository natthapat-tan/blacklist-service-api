from src.database.mongodb import MongoConnector
from src.database.postgresdb import PostgresConnector
from src.database.redisdb import RedisConnector

mongo_database = MongoConnector()
postgres_database = PostgresConnector()
redis_database = RedisConnector()

async def get_mongo_database():
    return mongo_database

async def get_postgres_database():
    return postgres_database

async def get_redis_database():
    return redis_database