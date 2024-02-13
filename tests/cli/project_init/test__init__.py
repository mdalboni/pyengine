import unittest
from os.path import join
from unittest.mock import patch, MagicMock

from cli import project_init as init_module


class TesProjectInitModule(unittest.TestCase):
    def setUp(self):
        self.project_path = "test_project_path"
        self.project_name = "test_project"

    @patch('cli.project_init.os.makedirs')
    def test_create_project_folder(self, mock_makedirs):
        init_module._create_project_folder(self.project_path)
        mock_makedirs.assert_called_once_with(self.project_path, exist_ok=False)

    @patch('cli.project_init._create_project_folder')
    @patch('cli.project_init.print')
    @patch('cli.project_init.open', new_callable=MagicMock)
    def test_init_project(self, mock_open, mock_print, mock_create_project_folder):
        init_module.init_project(self.project_path, self.project_name)
        mock_create_project_folder.assert_called()
        mock_print.assert_called_with("Project initialized.")

    @patch('cli.project_init._create_project_folder')
    @patch('cli.project_init.open', new_callable=MagicMock)
    def test_create_resource_files(self, mock_open, mock_create_project_folder):
        init_module.create_resource_files('resources', self.project_path)
        mock_create_project_folder.assert_called_with(join(self.project_path, 'resources', 'characters'))
        assert mock_open.call_count == 3

    @patch('cli.project_init.open', new_callable=MagicMock)
    def test_create_character_files(self, mock_open):
        init_module.create_character_files('characters', self.project_path)
        assert mock_open.call_count == 2

    @patch('cli.project_init.open', new_callable=MagicMock)
    def test_create_scene_files(self, mock_open):
        init_module.create_scene_files('scenes', self.project_path)
        assert mock_open.call_count == 5
