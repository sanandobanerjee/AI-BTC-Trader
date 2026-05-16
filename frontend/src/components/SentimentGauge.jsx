function SentimentGauge({positiveCount,negativeCount,neutralCount,sampleSize}) {
    if(!sampleSize || sampleSize===0){
        return(
            <div className="sentiment-gauge sentiment-gauge--empty">
                <p>No Sentiment Data Found</p>
            </div>
        )
    }

    const positivePct=((positiveCount/sampleSize)*100).toFixed(1)
    const negativePct=((negativeCount/sampleSize)*100).toFixed(1)
    const neutralPct=((neutralCount/sampleSize)*100).toFixed(1)

    const dominantLabel=
    positiveCount>=negativeCount&& positiveCount>=neutralCount?"Bullish":
    negativeCount >= positiveCount && negativeCount >= neutralCount?"Bearish"
      :"Neutral"  //positive beats negative on tie d/t conservative bias

    const dominantClass=
    dominantLabel==="Bullish"? "sentiment-gauge--bullish":
    dominantLabel === "Bearish"? "sentiment-gauge--bearish"
      : "sentiment-gauge--neutral"

    return (
    <div className={`sentiment-gauge ${dominantClass}`}>
      <div className="sentiment-gauge__label">{dominantLabel}</div>
      <div className="sentiment-gauge__bar">
        <div
          className="sentiment-gauge__segment sentiment-gauge__segment--positive"
          style={{ width: `${positivePct}%` }}
          title={`Positive: ${positivePct}%`}
        />
        <div
          className="sentiment-gauge__segment sentiment-gauge__segment--neutral"
          style={{ width: `${neutralPct}%` }}
          title={`Neutral: ${neutralPct}%`}
        />
        <div
          className="sentiment-gauge__segment sentiment-gauge__segment--negative"
          style={{ width: `${negativePct}%` }}
          title={`Negative: ${negativePct}%`}
        />
      </div>
      <div className="sentiment-gauge__stats">
        <span className="sentiment-gauge__stat sentiment-gauge__stat--positive">
          🟢 {positivePct}% Positive
        </span>
        <span className="sentiment-gauge__stat sentiment-gauge__stat--neutral">
          🟡 {neutralPct}% Neutral
        </span>
        <span className="sentiment-gauge__stat sentiment-gauge__stat--negative">
          🔴 {negativePct}% Negative
        </span>
      </div>
      <div className="sentiment-gauge__sample">
        Based on {sampleSize} articles
      </div>
    </div>
  )
}

export default SentimentGauge