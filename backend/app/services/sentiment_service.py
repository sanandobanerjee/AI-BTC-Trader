from transformers import pipeline,Pipeline
from app.models.sentiment import SentimentRecord
from app.repositories.sentiment_repository import SentimentRepository
from app.core.config import get_settings

settings=get_settings()

LABEL_MAP={     #inference schema
    "positive":"positive",
    "negative":"negative",
    "neutral":"neutral"
}

class SentimentService:
    def __init__(self,repository: SentimentRepository):
        self.repository=repository
        self._pipeline: Pipeline=None

    def _load_model(self)->Pipeline:        #lazy init.FinBERT downloaded on first run then ran from disk
        if self._pipeline is None:
            self._pipeline=pipeline(
                task="text-classification",
                model="ProsusAI/FinBERT",
                top_k=1
            )
        return self._pipeline
    
    def _classify(self,text:str)->tuple[str,float]:
        model=self._load_model()
        result=model(text,truncation=True,max_length=512)   #safety net
        top=result[0][0]
        label=LABEL_MAP.get(top["label"].lower(),"neutral")
        score=round(top["score"],4)
        return label,score
    
    async def analyse_and_store(self,text:str,source:str)->SentimentRecord:
        label,score = self._classify(text)
        record=SentimentRecord(
            source=source,
            raw_text=text,
            score=score,
            label=label
        )
        await self.repository.insert(record)
        return record
    
#sequential processing used,optimise to parallel processing(can be raised as issue) 
    async def analyse_batch(self,posts:list[dict]) -> list[SentimentRecord]:
        results=[]
        for post in posts:
            record=await self.analyse_and_store(
                text=post["text"],
                source=post["source"]
            )
            results.append(record)
        return results
    
    async def get_recent(self,limit: int=20)-> list[SentimentRecord]:
        return await self.repository.find_many(limit=limit)