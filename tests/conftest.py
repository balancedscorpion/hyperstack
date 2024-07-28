import pytest
import hyperstack
from unittest.mock import Mock, patch

@pytest.fixture
def mock_api_key(monkeypatch):
    monkeypatch.setenv("HYPERSTACK_API_KEY", "mock-api-key")

@pytest.fixture
def mock_environments():
    with patch('hyperstack.api.environments') as mock_env:
        mock_env.create_environment = Mock()
        yield mock_env

@pytest.fixture
def mock_hyperstack(mock_api_key):
    with patch('hyperstack._hyperstack') as mock_instance:
        mock_instance._request = Mock()

        # Ensure the _request method can return different responses based on input
        def mock_request(method, endpoint, **kwargs):
            # Check if the request is for creating an environment and simulate a conflict
            if endpoint == "core/environments" and kwargs.get('json', {}).get('name') == "existing-env":
                response = Mock()
                response.status_code = 409
                response.json.return_value = {"message": "Environment name already exists"}
                response.raise_for_status.side_effect = requests.exceptions.HTTPError("409 Client Error: Conflict")
                return response
            else:
                # Default successful response mock
                response = Mock()
                response.status_code = 201
                response.json.return_value = {"id": "env-123", "name": kwargs.get('json', {}).get('name')}
                return response
        
        mock_instance._request.side_effect = mock_request
        yield mock_instance

@pytest.fixture
def hyperstack_client(mock_hyperstack):
    return hyperstack

@pytest.fixture(autouse=True)
def reset_environment(mock_hyperstack):
    yield
    mock_hyperstack.environment = None

@pytest.fixture
def hyperstack_client(mock_hyperstack):
    return hyperstack

@pytest.fixture
def mock_requests_post(mocker):
    return mocker.patch("requests.post")

@pytest.fixture
def mock_requests_get(mocker):
    return mocker.patch("requests.get")

@pytest.fixture
def mock_requests_delete(mocker):
    return mocker.patch("requests.delete")

@pytest.fixture
def mock_requests_put(mocker):
    return mocker.patch("requests.put")