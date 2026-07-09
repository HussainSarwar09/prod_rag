import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client() -> TestClient:
    """
    Shared TestClient fixture for API tests.
    """
    return TestClient(app)
