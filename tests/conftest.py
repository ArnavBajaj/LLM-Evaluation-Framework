import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture(scope="session")
def api_client() -> TestClient:
    return TestClient(app)
