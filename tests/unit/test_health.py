"""Tests for health check endpoint."""

from fastapi.testclient import TestClient

from nuhoot.main import app


class TestHealthCheck:
    def test_health_returns_200(self):
        client = TestClient(app)
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_returns_healthy_status(self):
        client = TestClient(app)
        response = client.get("/health")
        assert response.json()["status"] == "healthy"

    def test_health_returns_service_name(self):
        client = TestClient(app)
        response = client.get("/health")
        assert response.json()["service"] == "nuhoot"
