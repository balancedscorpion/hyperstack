import pytest
from hyperstack import Hyperstack

@pytest.fixture
def mock_api_key(monkeypatch):
    monkeypatch.setenv("HYPERSTACK_API_KEY", "mock-api-key")

@pytest.fixture
def hyperstack_client(mock_api_key):
    return Hyperstack()

@pytest.fixture
def mock_requests_post(mocker):
    return mocker.patch("requests.post")

@pytest.fixture
def mock_requests_get(mocker):
    return mocker.patch("requests.get")

@pytest.fixture
def mock_requests_delete(mocker):
    return mocker.patch("requests.delete")