function timeAgo(isoString) {
  if (!isoString) return ""
  const seconds = Math.floor((new Date() - new Date(isoString)) / 1000)
  if (seconds < 60) return `${seconds}s ago`
  if (seconds < 3600) return `${Math.floor(seconds / 60)}m ago`
  if (seconds < 86400) return `${Math.floor(seconds / 3600)}h ago`
  return `${Math.floor(seconds / 86400)}d ago`
}

function labelConfig(label) {
  const map = {
    positive: { symbol: "🟢", className: "feed-item__label--positive" },
    negative: { symbol: "🔴", className: "feed-item__label--negative" },
    neutral:  { symbol: "🟡", className: "feed-item__label--neutral"  },
  }
  return map[label] ?? map.neutral
}

function FeedList({ feed, loading }) {
  if (loading) {
    return (
      <div className="feed-list feed-list--loading">
        <p>Loading feed...</p>
      </div>
    )
  }

  if (!feed || feed.length === 0) {
    return (
      <div className="feed-list feed-list--empty">
        <p>No sentiment records yet. Trigger pipeline to fetch articles.</p>
      </div>
    )
  }

  return (
    <ul className="feed-list">
      {feed.map((record) => {
        const { symbol, className } = labelConfig(record.label)
        const score = ((record.score ?? 0) * 100).toFixed(0)

        return (
          <li key={record.id} className="feed-item">
            <div className="feed-item__header">
              <span className={`feed-item__label ${className}`}>
                {symbol}                      {record.label}
              </span>
              <span className="feed-item__score"> - {score}%</span>
              <span className="feed-item__time"> - {timeAgo(record.created_at)}</span>
            </div>
            <p className="feed-item__text">{record.raw_text}.</p>
            <div className="feed-item__footer">
              <span className="feed-item__source">{record.source}</span>
            </div>
          </li>
        )
      })}
    </ul>
  )
}

export default FeedList