function stripHtml(html) {
  if (!html) return ""
  return html.replace(/<[^>]*>/g, " ").replace(/\s+/g, " ").trim()
}

function timeAgo(isoString) {
  if (!isoString) return ""
  const seconds = Math.floor((new Date() - new Date(isoString)) / 1000)
  if (seconds < 60)    return `${seconds}s ago`
  if (seconds < 3600)  return `${Math.floor(seconds / 60)}m ago`
  if (seconds < 86400) return `${Math.floor(seconds / 3600)}h ago`
  return `${Math.floor(seconds / 86400)}d ago`
}

function FeedList({ feed, loading }) {
  if (loading) {
    return <div className="feed-list feed-list--loading"><p>Loading feed...</p></div>
  }

  if (!feed || feed.length === 0) {
    return (
      <div className="feed-list feed-list--empty">
        <p>No records yet. Trigger pipeline to fetch articles.</p>
      </div>
    )
  }

  return (
    <ul className="feed-list">
      {feed.map((record) => {
        const label = record.label ?? "neutral"
        const score = ((record.score ?? 0) * 100).toFixed(0)

        return (
          <li key={record.id} className={`feed-item feed-item--${label}`}>
            <div className="feed-item__header">
              <span className="feed-item__source">{record.source}</span>
              <div className="feed-item__meta-right">
                <span className={`feed-item__label feed-item__label--${label}`}>
                  {label}
                </span>
                <span className="feed-item__score">{score}%</span>
              </div>
            </div>
            <p className="feed-item__text">{stripHtml(record.raw_text)}</p>
            <span className="feed-item__time">{timeAgo(record.created_at)}</span>
          </li>
        )
      })}
    </ul>
  )
}

export default FeedList