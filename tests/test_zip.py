import os
from pyfakefs.fake_filesystem import FakeFilesystem
from src.main import run_command
from unittest.mock import Mock
from src.exceptions import PathNotExists, EmptyDir, InvalidAmountArguments, IsNotDir


def test_cmd_zip(fs: FakeFilesystem, mock_logger_info: Mock):
    fs.create_dir('folder_to_zip/test')
    fs.create_dir('folder_to_zip/test2')
    fs.create_file('folder_to_zip/test/test_file.txt')
    os.chdir('/')

    run_command('zip', ['folder_to_zip', 'folder_zip'])
    assert os.path.exists('/folder_zip.zip')
    assert 'zip: OK' in mock_logger_info.call_args_list[-1].args[0]


def test_cmd_zip_errors(fs: FakeFilesystem, mock_logger_error: Mock, mock_print: Mock):
    fs.create_dir('folder_to_zip/test')
    fs.create_dir('folder_to_zip2/test')
    fs.create_file('folder_to_zip2/test/file.txt', contents='smth')
    fs.create_file('path/in_folder')
    fs.create_file('file.txt')
    os.chdir('/')

    error = run_command('zip', ['folder_to_zip'])[1]
    assert isinstance(error, InvalidAmountArguments)
    assert 'zip: Некорректное количество аргументов' in str(mock_print.call_args_list[-1].args[0])
    assert 'zip: Некорректное количество аргументов' in mock_logger_error.call_args_list[-1].args[0]

    error = run_command('zip', ['file.txt', 'ewfefd'])[1]
    assert isinstance(error, IsNotDir)
    assert 'zip: file.txt - Не папка' in str(mock_print.call_args_list[-1].args[0])
    assert 'zip: file.txt - Не папка' in mock_logger_error.call_args_list[-1].args[0]

    error = run_command('zip', ['folder_to_zip', 'folder_zip'])[1]
    assert isinstance(error, EmptyDir)
    assert 'zip: folder_to_zip - Папка пуста' in str(mock_print.call_args_list[-1].args[0])
    assert 'zip: folder_to_zip - Папка пуста' in mock_logger_error.call_args_list[-1].args[0]

    error = run_command('zip', ['folder_to_zip2', 'path2/in_folder'])[1]
    assert isinstance(error, PathNotExists)
    assert 'path2 не существует' in str(mock_print.call_args_list[-1].args[0])
    assert 'path2 не существует' in mock_logger_error.call_args_list[-1].args[0]
