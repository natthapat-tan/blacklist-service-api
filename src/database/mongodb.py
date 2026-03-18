import logging
import os

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from src.config import get_env

logger = logging.getLogger(__name__)
env = get_env()


class MongoConnector:

    client: AsyncIOMotorClient = None
    database: AsyncIOMotorDatabase = None

    # database connect and close connections
    async def connect_to_database(self, path: str, db_name: str = None):
        logger.info("Connecting to MongoDB ...")
        self.client = AsyncIOMotorClient(path,
                                         minPoolSize=20,
                                         maxPoolSize=100)
        
        if db_name is None:
            raise ValueError("Mongo Database Name is not set")
        self.database = getattr(self.client, db_name)

        logger.info("Connected to MongoDB")

    async def close_database_connection(self):
        logger.info("Closing connection to MongoDB")
        self.client.close()
        logger.info("MongoDB connection closed")

    async def find_documents(self, query: str, collection_name: str):
        cursor = self.database[collection_name].find(query)
        documents = []
        async for document in cursor:
            documents.append(document)
        # pprint.pprint(documents)
        return documents
    
    async def insert_documents(self, query: dict, collection_name: str):
        logger.info("MongoDB insert documents")
        collection = self.database[collection_name]  # This will create the collection if it doesn't exist
        await collection.insert_one(query)