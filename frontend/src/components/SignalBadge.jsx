function SignalBadge({ signal, confidence }) {
  if (!signal) {
    return (
      <div className="signal-badge signal-badge--empty">
        <span className="signal-badge__eyebrow">Active Signal</span>
        <span className="signal-badge__label">Awaiting Data</span>
      </div>
    )
  }

  const config = {
    BUY:  { label: "BUY",  className: "signal-badge--buy"  },
    SELL: { label: "SELL", className: "signal-badge--sell" },
    HOLD: { label: "HOLD", className: "signal-badge--hold" },
  }

  const { label, className } = config[signal] ?? config.HOLD
  const confidencePct = ((confidence ?? 0) * 100).toFixed(1)

  return (
    <div className={`signal-badge ${className}`}>
      <span className="signal-badge__eyebrow">Active Signal</span>
      <span className="signal-badge__label">{label}</span>
      <span className="signal-badge__confidence">{confidencePct}% Confidence</span>
    </div>
  )
}

export default SignalBadge