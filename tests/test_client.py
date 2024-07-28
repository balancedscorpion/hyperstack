import pytest
import requests
from unittest.mock import patch, MagicMock
from hyperstack import Hyperstack
import hyperstack
from conftest import MockHyperstack

def test_init(mock_hyperstack):
    assert isinstance(mock_hyperstack, Hyperstack)
    assert mock_hyperstack.api_key == "mock_api_key"
    assert mock_hyperstack.base_url == "https://mock-api.example.com/v1/"
    assert mock_hyperstack.headers["api_key"] == "mock_api_key"

def test_singleton():
    assert isinstance(hyperstack._hyperstack, MockHyperstack)
    assert hyperstack._hyperstack.api_key == "mock_api_key"


def test_get_method(mock_hyperstack):
    result = mock_hyperstack.get("test_endpoint")
    assert result == {"status": "success", "data": {}}

def test_post_method(mock_hyperstack):
    result = mock_hyperstack.post("test_endpoint", data={"key": "value"})
    assert result == {"status": "success", "data": {}}

def test_put_method(mock_hyperstack):
    result = mock_hyperstack.put("test_endpoint", data={"key": "value"})
    assert result == {"status": "success", "data": {}}

def test_delete_method(mock_hyperstack):
    result = mock_hyperstack.delete("test_endpoint")
    assert result == {"status": "success", "data": {}}

@pytest.fixture
def mock_env_api_key():
    with patch.dict('os.environ', {'HYPERSTACK_API_KEY': 'test_api_key'}):
        yield

def test_hyperstack_init(mock_env_api_key):
    hs = Hyperstack()
    assert hs.api_key == 'test_api_key'
    assert hs.base_url == "https://infrahub-api.nexgencloud.com/v1/"
    assert hs.headers == {
        "Content-Type": "application/json",
        "api_key": "test_api_key"
    }

def test_hyperstack_init_no_api_key():
    with patch.dict('os.environ', clear=True):
        with pytest.raises(EnvironmentError, match="HYPERSTACK_API_KEY environment variable not set"):
            Hyperstack()

def test_check_environment_set():
    hs = Hyperstack()
    hs.environment = None
    with pytest.raises(EnvironmentError, match="Environment is not set"):
        hs._check_environment_set()

    hs.environment = "test_env"
    hs._check_environment_set()  # Should not raise an error

@patch('requests.request')
def test_request(mock_request):
    mock_response = MagicMock()
    mock_response.raise_for_status.return_value = None
    mock_request.return_value = mock_response

    hs = Hyperstack()
    hs._request("GET", "test_endpoint")

    mock_request.assert_called_once_with(
        "GET",
        "https://infrahub-api.nexgencloud.com/v1/test_endpoint",
        headers=hs.headers
    )

@patch('requests.request')
def test_request_error(mock_request):
    mock_request.side_effect = requests.RequestException("Test error")

    hs = Hyperstack()
    with pytest.raises(requests.RequestException, match="Test error"):
        hs._request("GET", "test_endpoint")

@patch('hyperstack.client.Hyperstack._request')
def test_http_methods(mock_request):
    mock_response = MagicMock()
    mock_response.content = b'{"key": "value"}'
    mock_request.return_value = mock_response

    hs = Hyperstack()

    assert hs.get("test_endpoint") == {"key": "value"}
    mock_request.assert_called_with("GET", "test_endpoint")

    assert hs.post("test_endpoint", data={"test": "data"}) == {"key": "value"}
    mock_request.assert_called_with("POST", "test_endpoint", json={"test": "data"})

    assert hs.put("test_endpoint", data={"test": "data"}) == {"key": "value"}
    mock_request.assert_called_with("PUT", "test_endpoint", json={"test": "data"})

    assert hs.delete("test_endpoint") == {"key": "value"}
    mock_request.assert_called_with("DELETE", "test_endpoint")

# Add a new test for the PUT method specifically
@patch('hyperstack.client.Hyperstack._request')
def test_put_method(mock_request):
    mock_response = MagicMock()
    mock_response.content = b'{"key": "value"}'
    mock_request.return_value = mock_response

    hs = Hyperstack()
    result = hs.put("test_endpoint", data={"test": "data"})

    assert result == {"key": "value"}
    mock_request.assert_called_once_with("PUT", "test_endpoint", json={"test": "data"})

@patch('hyperstack.client.Hyperstack._request')
def test_http_methods(mock_request):
    mock_response = MagicMock()
    mock_response.content = b'{"key": "value"}'
    mock_request.return_value = mock_response

    hs = Hyperstack()

    assert hs.get("test_endpoint") == {"key": "value"}
    mock_request.assert_called_with("GET", "test_endpoint")

    assert hs.post("test_endpoint", data={"test": "data"}) == {"key": "value"}
    mock_request.assert_called_with("POST", "test_endpoint", json={"test": "data"})

    assert hs.put("test_endpoint", data={"test": "data"}) == {"key": "value"}
    mock_request.assert_called_with("PUT", "test_endpoint", json={"test": "data"})

    assert hs.delete("test_endpoint") == {"key": "value"}
    mock_request.assert_called_with("DELETE", "test_endpoint")

@patch('requests.request')
def test_request_error(mock_request):
    mock_request.side_effect = requests.RequestException("Test error")

    hs = Hyperstack()
    with pytest.raises(requests.RequestException, match="Test error"):
        hs._request("GET", "test_endpoint")