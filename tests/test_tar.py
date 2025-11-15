import os
from pyfakefs.fake_filesystem import FakeFilesystem
from src.main import run_command
from unittest.mock import Mock
from src.exceptions import PathNotExists, EmptyDir, InvalidAmountArguments, IsNotDir


def test_cmd_tar(fs: FakeFilesystem, mock_logger_info: Mock):
    fs.create_dir('folder_to_tar/test')
    fs.create_dir('folder_to_tar/test2')
    fs.create_file('folder_to_tar/test/test_file.txt')
    os.chdir('/')

    run_command('tar', ['folder_to_tar', 'folder_tar'])
    assert os.path.exists('/folder_tar.tar.gz')
    assert 'tar: OK' in mock_logger_info.call_args_list[-1].args[0]


def test_cmd_tar_errors(fs: FakeFilesystem, mock_logger_error: Mock, mock_print: Mock):
    fs.create_dir('folder_to_tar/test')
    fs.create_dir('folder_to_tar2/test')
    fs.create_file('folder_to_tar2/test/file.txt', contents='smth')
    fs.create_file('path/in_folder')
    fs.create_file('file.txt')
    os.chdir('/')

    error = run_command('tar', ['folder_to_tar'])[1]
    assert isinstance(error, InvalidAmountArguments)
    assert 'tar: Некорректное количество аргументов' in str(mock_print.call_args_list[-1].args[0])
    assert 'tar: Некорректное количество аргументов' in mock_logger_error.call_args_list[-1].args[0]

    error = run_command('tar', ['file.txt', 'ewfefd'])[1]
    assert isinstance(error, IsNotDir)
    assert 'tar: file.txt - Не папка' in str(mock_print.call_args_list[-1].args[0])
    assert 'tar: file.txt - Не папка' in mock_logger_error.call_args_list[-1].args[0]

    error = run_command('tar', ['folder_to_tar', 'folder_tar'])[1]
    assert isinstance(error, EmptyDir)
    assert 'tar: folder_to_tar - Папка пуста' in str(mock_print.call_args_list[-1].args[0])
    assert 'tar: folder_to_tar - Папка пуста' in mock_logger_error.call_args_list[-1].args[0]

    error = run_command('tar', ['folder_to_tar2', 'path2/in_folder'])[1]
    assert isinstance(error, PathNotExists)
    assert 'path2 не существует' in str(mock_print.call_args_list[-1].args[0])
    assert 'path2 не существует' in mock_logger_error.call_args_list[-1].args[0]
