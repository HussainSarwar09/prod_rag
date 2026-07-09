import pytest
from fastapi.testclient import TestClient

pytestmark = pytest.mark.unit

def test_root_endpoint(client: TestClient) -> None:
    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert data["application"] == "Production RAG"
    assert data["version"] == "0.1.0"


def test_health_endpoint(client: TestClient) -> None:
    response = client.get("/api/v1/health")

    assert response.status_code == 200

    assert response.json() == {
        "status": "healthy"
    }