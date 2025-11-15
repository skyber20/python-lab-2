from src.main import run_history
from unittest.mock import Mock, patch
from pyfakefs.fake_filesystem import FakeFilesystem


def test_cmd_history(fs: FakeFilesystem, mock_print: Mock):
    fs.create_file('path/to/.history.txt')

    with patch('src.commands.command_history.create_history_file', autospec=True) as mock_create_file:
        mock_create_file.return_value = '/path/to/.history.txt'

        run_history(inp='ls -l', show=False)
        run_history(inp='cd D:/User', show=False)
        run_history(inp='mv folder1 folder2', show=False)
        run_history(n=['3'])

    assert '1.ls -l' in mock_print.call_args_list[0].args[0]
    assert '2.cd D:/User' in mock_print.call_args_list[1].args[0]
    assert '3.mv folder1 folder2' in mock_print.call_args_list[2].args[0]
