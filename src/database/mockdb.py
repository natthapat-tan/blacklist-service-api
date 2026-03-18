import logging
from src.config import get_env

logger = logging.getLogger(__name__)
env = get_env()

MOCK_DATA = [{"id_card":"1291249478943", "first_name":"John", "last_name":"Smith", "Age": 25, "salary" : 22000},
             {"id_card":"3984732443020", "first_name":"Jane", "last_name":"Doe", "Age": 30, "salary" : 35000},
             {"id_card":"3874792345544", "first_name":"Jack", "last_name":"Hammer", "Age": 21, "salary" : 15000},
             {"id_card":"2140924594295", "first_name":"Adam", "last_name":"Levine", "Age": 42, "salary" : 60000},
             {"id_card":"4287235922374", "first_name":"Kathy", "last_name":"Molt", "Age": 51, "salary" : 32000},
             {"id_card":"3244534543551", "first_name":"Carl", "last_name":"Allen", "Age": 33, "salary" : 43000}]


class MockConnector:

    is_connected: bool = False

    async def connect_to_database(self):
        logger.info("Connecting to Mock Database ...")
        self.is_connected = True
        logger.info("Connected to Mock Database")

    async def close_database_connection(self):
        logger.info("Closing Mock Database connection pool")
        self.is_connected = False
        logger.info("Mock Database - connection closed")

    # --------------------------------------------------------
    # Database Utilities
    # --------------------------------------------------------

    async def fetch_all(self, query: str, *args) -> list[dict]:
        if not self.is_connected:
            raise RuntimeError("Not connected to the Mock Database")
        logger.info("fetch_all called with query: %s | args: %s", query, args)
        return list(MOCK_DATA)

    async def fetch_one(self, query: str, *args) -> dict | None:
        if not self.is_connected:
            raise RuntimeError("Not connected to the Mock Database")
        logger.info("fetch_one called with query: %s | args: %s", query, args)
        return dict(MOCK_DATA[0]) if MOCK_DATA else None

    async def execute_query(self, query: str, *args) -> None:
        if not self.is_connected:
            raise RuntimeError("Not connected to the Mock Database")
        logger.info("execute_query called with query: %s | args: %s", query, args)

    async def execute_transaction(self) -> None:
        if not self.is_connected:
            raise RuntimeError("Not connected to the Mock Database")
        logger.info("execute_transaction called — returning success (no-op)")