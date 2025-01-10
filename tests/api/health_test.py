import pytest
from fastapi.testclient import TestClient
from teleAgent.main import create_app

@pytest.fixture
def client():
    """Test client fixture"""
    app = create_app()
    return TestClient(app)

@pytest.mark.integration
def test_health_check(client):
    """Test health check endpoint"""
    response = client.get("/api/health")
    
    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "message": "Service is healthy"
    }