# AI API Failure Analyzer

An AI-powered API observability tool that analyzes application logs, detects failures, identifies latency anomalies, correlates related errors into incidents, and generates root-cause analysis using Google Gemini.

## Features

- **Log Parsing** — Extracts timestamps, log levels, HTTP methods, endpoints, status codes, and latency.
- **Failure Detection** — Identifies timeouts, database errors, payment failures, application errors, and HTTP 5xx responses.
- **Metrics** — Calculates request count, failure count, error rate, average latency, median latency, and endpoint-level statistics.
- **Latency Anomaly Detection** — Uses Median Absolute Deviation (MAD) and modified z-scores to identify unusually high latency.
- **Incident Correlation** — Groups related failures occurring within a short time window into incidents.
- **AI Root-Cause Analysis** — Uses Google Gemini to analyze incidents and provide root-cause hypotheses, confidence scores, and recommendations.
- **Web Dashboard** — React-based interface for uploading or pasting logs and viewing analysis results.
- **Dockerized** — Frontend and backend can be run together using Docker Compose.

## Architecture

```text
                    React Dashboard
                          |
                          v
                    Nginx Proxy
                          |
                          v
                     FastAPI API
                          |
          +---------------+---------------+
          |               |               |
          v               v               v
        Parser         Detector        Metrics
          |               |               |
          +---------------+---------------+
                          |
                          v
                Incident Correlation
                          |
                          v
                    Gemini AI
                          |
                          v
                Root-Cause Analysis
```

## Tech Stack

**Frontend**

- React
- Vite
- JavaScript
- CSS

**Backend**

- Python
- FastAPI
- Pydantic

**AI**

- Google Gemini API
- `google-genai`

**Infrastructure**

- Docker
- Docker Compose
- Nginx

## Project Structure

```text
ai-api-failure-analyzer/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── parser.py
│   │   ├── detector.py
│   │   ├── incident.py
│   │   ├── metrics.py
│   │   └── ai_analyzer.py
│   ├── Dockerfile
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   └── main.jsx
│   ├── Dockerfile
│   ├── nginx.conf
│   └── package.json
│
├── docker-compose.yml
├── .gitignore
└── README.md
```

## How It Works

1. User uploads or pastes API logs.
2. FastAPI parses the logs into structured events.
3. Failures and HTTP 5xx responses are detected.
4. System and endpoint-level metrics are calculated.
5. Latency anomalies are identified using MAD-based statistical detection.
6. Related failures are grouped into incidents.
7. Incident data and metrics are sent to Gemini.
8. Gemini generates a root-cause hypothesis, confidence score, and recommendations.
9. Results are displayed in the React dashboard.

## Example

### Input

```text
2026-09-08 14:30:01 INFO POST /api/payment 200 180ms
2026-09-08 14:30:02 INFO GET /api/users 200 95ms
2026-09-08 14:30:03 INFO GET /api/orders 200 140ms
2026-09-08 14:30:04 INFO POST /api/payment 200 210ms
2026-09-08 14:30:05 INFO GET /api/users 200 110ms
2026-09-08 14:30:06 ERROR Database connection timeout
2026-09-08 14:30:07 ERROR POST /api/payment 500 4800ms
2026-09-08 14:30:08 ERROR GET /api/orders 500 520ms
2026-09-08 14:30:20 INFO GET /api/users 200 105ms
2026-09-08 14:30:21 ERROR Payment service unavailable
2026-09-08 14:30:22 ERROR POST /api/payment 500 3900ms
2026-09-08 14:30:23 INFO GET /api/users 200 100ms
```

### Analysis

```text
Total Requests:    10
Failed Requests:    3
Error Rate:        30%
Average Latency: 1016 ms
Incidents:           2
```

Example incident:

```text
Severity: CRITICAL

Affected Endpoints:
/api/payment
/api/orders

Root Cause:
Database connection timeouts caused downstream HTTP 500
errors and elevated API latency.

Confidence: 92%
```

## Running Locally

### Backend

```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Create `backend/.env`:

```env
GEMINI_API_KEY=your_api_key_here
```

Start the backend:

```powershell
uvicorn app.main:app --reload
```

Backend runs on:

```text
http://localhost:8000
```

### Frontend

```powershell
cd frontend
npm install
npm run dev
```

Frontend runs on:

```text
http://localhost:5173
```

## Running with Docker

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_api_key_here
```

Build the application:

```powershell
docker compose build
```

Start the application:

```powershell
docker compose up
```

Open:

```text
http://localhost:5173
```

Stop the application:

```powershell
docker compose down
```

## API

### Health Check

```http
GET /
```

### Analyze Logs

```http
POST /api/analyze
```

Request:

```json
{
  "logs": "2026-09-08 14:30:01 INFO POST /api/payment 200 180ms"
}
```

## Security

The Gemini API key is stored in an environment variable and excluded from Git using `.gitignore`.

**Never commit your API key to the repository.**

## Current Limitations

- Supports a structured log format.
- Incident correlation uses a fixed time window.
- Incident data is not persisted.
- No authentication or user management.
- No automated test suite yet.
- AI analysis depends on Gemini API availability.

## Future Improvements

- PostgreSQL-based incident persistence
- Configurable incident correlation
- Historical incident comparison
- Prometheus/Grafana monitoring
- Automated tests and CI/CD
- Slack/PagerDuty integrations
- Authentication and rate limiting
- Similar-incident detection using historical data

## Project Status

**MVP / Portfolio Project**

Implemented:

- [x] Log parsing
- [x] Failure detection
- [x] Reliability metrics
- [x] Latency anomaly detection
- [x] Incident correlation
- [x] AI root-cause analysis
- [x] AI recommendations
- [x] React dashboard
- [x] Docker deployment
- [x] Nginx reverse proxy

## License

This project is available for educational and portfolio purposes.
