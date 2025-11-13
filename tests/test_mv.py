import os
import pytest
from pyfakefs.fake_filesystem import FakeFilesystem
from src.main import run_command
from unittest.mock import Mock
from src.exceptions import InvalidAmountPaths, InvalidAmountOptions, PathNotExists


def test_cmd_mv(fs: FakeFilesystem, mock_logger_info: Mock):
    fs.create_dir('test')
    fs.create_dir('test2')
    fs.create_dir('test3')
    fs.create_file('test/file_in.txt', contents='тест')
    os.chdir('/')

    run_command('mv', ['test/file_in.txt', 'test2'])
    assert (not os.path.exists('test/file_in.txt')) == os.path.exists('test2/file_in.txt')
    assert 'mv: OK' == mock_logger_info.call_args_list[-1].args[0]

    run_command('mv', ['test3', 'test'])
    assert (not os.path.exists('test3')) == os.path.exists('test/test3')
    assert 'mv: OK' == mock_logger_info.call_args_list[-1].args[0]

    run_command('mv', ['test3', 'test2/file_in.txt', 'test'])
    assert (not os.path.exists('test3')) == (not os.path.exists('test2/file_in.txt')) == os.path.exists('test/test3') \
           == os.path.exists('test/file_in.txt')
    assert 'mv: OK' == mock_logger_info.call_args_list[-1].args[0]


def test_cmd_mv_errors(fs: FakeFilesystem, mock_logger_error: Mock, mock_print: Mock):
    fs.create_dir('test')
    fs.create_dir('test2')
    fs.create_dir('test3')
    fs.create_file('test/file_in.txt', contents='тест')
    os.chdir('/')

    error = run_command('mv', ['test/file_in.txt'])[1]
    assert isinstance(error, InvalidAmountPaths)
    assert 'mv: Некорректное количество путей' == str(mock_print.call_args_list[-1].args[0])
    assert 'mv: Некорректное количество путей' == str(mock_logger_error.call_args_list[-1].args[0])

    error = run_command('mv', ['test/file_in.txt', 'test2', '-r'])[1]
    assert isinstance(error, InvalidAmountOptions)
    assert 'mv: Некорректное количество опций' == str(mock_print.call_args_list[-1].args[0])
    assert 'mv: Некорректное количество опций' == str(mock_logger_error.call_args_list[-1].args[0])

    error = run_command('mv', ['test/file_in.txt', 'test4/in_test4'])[1]
    assert isinstance(error, PathNotExists)
    assert 'mv: Пути C:\\test4 не существует' == str(mock_print.call_args_list[-1].args[0])
    assert 'mv: Пути C:\\test4 не существует' == str(mock_logger_error.call_args_list[-1].args[0])
