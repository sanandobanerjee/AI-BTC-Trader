from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import get_settings

settings=get_settings()

client: AsyncIOMotorClient=None

async def connect_db():
    global client
    client=AsyncIOMotorClient(settings.MONGODB_URI)

async def close_db():
    global client
    if client:
        client.close()

def get_database():
    return client[settings.MONGODB_DB_NAME]
