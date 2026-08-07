import { useState, useEffect } from "react"
import Dashboard from "./pages/Dashboard"
import ErrorBoundary from "./ErrorBoundary"
import { healthApi } from "./services/api"
import "./index.css"
import "./dashboard.css"
import "./components/components.css"

function App() {
  const [backendReady, setBackendReady] = useState(false)
  const [waking, setWaking]             = useState(true)

  useEffect(() => {
    let cancelled = false

    async function wake() {
      try {
        await healthApi.ping()
        if (!cancelled) {
          setBackendReady(true)
          setWaking(false)
        }
      } catch {
        if (!cancelled) {
          setWaking(false)
        }
      }
    }

    wake()
    return () => { cancelled = true }
  }, [])

  if (waking) {
    return (
      <div className="wake-screen">
        <span className="wake-screen__title">$aturn</span>
        <span className="wake-screen__msg">Waking up backend — this takes ~30s on first load</span>
        <span className="wake-screen__dot-row">
          <span className="wake-screen__dot" />
          <span className="wake-screen__dot" />
          <span className="wake-screen__dot" />
        </span>
      </div>
    )
  }

  return (
    <ErrorBoundary>
      <Dashboard />
    </ErrorBoundary>
  )
}

export default App