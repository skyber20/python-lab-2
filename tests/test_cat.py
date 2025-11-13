import os
import pytest
from pyfakefs.fake_filesystem import FakeFilesystem
from src.main import run_command
from unittest.mock import Mock, patch
from src.exceptions import InvalidOption
from pathlib import Path


def test_cmd_cat(fs: FakeFilesystem, mock_print: Mock, mock_logger_info: Mock):
    fs.create_dir('test')
    fs.create_file('test/read_me.txt', contents="здесь точно что то написано. наверное")
    fs.create_file('test/okak.txt', contents="окак")
    fs.create_file('test/okak2.txt', contents="окак2")
    os.chdir('/test')

    run_command('cat', ['read_me.txt'])
    assert 'здесь точно что то написано. наверное' == mock_print.call_args_list[0].args[0]
    assert 'cat: OK' == mock_logger_info.call_args_list[0].args[0]

    run_command('cat', ['okak.txt', 'okak2.txt'])
    assert 'окак' == mock_print.call_args_list[1].args[0]
    assert 'окак2' == mock_print.call_args_list[2].args[0]
    assert 'cat: OK' == mock_logger_info.call_args_list[1].args[0]


def test_cmd_cat_errors(fs: FakeFilesystem, mock_print: Mock, mock_logger_error: Mock):
    fs.create_dir('test/in_test')
    fs.create_file('test/read_me.txt', contents="тун тун")
    fs.create_file('/test/random.pdf', contents=b'\xff\xfe\x00\x01')
    os.chdir('/test')

    run_command('cat', ['in_test'])
    assert 'in_test - Не текстовый файл' == mock_print.call_args_list[0].args[0]
    assert 'cat: Не OK' == mock_logger_error.call_args_list[0].args[0]

    run_command('cat', ['wddfnbeh'])
    assert 'Пути wddfnbeh не существует' == mock_print.call_args_list[1].args[0]
    assert 'cat: Не OK' == mock_logger_error.call_args_list[1].args[0]

    error = run_command('cat', ['-l'])[1]
    assert isinstance(error, InvalidOption)
    assert 'cat: Опция -l не поддерживается' == str(mock_print.call_args_list[2].args[0])
    assert 'cat: Опция -l не поддерживается' == mock_logger_error.call_args_list[2].args[0]

    with patch.object(Path, 'read_text', side_effect=UnicodeDecodeError):
        run_command('cat', ['/test/random.pdf'])
    assert '/test/random.pdf - Не текстовый файл' == mock_print.call_args_list[-1].args[0]
    assert 'cat: Не OK' == mock_logger_error.call_args_list[-1].args[0]
