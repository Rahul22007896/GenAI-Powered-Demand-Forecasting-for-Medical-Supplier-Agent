import { useState } from "react";
import { Search } from "lucide-react";
import { Routes, Route } from "react-router-dom";
import ForecastPage from "./pages/ForecastPage";
import "./App.css";

/* ---------------- DASHBOARD ---------------- */

function Dashboard() {
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState("");

  const handleSubmit = async () => {
    if (!query.trim()) return;

    setLoading(true);
    setError("");
    setResults(null);

    try {
      const response = await fetch("http://localhost:8000/api/query", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query }),
      });

      if (!response.ok) {
        const err = await response.json();
        throw new Error(err.detail || "API error");
      }

      const data = await response.json();
      setResults(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-bg">
      <div className="container">

        {/* Header */}
        <div className="header">
          <h1>Demand Forecasting Analytics</h1>
        </div>

        {/* Search */}
        <div className="search-card">
          <div className="search-box">
            <Search size={18} />
            <input
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Ask a question about product demand..."
              disabled={loading}
            />
          </div>

          <button
            className="query-btn"
            onClick={handleSubmit}
            disabled={loading}
          >
            {loading ? "Processing..." : "Query Database"}
          </button>
        </div>

        {/* Error */}
        {error && <div className="error-box">Error: {error}</div>}

        {/* Results */}
        {results && (
          <div className="results-card">
            <div className="results-header">
              Results ({results.row_count} rows)
            </div>

            <div className="table-wrap">
              <table>
                <thead>
                  <tr>
                    {results.columns.map((col) => (
                      <th key={col}>{col.replace(/_/g, " ")}</th>
                    ))}
                  </tr>
                </thead>

                <tbody>
                  {results.data.map((row, i) => (
                    <tr key={i}>
                      {results.columns.map((col) => (
                        <td key={col}>
                          {col === "product_name" ? (
                            <a
                              href={`/forecast/${encodeURIComponent(
                                row.product_name
                              )}/${encodeURIComponent(row.manufacturer)}`}
                            >
                              {row.product_name}
                            </a>
                          ) : (
                            row[col]
                          )}
                        </td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

      </div>
    </div>
  );
}

/* ---------------- ROUTER ---------------- */

function App() {
  return (
    <Routes>
      <Route path="/" element={<Dashboard />} />
      <Route
        path="/forecast/:product/:manufacturer"
        element={<ForecastPage />}
      />
    </Routes>
  );
}

export default App;
