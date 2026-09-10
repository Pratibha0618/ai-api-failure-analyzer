from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.parser import parse_logs
from app.detector import detect_failures
from app.incident import group_into_incidents
from app.metrics import calculate_metrics
from app.ai_analyzer import analyze_incident


app = FastAPI(
    title="AI API Failure Analyzer",
    description="Analyzes API logs and identifies potential failures.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://ai-api-failure-analyzer-frontend.onrender.com",],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

class LogRequest(BaseModel):
    logs: str


@app.get("/")
def root():
    return {
        "message": "AI API Failure Analyzer is running"
    }


@app.post("/api/analyze")
def analyze(request: LogRequest):
    # Step 1: Parse raw logs
    events = parse_logs(request.logs)

    # Step 2: Detect individual failures
    failures = detect_failures(events)

    # Step 3: Calculate metrics
    metrics = calculate_metrics(events)

    # Step 4: Group related failures into incidents
    incidents = group_into_incidents(
        failures,
        metrics
    )

    # Step 5: Analyze each incident
    analyzed_incidents = []

    for incident in incidents:
        ai_analysis = analyze_incident(
            incident,
            metrics
        )

        analyzed_incidents.append({
            **incident,
            "ai_analysis": ai_analysis,
        })

    return {
        "metrics": metrics,
        "total_events": len(events),
        "total_failures": len(failures),
        "total_incidents": len(incidents),
        "incidents": analyzed_incidents,
    }