"""Security hardening and responsible AI automated verification test suite (Phase 15).

Tests:
1. HTTP Security Headers (OWASP defensive headers injection).
2. Client Request Rate Limiting (Sliding window enforcement & 429 response).
3. Payload Size Limitation (413 response on oversized payloads).
4. Path Traversal & File Access Defenses.
5. Responsible AI Safeguards:
   - Context Gating (DEC-17).
   - Automated Stale/Uncertain Data Suppression (DEC-10).
   - Mandatory Field Verification Disclaimers.
   - Anti-Overconfidence Linguistic Standards.
   - Absence of Causal Claims in Explanations.
"""

import pytest
from fastapi.testclient import TestClient
from api.main import app
from api.data_access.repository import AgriculturalDataRepository
from api.middleware.security import RateLimitMiddleware, RequestSizeLimitMiddleware


@pytest.fixture
def client():
    """FastAPI TestClient fixture."""
    return TestClient(app)


def test_http_security_headers_present(client):
    """Verify that OWASP-compliant defensive security headers are injected into API responses."""
    response = client.get("/health")
    assert response.status_code == 200
    headers = response.headers

    # Verify OWASP defensive headers
    assert headers.get("x-content-type-options") == "nosniff"
    assert headers.get("x-frame-options") == "DENY"
    assert headers.get("x-xss-protection") == "1; mode=block"
    assert headers.get("referrer-policy") == "strict-origin-when-cross-origin"
    assert "default-src 'self'" in headers.get("content-security-policy", "")
    assert "camera=()" in headers.get("permissions-policy", "")


def test_rate_limiting_headers_on_api_endpoints(client):
    """Verify that API endpoints include rate limit diagnostic headers."""
    response = client.get("/api/v1/upazilas")
    assert response.status_code == 200
    assert "x-ratelimit-limit" in response.headers
    assert "x-ratelimit-remaining" in response.headers


def test_rate_limiting_enforcement_returns_429():
    """Verify that exceeding configured rate limit yields HTTP 429 RATE_LIMIT_EXCEEDED."""
    from fastapi import FastAPI
    from fastapi.responses import JSONResponse

    # Create isolated test app with a strict 2-request limit
    test_app = FastAPI()
    test_app.add_middleware(RateLimitMiddleware, requests_per_minute=2, enabled=True)

    @test_app.get("/test")
    def test_endpoint():
        return {"status": "ok"}

    test_client = TestClient(test_app)

    # First request: ok
    r1 = test_client.get("/test")
    assert r1.status_code == 200
    assert r1.headers.get("X-RateLimit-Remaining") == "1"

    # Second request: ok
    r2 = test_client.get("/test")
    assert r2.status_code == 200
    assert r2.headers.get("X-RateLimit-Remaining") == "0"

    # Third request: rejected with 429
    r3 = test_client.get("/test")
    assert r3.status_code == 429
    data = r3.json()
    assert data["code"] == "RATE_LIMIT_EXCEEDED"
    assert "Retry-After" in r3.headers


def test_payload_size_limit_returns_413():
    """Verify that request bodies exceeding max_bytes return HTTP 413 PAYLOAD_TOO_LARGE."""
    from fastapi import FastAPI

    # Create isolated test app with a tiny 100-byte limit
    test_app = FastAPI()
    test_app.add_middleware(RequestSizeLimitMiddleware, max_bytes=100)

    @test_app.post("/test-post")
    async def post_endpoint(payload: dict):
        return {"status": "ok"}

    test_client = TestClient(test_app)

    # Oversized payload
    large_body = {"data": "A" * 200}
    response = test_client.post("/test-post", json=large_body)
    assert response.status_code == 413
    assert response.json()["code"] == "PAYLOAD_TOO_LARGE"


def test_path_traversal_protection_in_repository():
    """Verify AgriculturalDataRepository rejects directory traversal and non-parquet file paths."""
    repo = AgriculturalDataRepository()

    # Traversal attempts
    with pytest.raises(ValueError, match="Path traversal"):
        repo.load_parquet_table("../../../etc/passwd")

    with pytest.raises(ValueError, match="Path traversal"):
        repo.load_parquet_table("..\\secrets.txt")

    # Non-parquet file
    with pytest.raises(ValueError, match="Unauthorized non-parquet"):
        repo.load_parquet_table("config.json")


def test_context_gating_safeguard_dec17(client):
    """Verify DEC-17 contextual gating blocks advisory generation without crop and stage."""
    # Missing both crop and stage
    resp1 = client.get("/api/v1/upazilas/BD-50-20-30/advisories")
    assert resp1.status_code == 422

    # Empty crop
    resp2 = client.get("/api/v1/upazilas/BD-50-20-30/advisories?crop=&stage=tillering")
    assert resp2.status_code == 422
    assert resp2.json()["code"] == "CONTEXT_GATING_FAILED"


def test_suppression_safeguard_dec10_stale_data(client):
    """Verify DEC-10 suppression safely flags advisory when weather data is older than 36 hours."""
    from datetime import datetime, timezone, timedelta
    stale_time = (datetime.now(timezone.utc) - timedelta(hours=48)).isoformat()
    payload = {
        "upazila_id": "BD-50-20-30",
        "crop_name": "Boro Rice",
        "growth_stage": "Tillering",
        "data_timestamp_utc": stale_time,
        "ensemble_spread_pct": 10.0,
        "rain_prob_pct": 20.0,
    }
    response = client.post("/api/v1/advisories/evaluate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["tier_4_recommendation"]["is_suppressed"] is True
    assert "36-hour" in data["tier_4_recommendation"]["suppression_reason"]


def test_suppression_safeguard_dec10_ensemble_uncertainty(client):
    """Verify DEC-10 suppression flags advisory when ensemble spread > 50% with rain prob 40-60%."""
    from datetime import datetime, timezone, timedelta
    fresh_time = (datetime.now(timezone.utc) - timedelta(hours=2)).isoformat()
    payload = {
        "upazila_id": "BD-50-20-30",
        "crop_name": "Boro Rice",
        "growth_stage": "Tillering",
        "data_timestamp_utc": fresh_time,
        "ensemble_spread_pct": 65.0,  # High spread > 50%
        "rain_prob_pct": 50.0,  # Ambiguous rain probability 40-60%
    }
    response = client.post("/api/v1/advisories/evaluate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["tier_4_recommendation"]["is_suppressed"] is True
    assert "ensemble spread" in data["tier_4_recommendation"]["suppression_reason"].lower()


def test_mandatory_field_verification_disclaimer_present(client):
    """Verify that all Tier 4 recommendations carry the mandatory Bengali disclaimer (DEC-10, AGENTS.md)."""
    response = client.get("/api/v1/upazilas/BD-50-20-30/advisories?crop=boro_rice&stage=tillering")
    assert response.status_code == 200
    data = response.json()
    rec = data["tier_4_recommendation"]

    # Verify mandatory disclaimer substring
    expected_disclaimer_phrase = "জমির আইল এবং মাটির রস নিজে হাত দিয়ে পরীক্ষা করুন"
    assert expected_disclaimer_phrase in rec["mandatory_disclaimer_bn"]


def test_anti_overconfidence_linguistic_standards(client):
    """Verify that prohibited overconfident terms are absent from advisory texts."""
    response = client.get("/api/v1/upazilas/BD-50-20-30/advisories?crop=boro_rice&stage=tillering")
    assert response.status_code == 200
    raw_text = response.text

    # Banned terms per AGENTS.md Section 3.4
    banned_terms = ["১০০% নিশ্চিত", "নিশ্চিত বৃষ্টি", "ফলনের নিশ্চয়তা"]
    for term in banned_terms:
        assert term not in raw_text, f"Prohibited overconfident term found: {term}"


def test_risk_evaluation_disclaimer_present(client):
    """Verify that physical hazard assessments carry the DEC-06 non-guarantee disclaimer."""
    payload = {
        "upazila_id": "BD-50-20-30",
        "crop_id": "boro_rice",
        "growth_stage": "Tillering",
    }
    response = client.post("/api/v1/risk/evaluate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "scientific_disclaimer_bn" in data
    assert "আর্থিক ক্ষতি বা চূড়ান্ত ফলন হ্রাসের নিশ্চয়তা দেয় না" in data["scientific_disclaimer_bn"]
