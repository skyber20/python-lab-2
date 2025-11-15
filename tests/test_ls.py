import os
import time
from pyfakefs.fake_filesystem import FakeFilesystem
from src.main import run_command
from unittest.mock import Mock
from datetime import datetime
from src.exceptions import InvalidAmountArguments, InvalidOption


def test_cmd_ls_without_l(fs: FakeFilesystem, mock_print: Mock, mock_logger_info: Mock):
    fs.create_file('folder/test.txt', contents='можно высокий балл пжпжпжпжпж')
    fs.create_file('folder/test2.txt')
    fs.create_dir('folder/in_folder')
    os.chdir('/folder')

    # Текущий путь - /folder
    run_command('ls', [])
    assert all(i in mock_print.call_args_list[0].args[0] for i in ['test.txt', 'test2.txt', 'in_folder'])
    assert 'ls: OK' in mock_logger_info.call_args_list[0].args[0]

    os.chdir('/')
    run_command('ls', ['/folder'])
    assert all(i in mock_print.call_args_list[0].args[0] for i in ['test.txt', 'test2.txt', 'in_folder'])
    assert 'ls: OK' in mock_logger_info.call_args_list[0].args[0]


def test_cmd_ls_with_l(fs: FakeFilesystem, mock_print: Mock, mock_logger_info: Mock):
    fs.create_file('folder/test.txt',)
    fs.create_dir('folder/in_folder')

    file_path = '/folder/test.txt'
    file_obj = fs.get_object(file_path)
    file_obj.st_size = 1024
    file_obj.st_mode = 0o100644
    file_obj.st_mtime = time.mktime(datetime(2025, 11, 15, 12, 30).timetuple())

    dir_path = '/folder/in_folder'
    dir_obj = fs.get_object(dir_path)
    dir_obj.st_mode = 0o40755
    dir_obj.st_mtime = time.mktime(datetime(2025, 11, 15, 12, 45).timetuple())

    os.chdir('/')

    run_command('ls', ['folder', '-l'])

    # [:-1] так как последний вызов принт - print(), нужный только для переноса на след строку
    output = '\n'.join(call.args[0] for call in mock_print.call_args_list[:-1])

    assert 'test.txt' in output
    assert '12:30' in output
    assert '-rw-r--r--' in output
    assert 'in_folder' in output
    assert '1024' in output
    assert 'ls: OK' in mock_logger_info.call_args_list[-1].args[0]


def test_cmd_ls_errors(fs: FakeFilesystem, mock_print: Mock, mock_logger_error: Mock):
    fs.create_file('folder/test.txt')
    fs.create_file('folder/test2.txt')
    fs.create_dir('folder/in_folder')
    os.chdir('/folder')

    error = run_command('ls', ['folder', '-l', '-r'])[1]
    assert isinstance(error, InvalidAmountArguments)
    assert 'ls: Некорректное количество аргументов' in str(mock_print.call_args_list[-1].args[0])
    assert 'ls: Некорректное количество аргументов' in mock_logger_error.call_args_list[-1].args[0]

    error = run_command('ls', ['folder', '-f'])[1]
    assert isinstance(error, InvalidOption)
    assert 'ls: Опция -f не поддерживается' in str(mock_print.call_args_list[-1].args[0])
    assert 'ls: Опция -f не поддерживается' in mock_logger_error.call_args_list[-1].args[0]

    run_command('ls', ['not_exist_path'])
    assert 'not_exist_path: Нет такого пути' in mock_print.call_args_list[-1].args[0]
    assert 'ls: Не OK' in mock_logger_error.call_args_list[-1].args[0]
