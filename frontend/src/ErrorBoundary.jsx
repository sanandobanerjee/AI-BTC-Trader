import { Component } from "react"

class ErrorBoundary extends Component {
  constructor(props) {
    super(props)
    this.state = { error: null }
  }

  static getDerivedStateFromError(error) {
    return { error: error.message }
  }

  componentDidCatch(error, info) {
    console.error("Component crashed:", error)
    console.error("Component stack:", info.componentStack)
  }

  render() {
    if (this.state.error) {
      return (
        <div style={{
          padding: 40,
          color: "#ef4444",
          background: "#0f0f0f",
          minHeight: "100vh",
          fontFamily: "monospace"
        }}>
          <h2 style={{ marginBottom: 16 }}>Component Error</h2>
          <pre style={{ whiteSpace: "pre-wrap" }}>{this.state.error}</pre>
          <button
            onClick={() => this.setState({ error: null })}
            style={{
              marginTop: 20,
              padding: "8px 16px",
              background: "#1a1a1a",
              color: "#f7931a",
              border: "1px solid #f7931a",
              borderRadius: 6,
              cursor: "pointer"
            }}
          >
            Retry
          </button>
        </div>
      )
    }
    return this.props.children
  }
}

export default ErrorBoundary