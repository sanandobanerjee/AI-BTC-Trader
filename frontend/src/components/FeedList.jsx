function stripHtml(html) {
  if (!html) return ""
  return html.replace(/<[^>]*>/g, " ").replace(/\s+/g, " ").trim()
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
        const text  = stripHtml(record.raw_text)
        const hasUrl = Boolean(record.url)

        return (
          <div key={record.id} className="feed-item">
            <div className="feed-item__header">
              <span className="feed-item__sentiment" style={{ color }}>
                {label.charAt(0).toUpperCase() + label.slice(1)}
                <span className="feed-item__score"> — {score}%</span>
              </span>
            </div>
            {hasUrl ? (
              <a className="feed-item__text feed-item__link" href={record.url} target="_blank" rel="noopener noreferrer">{text}</a>
            ) : (
              <p className="feed-item__text">{text}</p>
            )}
          </div>
        )
      })}
    </div>
  )
}

export default FeedList