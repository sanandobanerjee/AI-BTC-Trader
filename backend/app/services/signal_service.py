from app.models.signal import TradingSignal
from app.repositories.sentiment_repository import SentimentRepository
from app.repositories.signal_repository import SignalRepository

#configurational values
BUY_THRESHOLD=0.6
SELL_THRESHOLD=0.4
MIN_SAMPLE_SIZE=5

class SignalService:
    def __init__(
        self, 
        sentiment_repository: SentimentRepository,
        signal_repository: SignalRepository
    ):
        self.sentiment_repo = sentiment_repository
        self.signal_repo= signal_repository


    async def compute_and_store(self,sample_size: int=20) -> TradingSignal:
        records= await self.sentiment_repo.find_many(limit=sample_size)

        if len(records)< MIN_SAMPLE_SIZE:
            return await self._store_hold_signal(
                reason="insufficient_data",
                sample_size=len(records)
            )

        positive=[r for r in records if r.label == "positive"]
        negative=[r for r in records if r.label == "negative"]
        neutral=[r for r in records if r.label == "neutral"]

        avg_score=sum(r.score for r in records)/len(records)

        positive_ratio=len(positive)/len(records)
        negative_ratio=len(negative)/len(records)

        signal, confidence=self._decide(
            positive_ratio=positive_ratio,
            negative_ratio=negative_ratio,
            avg_score=avg_score)
        
        trading_signal=TradingSignal(
            signal=signal,
            confidence=round(confidence,4),
            avg_sentiment_score=round(avg_score,4),
            positive_count=len(positive),
            negative_count=len(negative),
            neutral_count=len(neutral),
            sample_size=len(records)
        )

        await self.signal_repo.insert(trading_signal)
        return trading_signal
    
    def _decide(
        self,
        positive_ratio: float,
        negative_ratio:float,
        avg_score:float,
    ) -> tuple[str,float]:
        
        if positive_ratio >= BUY_THRESHOLD:
            confidence=(positive_ratio - BUY_THRESHOLD)/(1-BUY_THRESHOLD)
            return "BUY", confidence

        if negative_ratio >= SELL_THRESHOLD:
            confidence=(negative_ratio - SELL_THRESHOLD)/(1 - SELL_THRESHOLD)
            return "SELL", confidence
        
        spread=abs(positive_ratio-negative_ratio)
        confidence=1-spread
        return "HOLD", confidence
    
    async def _store_hold_signal(
        self,
        reason: str,    #for future scenario to differentiate errrors
        sample_size: int,
    ) -> TradingSignal:
        signal=TradingSignal(
            signal = "HOLD",
            confidence=0.0,
            avg_sentiment_score=0.0,
            positive_count=0,
            negative_count=0,
            neutral_count=0,
            sample_size=sample_size
        )
        await self.signal_repo.insert(signal)
        return signal
    
    async def get_latest(self)-> TradingSignal | None:
        return await self.signal_repo.find_latest()

    async def get_history(self,limit: int =20) -> list[TradingSignal]:
        return await self.signal_repo.find_many(limit=limit)        
