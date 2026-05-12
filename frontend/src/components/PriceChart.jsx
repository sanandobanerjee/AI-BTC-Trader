import {
    LineChart,Line,XAxis,YAxis,CartesianGrid,Tooltip,ResponsiveContainer
} from "recharts"

function formatTime(isoString) {
  if (!isoString) return ""
  const parsed = new Date(isoString)
  return parsed.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })
}

function formatPrice(value){
        return "$" + Number(value).toLocaleString()
}

function PriceChart({priceHistory,currentPrice}){
    if (!priceHistory || priceHistory.length === 0) {
        return (
            <div className="price-chart price-chart--empty">
                <p>No price history yet</p>
            </div>
        )
    }

      const chartData = [...priceHistory]
    .reverse()
    .map((snapshot) => ({
      time: formatTime(snapshot.created_at),
      price: snapshot.price_usd,
    }))

    const prices = chartData.map((d) => d.price)
    const minPrice = Math.min(...prices)
    const maxPrice = Math.max(...prices)
    const padding = (maxPrice - minPrice) * 0.05
    const yDomain = [Math.floor(minPrice - padding),Math.ceil(maxPrice + padding),]

    return (
    <div className="price-chart">
      {currentPrice && (
        <div className="price-chart__current">
          <span className="price-chart__price">
            {formatPrice(currentPrice.price_usd)}
          </span>
            <span
              className={
                "price-chart__change " +
                (currentPrice.price_change_24h_pct >= 0
                ? "price-chart__change--positive"
                : "price-chart__change--negative")
              }
             >
            {currentPrice.price_change_24h_pct >= 0 ? "+" : ""}
            {currentPrice.price_change_24h_pct?.toFixed(2)}% (24h)
          </span>
        </div>
      )}
      <ResponsiveContainer width="100%" height={200}>
        <LineChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" stroke="#2a2a2a" />
          <XAxis
            dataKey="time"
            tick={{ fontSize: 11, fill: "#888" }}
            interval="preserveStartEnd"/>
          <YAxis
            domain={yDomain}
            tickFormatter={formatPrice}
            tick={{ fontSize: 11, fill: "#888" }}
            width={90}/>
          <Tooltip
            formatter={(value) => [formatPrice(value), "BTC Price"]}
            contentStyle={{ background: "#1a1a1a", border: "1px solid #333" }}
            labelStyle={{ color: "#888" }}/>
          <Line
            type="monotone"
            dataKey="price"
            stroke="#000090"
            strokeWidth={2}
            dot={false}
            activeDot={{ r: 4 }}/>
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}

export default PriceChart