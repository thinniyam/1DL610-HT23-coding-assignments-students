import pytest
from unittest.mock import patch
from products import searchAndBuyProduct

@pytest.fixture
def input_stub(mocker):
    def input_side_effect(prompt):
        if "Search for products" in prompt:
            return "all"
        elif "Ready to shop" in prompt:
            return "Y"
    return mocker.patch('builtins.input', side_effect=input_side_effect)

@pytest.fixture
def login_stub(mocker):
    return mocker.patch('products.login', return_value={"username": "Ramanathan", "wallet": 100 })

@pytest.fixture
def checkoutAndPayment_stub(mocker):
    return mocker.patch('products.checkoutAndPayment', return_value=None)

@pytest.fixture
def display_csv_as_table_stub(mocker):
    return mocker.patch('products.display_csv_as_table', return_value=None)

@pytest.mark.parametrize("user_inputs", [("Ramanathan", "Notaproblem23*", "all", "Y", "l")])
def test_with_stub(input_stub, login_stub, checkoutAndPayment_stub, display_csv_as_table_stub, user_inputs):
    with patch('builtins.input', side_effect=user_inputs):
        searchAndBuyProduct()

    checkoutAndPayment_stub.assert_called_once_with({"username": "Ramanathan", "wallet": 100 })
    login_stub.assert_called_once()
