from unittest.mock import patch

import pytest

from hyperstack.api.stock import retrieve_gpu_stock


@pytest.fixture
def mock_hyperstack():
    with patch('hyperstack.Hyperstack') as MockHyperstack:
        mock_instance = MockHyperstack.return_value
        mock_instance.get.return_value = {"status": "success", "data": {"gpu_stock": []}}
        yield mock_instance


def test_retrieve_gpu_stock(mock_hyperstack):
    result = retrieve_gpu_stock(mock_hyperstack)
    mock_hyperstack.get.assert_called_once_with("core/stocks")
    assert result == {"status": "success", "data": {"gpu_stock": []}}
