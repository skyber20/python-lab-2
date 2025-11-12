import pytest
from unittest.mock import Mock
from pytest_mock import MockerFixture
from pyfakefs.fake_filesystem import FakeFilesystem


@pytest.fixture
def fake_logger(mocker: MockerFixture) -> Mock:
    mock_logger = mocker.patch('utils.my_logger.logger.info')
    return mock_logger


@pytest.fixture
def fake_logger(mocker: MockerFixture) -> Mock:
    mock_logger = mocker.patch('utils.my_logger.logger.info')
