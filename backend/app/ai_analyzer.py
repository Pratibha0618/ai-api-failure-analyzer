import os
import json

from dotenv import load_dotenv
from google import genai


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError("GEMINI_API_KEY is not configured.")

client = genai.Client(api_key=api_key, http_options={"timeout": 30000})


def analyze_incident(incident: dict, metrics: dict) -> dict:
    prompt = f"""
You are an experienced Site Reliability Engineer.

Analyze the following API incident and determine the most likely root cause.

Incident:
{json.dumps(incident, indent=2)}

System metrics:
{json.dumps(metrics, indent=2)}

Return ONLY valid JSON in exactly this format:

{{
  "root_cause": "short explanation of the most likely root cause",
  "confidence": 0,
  "recommendations": [
    "recommendation 1",
    "recommendation 2",
    "recommendation 3"
  ]
}}

Rules:
- confidence must be an integer from 0 to 100.
- Base the diagnosis only on the provided evidence.
- Do not invent logs, metrics, or infrastructure details.
- Give practical recommendations an engineer could investigate.
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
    )

    text = response.text.strip()

    # Remove markdown code fences if Gemini adds them.
    if text.startswith("```"):
        text = text.replace("```json", "")
        text = text.replace("```", "")
        text = text.strip()

    return json.loads(text)