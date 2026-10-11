
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_valid_risk_request():
    response = client.post(
        "/analyze-risk",
        json={
            "supplier_name": "Saudi Logistics",
            "critical_process": "Supply Chain",
            "impact_level": "high",
            "recovery_hours": 48
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["risk_score"] == 100
    assert data["risk_level"] == "High"


def test_reject_invalid_impact_level():
    response = client.post(
        "/analyze-risk",
        json={
            "supplier_name": "Test Supplier",
            "critical_process": "Testing",
            "impact_level": "unknown",
            "recovery_hours": 12
        },
    )
    assert response.status_code == 422


def test_reject_negative_recovery_hours():
    response = client.post(
        "/analyze-risk",
        json={
            "supplier_name": "Test Supplier",
            "critical_process": "Testing",
            "impact_level": "low",
            "recovery_hours": -1
        },
    )
    assert response.status_code == 422


def test_reject_extra_fields():
    response = client.post(
        "/analyze-risk",
        json={
            "supplier_name": "Test Supplier",
            "critical_process": "Testing",
            "impact_level": "low",
            "recovery_hours": 12,
            "is_admin": True
        },
    )
    assert response.status_code == 422
