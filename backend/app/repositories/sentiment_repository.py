from typing import Optional
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.repositories.base import BaseRepository
from app.models.sentiment import SentimentRecord

class SentimentRepository(BaseRepository[SentimentRecord]):
    def __init__(self, db: AsyncIOMotorDatabase):
        super().__init__(db, "sentiments")

    async def insert(self, document: SentimentRecord)->str:
        payload = document.model_dump()
        payload["_id"]=payload.pop("id")    #resolves id conflict
        result = await self.collection.insert_one(payload)
        return str(result.inserted_id)
    
    async def find_latest(self)-> Optional[SentimentRecord]:
        doc=await self.collection.find_one(
            sort=[("created_at",-1)]
        )
        if not doc:
            return None
        doc["id"]=str(doc.pop("_id"))
        return SentimentRecord(**doc)
    
    async def find_many(self, limit: int = 20)-> list[SentimentRecord]:
        cursor= self.collection.find().sort("created_at",-1).limit(limit)
        docs=await cursor.to_list(length=limit)
        records=[]
        for doc in docs:
            doc["id"]=str(doc.pop("_id"))
            records.append(SentimentRecord(**doc))
        return records
    
    async def find_by_source(self,source:str,limit:int=20)-> list[SentimentRecord]:
        cursor=self.collection.find({"source":source}).sort("created_at",-1).limit(limit)
        docs=await cursor.to_list(length=limit)
        records=[]
        for doc in docs:
            doc["id"]=str(doc.pop("_id"))
            records.append(SentimentRecord(**doc))
        return records