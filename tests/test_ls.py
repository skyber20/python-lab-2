import pytest
import os
from pyfakefs.fake_filesystem import FakeFilesystem
from unittest.mock import patch
from src import exceptions
from src.commands.command_ls import run_ls


def test_current_directory_without_options(fs: FakeFilesystem):
    fs.create_file('/test/test.txt', contents='что то')
    fs.create_file('/test/test2.txt', contents='что то')
    fs.create_file('/test/test_folder/in_test_folder')

    os.chdir('/test')

    with patch('builtins.print') as mock_print:
        run_ls([])
        assert mock_print.called
