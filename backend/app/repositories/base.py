from abc import ABC,abstractmethod
from typing import Optional,Generic,TypeVar
from motor.motor_asyncio import AsyncIOMotorDatabase

T=TypeVar("T")

class BaseRepository(ABC,Generic[T]):
        def __init__(self, db:AsyncIOMotorDatabase, collection_name:str):
                self.collection=db[collection_name]
            
        @abstractmethod
        async def insert(self,document:T) -> str:
                pass
        
        @abstractmethod
        async def find_latest(self) -> Optional[T]:
                pass
        
        @abstractmethod
        async def find_many(self,limit:int=20)->list[T]:
                pass