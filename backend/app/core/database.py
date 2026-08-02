import certifi
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import OperationFailure
from app.core.config import get_settings

settings=get_settings()
client: AsyncIOMotorClient=None

async def connect_db():
    global client
    client=AsyncIOMotorClient(
        settings.MONGODB_URI,
        tlsCAFile=certifi.where())
    await ensure_ttl_indexes()

async def ensure_ttl_indexes():
    db = get_database()
    sentiment_ttl_seconds = settings.SENTIMENT_TTL_DAYS * 86400
    signal_ttl_seconds = sentiment_ttl_seconds + (settings.SIGNAL_TTL_BUFFER_HOURS * 3600) 
    #signal stays for 12 hours on top of the sentiment timeline

    await _apply_ttl(db["sentiments"], "sentiments", sentiment_ttl_seconds)
    await _apply_ttl(db["signals"], "signals", signal_ttl_seconds)

async def _apply_ttl(collection, name, ttl_seconds):
    db = get_database()
    try:
        await collection.create_index(
            "created_at",
            name="created_at_ttl",
            expireAfterSeconds=ttl_seconds,
        )
    except OperationFailure as exc:
        if exc.code == 85:
            await db.command(
                "collMod",
                name,
                index={
                    "keyPattern": {"created_at": 1},
                    "expireAfterSeconds": ttl_seconds,
                },
            )
        else:
            raise

async def close_db():
    global client
    if client:
        client.close()

def get_database():
    return client[settings.MONGODB_DB_NAME]