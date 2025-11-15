import os
from pyfakefs.fake_filesystem import FakeFilesystem
from src.main import run_command
from unittest.mock import Mock, patch


def test_cmd_undo(fs: FakeFilesystem, mock_logger_info: Mock):
    fs.create_file('path/to/undo_commands.json', contents='[]')
    fs.create_dir('path/to/.trash')
    fs.create_dir('folder5')
    fs.create_file('folder/test.txt')
    fs.create_file('folder/test2.txt')
    os.chdir('/')

    with patch('src.commands.command_undo.create_undo_file', autospec=True) as mock_create_undo, \
            patch('builtins.input', return_value='y'), \
            patch('src.commands.command_rm.create_trash', autospec=True) as mock_create_trash:
        mock_create_undo.return_value = '/path/to/undo_commands.json'
        mock_create_trash.return_value = '/path/to/.trash'

        # проверяем для cp
        run_command('cp', ['folder', 'folder2', '-r'])
        assert os.path.exists('folder2/test.txt')
        assert os.path.exists('folder2/test2.txt')

        run_command('undo', [])
        assert not os.path.exists('folder2')
        assert 'undo: OK' in mock_logger_info.call_args_list[-1].args[0]

        # проверяем для rm
        assert os.path.exists('folder')
        run_command('rm', ['folder', '-r'])
        assert not os.path.exists('folder')

        run_command('undo', [])
        assert os.path.exists('folder')
        assert 'undo: OK' in mock_logger_info.call_args_list[-1].args[0]

        # проверяем для mv
        assert os.path.exists('folder')
        assert not os.path.exists('folder5/folder')
        run_command('mv', ['folder', 'folder5'])
        assert not os.path.exists('folder')
        assert os.path.exists('folder5/folder')

        run_command('undo', [])
        assert os.path.exists('folder')
        assert not os.path.exists('folder5/folder')
        assert 'undo: OK' in mock_logger_info.call_args_list[-1].args[0]


def test_cmd_undo_errors(fs: FakeFilesystem, mock_print: Mock):
    fs.create_file('path/to/undo_commands.json', contents='[]')
    fs.create_file('folder/test.txt')
    os.chdir('/')

    with patch('src.commands.command_undo.create_undo_file', autospec=True) as mock_create_undo:
        mock_create_undo.return_value = '/path/to/undo_commands.json'

        run_command('mv', ['folder', 'renamed_folder'])
        assert not os.path.exists('folder')
        assert os.path.exists('renamed_folder')

        # создадим папку с тем же именем, что была до переименования. Тогда undo не сможет все вернуть, как было
        fs.create_dir('folder')
        run_command('undo', [])
        assert 'Другая ошибка' in mock_print.call_args_list[-1].args[0]
