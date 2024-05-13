from motor.motor_asyncio import AsyncIOMotorClient
from odmantic import AIOEngine

from config import MONGODB_NAME, MONGODB_URL

client = AsyncIOMotorClient(MONGODB_URL)
engine = AIOEngine(client=client, database=MONGODB_NAME)

__all__ = ["engine"]
