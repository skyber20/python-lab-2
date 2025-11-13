import os
import pytest
from pyfakefs.fake_filesystem import FakeFilesystem
from src.main import run_command
from unittest.mock import Mock
from src.exceptions import InvalidAmountPaths, InvalidOption, PathNotExists


def test_cmd_cp(fs: FakeFilesystem, mock_logger_info: Mock):
    fs.create_dir('test')
    fs.create_dir('test2')
    fs.create_dir('test3')
    fs.create_file('test/file_in.txt', contents='тест')
    os.chdir('/')

    run_command('cp', ['test/file_in.txt', 'test2'])
    assert os.path.exists('test/file_in.txt') == os.path.exists('test2/file_in.txt')
    assert 'cp: OK' == mock_logger_info.call_args_list[-1].args[0]

    run_command('cp', ['test3', 'test', '-r'])
    assert os.path.exists('test') == os.path.exists('test/test3')
    assert 'cp: OK' == mock_logger_info.call_args_list[-1].args[0]

    run_command('cp', ['test3', 'test/file_in.txt', 'test', '-r'])
    assert os.path.exists('test') == os.path.exists('test/file_in.txt') == os.path.exists('test/test3')
    assert 'cp: OK' == mock_logger_info.call_args_list[-1].args[0]


def test_cmd_cp_errors(fs: FakeFilesystem, mock_logger_error: Mock, mock_print: Mock):
    fs.create_dir('test')
    fs.create_dir('test2')
    fs.create_dir('test3')
    fs.create_file('test/file_in.txt', contents='тест')
    os.chdir('/')

    error = run_command('cp', ['test/file_in.txt'])[1]
    assert isinstance(error, InvalidAmountPaths)
    assert 'cp: Некорректное количество путей' == str(mock_print.call_args_list[-1].args[0])
    assert 'cp: Некорректное количество путей' == str(mock_logger_error.call_args_list[-1].args[0])

    error = run_command('cp', ['test/file_in.txt', 'test2', '-f'])[1]
    assert isinstance(error, InvalidOption)
    assert 'cp: Опция -f не поддерживается' == str(mock_print.call_args_list[-1].args[0])
    assert 'cp: Опция -f не поддерживается' == str(mock_logger_error.call_args_list[-1].args[0])

    error = run_command('cp', ['test/file_in.txt', 'test4/in_test4', '-r'])[1]
    assert isinstance(error, PathNotExists)
    assert 'cp: Пути C:\\test4 не существует' == str(mock_print.call_args_list[-1].args[0])
    assert 'cp: Пути C:\\test4 не существует' == str(mock_logger_error.call_args_list[-1].args[0])

    run_command('cp', ['test', 'test2'])
    assert 'Для копирования папки нужна опция -r' == str(mock_print.call_args_list[-1].args[0])
