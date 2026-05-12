from typing import Optional
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.repositories.base import BaseRepository
from app.models.signal import TradingSignal

class SignalRepository(BaseRepository[TradingSignal]):
    def __init__(self, db: AsyncIOMotorDatabase):
        super().__init__(db, "signals")

    async def insert(self, document: TradingSignal)->str:
        payload = document.model_dump()
        payload["_id"]=payload.pop("id")    #resolves id conflict
        result = await self.collection.insert_one(payload)
        return str(result.inserted_id)
    
    async def find_latest(self)-> Optional[TradingSignal]:
        doc=await self.collection.find_one(
            sort=[("created_at",-1)]
        )
        if not doc:
            return None
        doc["id"]=str(doc.pop("_id"))
        return TradingSignal(**doc)
    
    async def find_many(self, limit: int = 20)-> list[TradingSignal]:
        cursor= self.collection.find().sort("created_at",-1).limit(limit)
        docs=await cursor.to_list(length=limit)
        records=[]
        for doc in docs:
            doc["id"]=str(doc.pop("_id"))
            records.append(TradingSignal(**doc))
        return records
    
    async def find_by_signal_type(self,signal:str,limit:int=20)-> list[TradingSignal]:
        cursor=self.collection.find({"signal":signal}).sort("created_at",-1)
        docs=await cursor.to_list(length=50)
        records=[]
        for doc in docs:
            doc["id"]=str(doc.pop("_id"))
            records.append(TradingSignal(**doc))
        return records