import os
import pytest
from pyfakefs.fake_filesystem import FakeFilesystem
from src.main import run_command
from unittest.mock import Mock
from src.exceptions import InvalidAmountArguments, PathNotExists, IsNotDir


def test_without_args_and_wave(mock_logger_info: Mock):
    run_command('cd', [])
    assert os.getcwd() == os.path.expanduser('~')
    run_command('cd', ['~'])
    assert os.getcwd() == os.path.expanduser('~')
    assert all('cd: OK' == args[0] for args, _ in mock_logger_info.call_args_list)


def test_cmd_cd(fs: FakeFilesystem, mock_logger_info: Mock):
    fs.create_dir('test/in_test')

    run_command('cd', ['test'])
    assert os.getcwd() == os.path.join(os.path.abspath('/'), 'test')
    run_command('cd', ['.'])
    assert os.getcwd() == os.path.join(os.path.abspath('/'), 'test')
    run_command('cd', ['..'])
    assert os.getcwd() == os.path.abspath('/')
    run_command('cd', ['/test/in_test'])
    assert os.getcwd() == os.path.join(os.path.abspath('/'), 'test', 'in_test')

    assert all('cd: OK' == args[0] for args, _ in mock_logger_info.call_args_list)


def test_cmd_cd_errors(fs: FakeFilesystem, mock_logger_error: Mock, mock_print: Mock):
    fs.create_dir('test')
    fs.create_file('test/smth.txt')

    success1, error1 = run_command('cd', ['abcdababa'])
    success2, error2 = run_command('cd', ['test/smth.txt'])
    success3, error3 = run_command('cd', ['/test', '/'])

    assert isinstance(error1, PathNotExists)
    assert isinstance(error2, IsNotDir)
    assert isinstance(error3, InvalidAmountArguments)

    assert 'cd: Пути abcdababa не существует' == str(mock_print.call_args_list[0].args[0])
    assert 'cd: smth.txt - Не папка' == str(mock_print.call_args_list[1].args[0])
    assert 'cd: Некорректное количество аргументов' == str(mock_print.call_args_list[2].args[0])

    assert 'cd: Пути abcdababa не существует' == mock_logger_error.call_args_list[0].args[0]
    assert 'cd: smth.txt - Не папка' == mock_logger_error.call_args_list[1].args[0]
    assert 'cd: Некорректное количество аргументов' == mock_logger_error.call_args_list[2].args[0]

