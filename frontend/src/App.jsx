import Dashboard from "./pages/Dashboard"
import ErrorBoundary from "./ErrorBoundary"
import "./index.css"
import "./dashboard.css"
import "./components/components.css"

function App() {
  return (
    <ErrorBoundary>
      <Dashboard />
    </ErrorBoundary>
  )
}

export default App