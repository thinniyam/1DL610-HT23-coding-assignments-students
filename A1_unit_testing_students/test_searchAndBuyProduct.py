import pytest
from unittest.mock import patch
from products import searchAndBuyProduct

@pytest.fixture
def login_stub(mocker):
    return mocker.patch('products.login', return_value={"username": "Ramanathan", "wallet": 100 })

@pytest.fixture
def checkoutAndPayment_stub(mocker):
    return mocker.patch('products.checkoutAndPayment', return_value=None)

@pytest.fixture
def display_csv_as_table_stub(mocker):
    return mocker.patch('products.display_csv_as_table', return_value=None)

@pytest.fixture
def display_filtered_table_stub(mocker):
    return mocker.patch('products.display_filtered_table', return_value=None)

@pytest.mark.parametrize("user_inputs", [("all", "Y")])
def test_with_stubs1(login_stub, checkoutAndPayment_stub, display_csv_as_table_stub, display_filtered_table_stub, user_inputs):
    with patch('builtins.input', side_effect=user_inputs):
        searchAndBuyProduct()

    login_stub.assert_called_once()
    display_csv_as_table_stub.assert_called_once()
    display_filtered_table_stub.assert_not_called()
    checkoutAndPayment_stub.assert_called_once_with({"username": "Ramanathan", "wallet": 100 })

