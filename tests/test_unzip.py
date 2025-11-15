import os
import shutil
from pyfakefs.fake_filesystem import FakeFilesystem
from src.main import run_command
from unittest.mock import Mock
from src.exceptions import PathNotExists, InvalidAmountArguments


def test_cmd_unzip(fs: FakeFilesystem, mock_logger_info):
    fs.create_file('folder_to_zip/in_folder/smth.txt')
    os.chdir('/')

    run_command('zip', ['folder_to_zip', 'folder_zipped'])
    assert os.path.exists('folder_zipped.zip')

    shutil.rmtree('folder_to_zip')
    assert not os.path.exists('folder_to_zip')

    run_command('unzip', ['folder_zipped'])
    # при разархивации будет название той папки, которую мы сначала архивировали
    # поэтому я удалил исходную папку, чтобы проверить, создастся ли эта папка снова при разархивации
    assert os.path.exists('folder_to_zip')
    assert 'unzip: OK' in mock_logger_info.call_args_list[-1].args[0]


def test_cnd_unzip_errors(fs: FakeFilesystem, mock_logger_error: Mock, mock_print: Mock):
    fs.create_file('folder_to_zip/in_zip/zip_text.txt')
    fs.create_dir('empty_zip.zip')
    os.chdir('/')

    run_command('zip', ['folder_to_zip', 'folder_zipped.zip'])
    assert os.path.exists('folder_zipped.zip')

    error = run_command('unzip', ['folder_zipped.zip', 'unzipped_folder'])[1]
    assert isinstance(error, InvalidAmountArguments)
    assert 'unzip: Некорректное количество аргументов' in str(mock_print.call_args_list[-1].args[0])
    assert 'unzip: Некорректное количество аргументов' in mock_logger_error.call_args_list[-1].args[0]

    error = run_command('unzip', ['no_exist_folder.zip'])[1]
    assert isinstance(error, PathNotExists)
    assert 'unzip: Пути no_exist_folder.zip не существует' in str(mock_print.call_args_list[-1].args[0])
    assert 'unzip: Пути no_exist_folder.zip не существует' in mock_logger_error.call_args_list[-1].args[0]

    # так как пустой архив
    run_command('unzip', ['empty_zip.zip'])
    assert 'Не удалось разархивировать empty_zip.zip' in str(mock_print.call_args_list[-1].args[0])
    assert 'Не удалось разархивировать empty_zip.zip' in mock_logger_error.call_args_list[-1].args[0]
