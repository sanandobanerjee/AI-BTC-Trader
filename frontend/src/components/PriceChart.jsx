import {
  LineChart, Line, XAxis, YAxis,
  CartesianGrid, Tooltip, ResponsiveContainer
} from "recharts"

function formatTime(isoString) {
  if (!isoString) return ""
  return new Date(isoString).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })
}

function formatPrice(value) {
  return "$" + Number(value).toLocaleString()
}

function PriceChart({ priceHistory, currentPrice }) {
  if (!priceHistory || priceHistory.length === 0) {
    return <div className="price-chart price-chart--empty"><p>No price history yet</p></div>
  }

  const chartData = [...priceHistory].reverse().map((s) => ({
    time:  formatTime(s.created_at),
    price: s.price_usd,
  }))

  const prices   = chartData.map((d) => d.price)
  const minPrice = Math.min(...prices)
  const maxPrice = Math.max(...prices)
  const padding  = (maxPrice - minPrice) * 0.1
  const yDomain  = [Math.floor(minPrice - padding), Math.ceil(maxPrice + padding)]

  return (
    <div className="price-chart">
      {currentPrice && (
        <div className="price-chart__current">
          <span className="price-chart__price">{formatPrice(currentPrice.price_usd)}</span>
          <span className={`price-chart__change ${
            currentPrice.price_change_24h_pct >= 0
              ? "price-chart__change--positive"
              : "price-chart__change--negative"
          }`}>
            {currentPrice.price_change_24h_pct >= 0 ? "+" : ""}
            {currentPrice.price_change_24h_pct?.toFixed(2)}% (24h)
          </span>
        </div>
      )}
      <div className="price-chart__graph">
        <ResponsiveContainer width="100%" height="100%">
        <LineChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" stroke="#2a2a2a" vertical={false} />
          <XAxis
            dataKey="time"
            tick={{ fontSize: 10, fill: "#808080", fontFamily: "JetBrains Mono" }}
            interval="preserveStartEnd"
            axisLine={false}
            tickLine={false}
          />
          <YAxis
            domain={yDomain}
            tickFormatter={formatPrice}
            tick={{ fontSize: 10, fill: "#808080", fontFamily: "JetBrains Mono" }}
            width={85}
            axisLine={false}
            tickLine={false}
          />
          <Tooltip
            formatter={(value) => [formatPrice(value), "BTC"]}
            contentStyle={{
              background: "#2a2a2a",
              border: "1px solid #4d4d4d",
              borderRadius: 6,
              fontSize: 12,
              fontFamily: "JetBrains Mono",
            }}
            labelStyle={{ color: "#808080" }}
            itemStyle={{ color: "#f7931a" }}
          />
          <Line
            type="monotone"
            dataKey="price"
            stroke="#f7931a"
            strokeWidth={1.5}
            dot={false}
            activeDot={{ r: 3, fill: "#f7931a" }}
          />
        </LineChart>
      </ResponsiveContainer>
      </div>
    </div>
  )
}

export default PriceChart