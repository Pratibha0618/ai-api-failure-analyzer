import { useState } from "react";
import "./App.css";

function App() {
  const [logs, setLogs] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleFileUpload = (event) => {
    const file = event.target.files[0];

    if (!file) return;

    if (!file.name.endsWith(".log") && !file.name.endsWith(".txt")) {
      alert("Please upload a .log or .txt file.");
      return;
    }

    const reader = new FileReader();

    reader.onload = (e) => {
      setLogs(e.target.result);
      setResult(null);
    };

    reader.readAsText(file);
  };

  const analyzeLogs = async () => {
    if (!logs.trim()) {
      alert("Please paste logs or upload a log file.");
      return;
    }

    setLoading(true);
    setResult(null);

    try {
      const response = await fetch("https://ai-api-failure-analyzer-backend1.onrender.com/api/analyze", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ logs }),
      });

      if (!response.ok) {
        throw new Error("Backend returned an error.");
      }

      const data = await response.json();
      setResult(data);
    } catch (error) {
      console.error(error);
      alert("Could not connect to the backend.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">

      <header className="header">
        <div className="header-content">
          <h1>AI API Failure Analyzer</h1>
          <p>
            Detect API failures, correlate incidents, and identify potential
            root causes.
          </p>
        </div>
      </header>

      <main className="container">

        <section className="input-section">
          <h2>Log Analysis</h2>

          <div className="upload-area">
            <label htmlFor="log-file">
              Upload .log file
            </label>

            <input
              id="log-file"
              type="file"
              accept=".log,.txt"
              onChange={handleFileUpload}
            />

            <span>or paste your logs below</span>
          </div>

          <textarea
            value={logs}
            onChange={(e) => setLogs(e.target.value)}
            placeholder="Paste your API logs here..."
          />

          <button
            className="analyze-button"
            onClick={analyzeLogs}
            disabled={loading}
          >
            {loading ? "Analyzing..." : "Analyze Logs"}
          </button>
        </section>

        {result && (
          <>
            <section className="metrics">

              <div className="metric-card">
                <span>Total Requests</span>
                <strong>{result.metrics.total_requests}</strong>
              </div>

              <div className="metric-card">
                <span>Failed Requests</span>
                <strong>{result.metrics.failed_requests}</strong>
              </div>

              <div className="metric-card">
                <span>Error Rate</span>
                <strong>{result.metrics.error_rate_percent}%</strong>
              </div>

              <div className="metric-card">
                <span>Avg Latency</span>
                <strong>
                  {result.metrics.average_latency_ms} ms
                </strong>
              </div>

              <div className="metric-card">
                <span>Incidents</span>
                <strong>{result.total_incidents}</strong>
              </div>

            </section>

            <section className="incidents">
              <h2>Detected Incidents</h2>

              {result.incidents.map((incident) => (
                <div
                  className="incident-card"
                  key={incident.incident_id}
                >

                  <div className="incident-header">
                    <h3>Incident #{incident.incident_id}</h3>

                    <span className="severity">
                      {incident.severity}
                    </span>
                  </div>

                  <p>
                    <strong>Affected endpoint:</strong>{" "}
                    {incident.affected_endpoints.join(", ")}
                  </p>

                  <p>
                    <strong>Failures:</strong>{" "}
                    {incident.failure_count}
                  </p>

                  <h4>Root Cause Analysis</h4>

                  <div className="root-cause">
                    {incident.ai_analysis.root_cause}
                  </div>

                  <p>
                    <strong>Confidence:</strong>{" "}
                    {incident.ai_analysis.confidence}%
                  </p>

                  <h4>Recommendations</h4>

                  <ul className="recommendations">
                    {incident.ai_analysis.recommendations.map(
                      (recommendation, index) => (
                        <li key={index}>
                          {recommendation}
                        </li>
                      )
                    )}
                  </ul>

                  {incident.anomalies.length > 0 && (
                    <>
                      <h4>Latency Anomalies</h4>

                      {incident.anomalies.map(
                        (anomaly, index) => (
                          <div
                            className="anomaly"
                            key={index}
                          >
                            <strong>
                              {anomaly.endpoint}
                            </strong>

                            <span>
                              {anomaly.latency_ms} ms
                            </span>

                            <small>
                              {anomaly.reason}
                            </small>
                          </div>
                        )
                      )}
                    </>
                  )}

                </div>
              ))}
            </section>
          </>
        )}

      </main>
    </div>
  );
}

export default App;