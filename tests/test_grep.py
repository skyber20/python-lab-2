import os
from pyfakefs.fake_filesystem import FakeFilesystem
from src.main import run_command
from unittest.mock import Mock
from src.exceptions import PathNotExists, InvalidAmountArguments, InvalidOption


def test_cmd_grep(fs: FakeFilesystem, mock_logger_info: Mock, mock_print: Mock):
    fs.create_file('folder_for_search/in1/test.txt', contents='HelLo WOrld!!')
    fs.create_file('folder_for_search/in2/test3.txt', contents='окакHELLOмир!\nHello Again!')
    fs.create_file('folder_for_search/in3/test4.txt', contents='something text')
    os.chdir('/')

    run_command('grep', ['heLlO', 'folder_for_search', '-i', '-r'])
    assert 'test.txt:1:HelLo WOrld!!' in mock_print.call_args_list[0].args[0]
    assert 'test3.txt:1:окакHELLOмир!' in mock_print.call_args_list[1].args[0]
    assert 'test3.txt:2:Hello Again!' in mock_print.call_args_list[2].args[0]
    assert 'grep: OK' in mock_logger_info.call_args_list[0].args[0]

    run_command('grep', ['HELLO', 'folder_for_search', '-r'])
    assert 'test3.txt:1:окакHELLOмир!' in mock_print.call_args_list[3].args[0]
    assert 'grep: OK' in mock_logger_info.call_args_list[1].args[0]

    run_command('grep', ['smth', 'folder_for_search', '-i', '-r'])
    assert 'Не удалось найти строки, содержащие pattern: smth' in mock_print.call_args_list[4].args[0]


def test_cmd_grep_errors(fs: FakeFilesystem, mock_logger_error: Mock, mock_print: Mock):
    fs.create_file('folder_for_search/in1/test.txt', contents='HelLo WOrld!!')
    fs.create_file('folder_for_search/in2/test3.txt', contents='окакHELLOмир!\nHello Again!')
    fs.create_file('folder_for_search/in3/test4.txt', contents='something text')
    os.chdir('/')

    error = run_command('grep', ['heLlO'])[1]
    assert isinstance(error, InvalidAmountArguments)
    assert 'grep: Некорректное количество аргументов' in str(mock_print.call_args_list[-1].args[0])
    assert 'grep: Некорректное количество аргументов' in mock_logger_error.call_args_list[-1].args[0]

    error = run_command('grep', ['HELLO', 'not_exist_folder', '-r'])[1]
    assert isinstance(error, PathNotExists)
    assert 'grep: Пути not_exist_folder не существует' in str(mock_print.call_args_list[-1].args[0])
    assert 'grep: Пути not_exist_folder не существует' in mock_logger_error.call_args_list[-1].args[0]

    error = run_command('grep', ['HELLO', 'folder_for_search', '-r', '-l'])[1]
    assert isinstance(error, InvalidOption)
    assert 'grep: Опция -l не поддерживается' in str(mock_print.call_args_list[-1].args[0])
    assert 'grep: Опция -l не поддерживается' in mock_logger_error.call_args_list[-1].args[0]

    run_command('grep', ['hello', 'folder_for_search', '-i'])
    assert 'grep: Нужна опция -r для поиска внутри директории' in mock_print.call_args_list[-1].args[0]
    assert 'grep: Нужна опция -r для поиска внутри директории' in mock_logger_error.call_args_list[-1].args[0]
