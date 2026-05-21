function SentimentGauge({ positiveCount, negativeCount, neutralCount, sampleSize }) {
  if (!sampleSize || sampleSize === 0) {
    return (
      <div className="sentiment-gauge sentiment-gauge--empty">
        <p>No sentiment data yet</p>
      </div>
    )
  }

  const positivePct = ((positiveCount / sampleSize) * 100).toFixed(1)
  const negativePct = ((negativeCount / sampleSize) * 100).toFixed(1)
  const neutralPct  = ((neutralCount  / sampleSize) * 100).toFixed(1)

  const dominantLabel =
    positiveCount >= negativeCount && positiveCount >= neutralCount ? "Bullish" :
    negativeCount >= positiveCount && negativeCount >= neutralCount ? "Bearish" :
    "Neutral"

  const dominantClass =
    dominantLabel === "Bullish" ? "sentiment-gauge--bullish" :
    dominantLabel === "Bearish" ? "sentiment-gauge--bearish" :
    "sentiment-gauge--neutral"

  return (
    <div className={`sentiment-gauge ${dominantClass}`}>
      <div className="sentiment-gauge__label">{dominantLabel}</div>
      <div className="sentiment-gauge__sublabel">Current Sentiment</div>
      <div className="sentiment-gauge__stats">
        {[
          { key: "positive", label: "Bullish", value: positivePct },
          { key: "neutral",  label: "Neutral", value: neutralPct  },
          { key: "negative", label: "Bearish", value: negativePct },
        ].map(({ key, label, value }) => (
          <div key={key} className={`sentiment-gauge__stat sentiment-gauge__stat--${key}`}>
            <span className="sentiment-gauge__stat-name">{label} - </span>
            <span className="sentiment-gauge__stat-val">{value}%</span>
          </div>
        ))}
      </div>
      <div className="sentiment-gauge__sample">Based on {sampleSize} articles</div>
    </div>
  )
}

export default SentimentGauge