
from fastapi import FastAPI

app = FastAPI(
    title="RASD Intelligence",
    description="AI-powered Risk and Business Continuity Intelligence",
    version="0.1.0",
)


@app.get("/")
def home():
    return {
        "message": "RASD Intelligence API is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }



from pydantic import BaseModel, Field, ConfigDict
from typing import Literal


class RiskRequest(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True
    )

    supplier_name: str = Field(min_length=2, max_length=120)
    critical_process: str = Field(min_length=2, max_length=200)
    impact_level: Literal["low", "medium", "high"]
    recovery_hours: int = Field(ge=0, le=8760)



@app.post("/analyze-risk")
def analyze_risk(request: RiskRequest):
    scores = {
        "low": 25,
        "medium": 50,
        "high": 75
    }

    score = scores[request.impact_level]

    if request.recovery_hours > 24:
        score += 25

    score = min(score, 100)

    if score >= 75:
        risk_level = "High"
    elif score >= 50:
        risk_level = "Medium"
    else:
        risk_level = "Low"

    return {
        "supplier": request.supplier_name,
        "critical_process": request.critical_process,
        "risk_score": score,
        "risk_level": risk_level,
        "recovery_hours": request.recovery_hours
    }
