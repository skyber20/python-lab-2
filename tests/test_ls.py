# import pytest
# from unittest.mock import patch
# from src.commands.command_ls import run_ls
#
#
# def run_ls_with_mocks(ls_args: list[str], exists=True) -> dict[str, str | list]:
#     with patch('os.getcwd', return_value='/test'), \
#         patch('os.path.exists', return_value=exists), \
#         patch('builtins.print') as mock_print, \
#         patch('utils.my_logger.logger.info') as mock_log_info, \
#         patch('utils.my_logger.logger.error') as mock_log_error:
#
#         run_ls(ls_args)
#
#         return {
#             'output': ' '.join(str(call.args[0]) for call in mock_print.call_args_list),
#             'info_logs': ' '.join(str(call.args[0]) for call in mock_print.call_args_list),
#             'error_logs': ' '.join(str(call.args[0]) for call in mock_print.call_args_list)
#         }
