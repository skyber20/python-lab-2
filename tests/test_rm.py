import os
from pyfakefs.fake_filesystem import FakeFilesystem
from src.main import run_command
from unittest.mock import Mock, patch
from src.exceptions import InvalidAmountPaths, InvalidOption


def test_del_important_data(fs: FakeFilesystem, mock_print: Mock):
    fs.create_dir('test/in_test/in_in_test')
    fs.create_dir('test2')
    fs.create_file('test2/smth.txt')
    os.chdir('/test/in_test')

    run_command('rm', ['.', '..', '/', '-r'])
    assert 'Невозможно удалить текущий и корневой каталоги' in mock_print.call_args_list[0].args[0]
    assert 'Невозможно удалить родительскую папку' in mock_print.call_args_list[1].args[0]
    assert 'Невозможно удалить текущий и корневой каталоги' in mock_print.call_args_list[2].args[0]


def test_cmd_rm(fs: FakeFilesystem, mock_logger_info: Mock):
    fs.create_dir('test/in_test/in_in_test')
    fs.create_dir('test2')
    fs.create_dir('test3')
    fs.create_file('test2/smth.txt')
    fs.create_dir('/tmp_trash')
    os.chdir('/')

    with patch('builtins.input', return_value='y'), \
            patch('src.commands.command_rm.create_trash', return_value='/tmp_trash'):
        assert os.path.exists('test2/smth.txt')
        run_command('rm', ['test2/smth.txt'])
        assert not os.path.exists('test2/smth.txt')
        assert 'rm: OK' in mock_logger_info.call_args_list[-1].args[0]

        assert os.path.exists('test3')
        run_command('rm', ['test3', '-r'])
        assert not os.path.exists('test3')
        assert 'rm: OK' in mock_logger_info.call_args_list[-1].args[0]

    with patch('builtins.input', return_value='n'),\
            patch('src.commands.command_rm.create_trash', return_value='/tmp_trash'):
        assert os.path.exists('test/in_test/in_in_test')
        run_command('rm', ['test/in_test/in_in_test', '-r'])
        assert os.path.exists('test/in_test/in_in_test')
        assert 'rm: OK' in mock_logger_info.call_args_list[-1].args[0]


def test_cmd_rm_errors(fs: FakeFilesystem, mock_logger_error: Mock, mock_print):
    fs.create_dir('test/in_test/in_in_test')
    fs.create_dir('test2')
    fs.create_dir('test3')
    fs.create_file('test2/smth.txt')
    fs.create_dir('/tmp_trash')
    os.chdir('/')

    with patch('builtins.input', return_value='y'), \
            patch('src.commands.command_rm.create_trash', return_value='/tmp_trash'):
        error = run_command('rm', ['-r'])[1]
        assert isinstance(error, InvalidAmountPaths)
        assert 'rm: Некорректное количество путей' in str(mock_print.call_args_list[-1].args[0])
        assert 'rm: Некорректное количество путей' in mock_logger_error.call_args_list[-1].args[0]

        error = run_command('rm', ['test2', '-l'])[1]
        assert isinstance(error, InvalidOption)
        assert 'rm: Опция -l не поддерживается' in str(mock_print.call_args_list[-1].args[0])
        assert 'rm: Опция -l не поддерживается' in mock_logger_error.call_args_list[-1].args[0]

        run_command('rm', ['test2'])
        assert 'Для удаления папки нужна опция -r' in str(mock_print.call_args_list[-1].args[0])
        assert 'rm: Не OK' in mock_logger_error.call_args_list[-1].args[0]
