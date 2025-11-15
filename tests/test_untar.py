import os
import shutil
from pyfakefs.fake_filesystem import FakeFilesystem
from src.main import run_command
from unittest.mock import Mock
from src.exceptions import PathNotExists, InvalidAmountArguments


def test_cmd_untar(fs: FakeFilesystem, mock_logger_info):
    fs.create_file('folder_to_tar/in_folder/smth.txt')
    os.chdir('/')

    run_command('tar', ['folder_to_tar', 'folder_tarred'])
    assert os.path.exists('folder_tarred.tar.gz')

    shutil.rmtree('folder_to_tar')
    assert not os.path.exists('folder_to_tar')

    # могут возникать предупреждения при разархивации
    run_command('untar', ['folder_tarred'])
    # при разархивации будет название той папки, которую мы сначала архивировали
    # поэтому я удалил исходную папку, чтобы проверить, создастся ли эта папка снова при разархивации
    assert os.path.exists('folder_to_tar')
    assert 'untar: OK' in mock_logger_info.call_args_list[-1].args[0]


def test_cnd_untar_errors(fs: FakeFilesystem, mock_logger_error: Mock, mock_print: Mock):
    fs.create_file('folder_to_tar/in_tar/tar_text.txt')
    fs.create_dir('empty_tar.tar.gz')
    os.chdir('/')

    run_command('tar', ['folder_to_tar', 'folder_tarred.tar.gz'])
    assert os.path.exists('folder_tarred.tar.gz')

    error = run_command('untar', ['folder_tarred.tar.gz', 'untarred_folder'])[1]
    assert isinstance(error, InvalidAmountArguments)
    assert 'untar: Некорректное количество аргументов' in str(mock_print.call_args_list[-1].args[0])
    assert 'untar: Некорректное количество аргументов' in mock_logger_error.call_args_list[-1].args[0]

    error = run_command('untar', ['no_exist_folder.tar.gz'])[1]
    assert isinstance(error, PathNotExists)
    assert 'untar: Пути no_exist_folder.tar.gz не существует' in str(mock_print.call_args_list[-1].args[0])
    assert 'untar: Пути no_exist_folder.tar.gz не существует' in mock_logger_error.call_args_list[-1].args[0]

    # так как пустой архив, то не может разархивировать
    run_command('untar', ['empty_tar.tar.gz'])
    assert 'Не удалось разархивировать empty_tar.tar.gz' in str(mock_print.call_args_list[-1].args[0])
    assert 'Не удалось разархивировать empty_tar.tar.gz' in mock_logger_error.call_args_list[-1].args[0]
