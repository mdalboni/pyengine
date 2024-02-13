import unittest
from unittest.mock import patch

from cli.installer import build  # corrected import


class TestBuild(unittest.TestCase):

    @patch('cli.installer.build.os')
    @patch('cli.installer.build.shutil')
    @patch('cli.installer.build.subprocess')
    @patch('cli.installer.build.py_installer')
    def test_build(self, mock_py_installer, mock_subprocess, mock_shutil, mock_os):
        # Setup
        mock_os.path.dirname.return_value = 'data_path'
        mock_subprocess.Popen.return_value.communicate.return_value = (b'#build_main_path#game_name#\n', None)
        mock_os.listdir.return_value = [
            '__init__.py',
            '__main__.py',
            'configuration.py',
            'build.py',
            'characters.py'
        ]
        # Call
        build.build('output_path', 'project_path', ['platforms'], ['resolutions'], ['languages'])

        # Assert
        mock_os.listdir.assert_called_once_with('project_path')
        mock_subprocess.Popen.assert_called_once_with('python build.py', stdout=mock_subprocess.PIPE, shell=True)
        mock_py_installer.run.assert_called_once()
        mock_shutil.rmtree.assert_called_once_with('data_path', ignore_errors=True)

    @patch('cli.installer.build.os')
    @patch('cli.installer.build.shutil')
    @patch('cli.installer.build.py_installer')
    def test_build_app(self, mock_py_installer, mock_shutil, mock_os):
        # Call
        build.build_app('build_main_path', 'data_path', 'game_name', 'output_path')

        # Assert
        mock_py_installer.run.assert_called_once()
        mock_shutil.rmtree.assert_called_once_with('data_path', ignore_errors=True)

    @patch('cli.installer.build.subprocess')
    def test_build_game_jsons(self, mock_subprocess):
        # Setup
        mock_subprocess.Popen.return_value.communicate.return_value = (b'#build_main_path#game_name#\n', None)

        # Call
        build_main_path, game_name = build.build_game_jsons()

        # Assert
        self.assertEqual(build_main_path, 'build_main_path')
        self.assertEqual(game_name, 'game_name')
        mock_subprocess.Popen.assert_called_once_with('python build.py', stdout=mock_subprocess.PIPE, shell=True)

    @patch('cli.installer.build.os')
    def test_validate_files(self, mock_os):
        # Setup
        mock_os.listdir.return_value = ['__init__.py', '__main__.py', 'configuration.py', 'build.py', 'characters.py']

        # Call
        build.validate_files('project_path')

        # Assert
        mock_os.listdir.assert_called_once_with('project_path')
