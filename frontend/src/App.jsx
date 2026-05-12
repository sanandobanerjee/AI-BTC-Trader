import Dashboard from "./pages/Dashboard"
import ErrorBoundary from "./ErrorBoundary"
import "./dashboard.css"

function App() {
  return (
    <ErrorBoundary>
      <Dashboard />
    </ErrorBoundary>
  )
}

export default App