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

const LABEL_COLOR = {
  positive: "var(--buy)",
  negative: "var(--sell)",
  neutral:  "var(--hold)",
}

function FeedList({ feed, loading }) {
  if (loading) {
    return (
      <div className="feed-list feed-list--state">
        <p className="feed-list__message">Loading feed...</p>
      </div>
    )
  }

  if (!feed || feed.length === 0) {
    return (
      <div className="feed-list feed-list--state">
        <p className="feed-list__message">No records yet. Trigger pipeline to fetch articles.</p>
      </div>
    )
  }

  return (
    <div className="feed-list">
      {feed.map((record) => {
        const label = record.label ?? "neutral"
        const score = ((record.score ?? 0) * 100).toFixed(0)
        const color = LABEL_COLOR[label] ?? LABEL_COLOR.neutral

        return (
          <div key={record.id} className="feed-item">
            <div className="feed-item__header">
              <span className="feed-item__sentiment" style={{ color }}>
                {label.charAt(0).toUpperCase() + label.slice(1)}
                <span className="feed-item__score"> — {score}%</span>
              </span>
              <span className="feed-item__time">{timeAgo(record.created_at)}</span>
            </div>
            <p className="feed-item__text">{stripHtml(record.raw_text)}</p>
          </div>
        )
      })}
    </div>
  )
}

export default FeedList