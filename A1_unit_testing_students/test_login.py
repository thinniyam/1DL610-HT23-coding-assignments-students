import json
import pytest
from unittest import mock
from login import login


@pytest.fixture
def json_dump_mock(monkeypatch):
    # Create a MagicMock for json.dump
    mock_dump = mock.MagicMock()
    monkeypatch.setattr('json.dump', mock_dump)
    return mock_dump


@pytest.fixture
def registered_user():
    return {"username": "testuser", "password": "Test_Password", "wallet": 0}


@pytest.fixture
def login_open_users_file_stub(monkeypatch, registered_user):
    # Provide user file content for the login function
    read_data = json.dumps([registered_user])
    monkeypatch.setattr('builtins.open', mock.mock_open(read_data=read_data))


@pytest.mark.parametrize("user_inputs", [
    ("testuser", "Test_Password")
])
def test_successful_login(user_inputs, login_open_users_file_stub, json_dump_mock, capsys):
    # Run the login function
    with mock.patch('builtins.input', side_effect=user_inputs):
        login()

    json_dump_mock.assert_not_called()

    # Capture the printed output
    captured = capsys.readouterr()

    # Assert the output contains the expected message
    assert "Successfully logged in" in captured.out


@pytest.mark.parametrize("user_inputs", [
    ("testuser", "wrongpassword", "N"),
    ("wronguser", "Test_Password", "N"),
    ("testuser", "", "n"),
    ("", "Test_Password", "n")
])
def test_failed_login_and_dont_register(user_inputs, login_open_users_file_stub, json_dump_mock, capsys):
    # Run the login function
    with mock.patch('builtins.input', side_effect=user_inputs):
        login()

    json_dump_mock.assert_not_called()

    # Capture the printed output
    captured = capsys.readouterr()

    # Assert the output contains the expected message
    assert "Either username or password were incorrect" in captured.out


@pytest.mark.parametrize("user_inputs", [
    ("non_existing_user", "password", "Y", "Correct_New_Password"),
    ("non_existing_user", "", "Y", "8Letter$")
])
def test_failed_login_and_register_successfully(user_inputs, login_open_users_file_stub, json_dump_mock, capsys):
    # Run the login function
    with mock.patch('builtins.input', side_effect=user_inputs):
        login()

    json_dump_mock.assert_called_once()

    # Capture the printed output
    captured = capsys.readouterr()

    # Assert the output contains the expected message
    assert "Either username or password were incorrect" in captured.out
    assert "Successfully registered" in captured.out


@pytest.mark.parametrize("user_inputs", [
    ("non_existing_user", "password", "Y", "password_missing_capital_letter", "Correct_New_Password"),
    ("non_existing_user", "password", "Y", "PasswordMissingSpecialCharacter", "Correct_New_Password"),
    ("non_existing_user", "password", "Y", "7L%tter", "Correct_New_Password"),
    ("non_existing_user", "password", "Y", "password_missing_capital_letter", "PasswordMissingSpecialCharacter", "Pw$hort", "Correct_New_Password")
])
def test_failed_login_and_retry_register(user_inputs, login_open_users_file_stub, json_dump_mock, capsys):
    # Run the login function
    with mock.patch('builtins.input', side_effect=user_inputs):
        login()

    json_dump_mock.assert_called_once()

    # Capture the printed output
    captured = capsys.readouterr()

    # Assert the output contains the expected message
    assert "Either username or password were incorrect" in captured.out
    assert "Password must have at least 1 capital letter, 1 special symbol and be 8 characters long." in captured.out
    assert "Successfully registered" in captured.out

