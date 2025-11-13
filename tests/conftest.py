import pytest
from pytest_mock import MockerFixture
from unittest.mock import Mock


@pytest.fixture
def mock_print(mocker: MockerFixture) -> Mock:
    return mocker.patch('builtins.print')


@pytest.fixture
def mock_logger_info(mocker: MockerFixture) -> Mock:
    return mocker.patch('utils.my_logger.logger.info')


@pytest.fixture
def mock_logger_error(mocker: MockerFixture) -> Mock:
    return mocker.patch('utils.my_logger.logger.error')
