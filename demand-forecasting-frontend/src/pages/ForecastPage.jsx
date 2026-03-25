import { useParams } from "react-router-dom";
import { useEffect, useState } from "react";

/* ---------- Utilities ---------- */

const inferRiskLevel = (text) => {
  const t = text.toLowerCase();
  if (t.includes("shortage") || t.includes("disruption") || t.includes("delay"))
    return "HIGH";
  if (t.includes("seasonal") || t.includes("volatility") || t.includes("risk"))
    return "MEDIUM";
  return "LOW";
};

const riskColor = {
  LOW: "#22c55e",
  MEDIUM: "#facc15",
  HIGH: "#ef4444",
};

const splitIntoBullets = (text) =>
  text
    .split(/\.\s+|\n/)
    .map((s) => s.trim())
    .filter(Boolean);

/* ---------- Component ---------- */

const ForecastPage = () => {
  const { product, manufacturer } = useParams();
  const [data, setData] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    fetch(
      `http://localhost:8000/api/product/forecast-insight?product=${product}&manufacturer=${manufacturer}`
    )
      .then((res) => {
        if (!res.ok) throw new Error("Failed to fetch forecast insight");
        return res.json();
      })
      .then(setData)
      .catch((err) => setError(err.message));
  }, [product, manufacturer]);

  if (error) return <p style={{ padding: 40, color: "red" }}>{error}</p>;
  if (!data) return <p style={{ padding: 40 }}>Loading forecast...</p>;

  const bullets = splitIntoBullets(data.insight);
  const risk = inferRiskLevel(data.insight);

  return (
    <div style={{ padding: "40px", maxWidth: "900px", margin: "0 auto" }}>

      {/* Manufacturer */}
      <div style={boxStyle}>
        <h1>{data.manufacturer}</h1>
      </div>

      {/* Product */}
      <div style={{ ...boxStyle, opacity: 0.9 }}>
        <h3>{data.product}</h3>
      </div>

      {/* Forecast Insight */}
      <div
        style={{
          ...boxStyle,
          borderLeft: `6px solid ${riskColor[risk]}`,
        }}
      >
        <div style={{ display: "flex", alignItems: "center", gap: "12px" }}>
          <h4 style={{ margin: 0 }}>📈 Forecast Insight</h4>
          <span
            style={{
              background: riskColor[risk],
              color: "#000",
              padding: "4px 10px",
              borderRadius: "999px",
              fontSize: "12px",
              fontWeight: "600",
            }}
          >
            {risk} RISK
          </span>
        </div>

        <ul style={{ marginTop: "16px", paddingLeft: "20px" }}>
          {bullets.map((b, i) => (
            <li key={i} style={{ marginBottom: "8px" }}>
              {b.includes("increase") || b.includes("growth") ? "📈 " : ""}
              {b.includes("risk") || b.includes("shortage") ? "⚠️ " : ""}
              {b.includes("inventory") ? "📦 " : ""}
              {b}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

/* ---------- Shared Style ---------- */

const boxStyle = {
  background: "rgba(255,255,255,0.08)",
  borderRadius: "16px",
  padding: "22px 26px",
  marginBottom: "24px",
};

export default ForecastPage;
