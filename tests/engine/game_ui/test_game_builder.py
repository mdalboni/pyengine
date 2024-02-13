import unittest
from unittest.mock import patch, mock_open

from engine.game_objects.character import Character
from engine.game_ui.game import Game
from engine.game_ui.game_builder import GameBuilder
from engine.game_ui.game_configurations import Configuration


class TestGameBuilder(unittest.TestCase):

    def setUp(self):
        self.configuration = Configuration(
            game_title='Test Game',
            resource_folder='resources',
            languages=['en', 'fr'],
            build=True
        )
        self.game = Game(self.configuration, debug=True)
        self.game_builder = GameBuilder(self.game)

    def test_game_builder_init(self):
        self.assertEqual(self.game_builder.game, self.game)
        self.assertEqual(self.game_builder.config, self.configuration)

    @patch("builtins.open", new_callable=mock_open)
    @patch('engine.game_ui.game_builder.os.makedirs')
    @patch('engine.game_ui.game_builder.shutil.copy')
    @patch('engine.game_ui.game_builder.GameBuilder._move_to_output_folder')
    @patch('engine.game_ui.game_builder.dump')
    def test_game_builder_build(self, mock_dump, mock_move_to_output_folder, _, __, mock_open_instance):
        characters = {'Test Character': Character('Test Character', 'state', {'state': 'image.png'})}
        self.game_builder.build(characters, 'output')
        mock_dump.assert_called_once()
        mock_move_to_output_folder.assert_called_once()

    @patch('os.makedirs')
    @patch('shutil.copy')
    @patch('os.listdir')
    def test_game_builder_move_to_output_folder(self, mock_listdir, mock_copy, mock_makedirs):
        mock_listdir.return_value = ['file1', 'file2']
        self.game_builder._move_to_output_folder('source', 'output')
        mock_makedirs.assert_called_once_with('output', exist_ok=True)
        self.assertEqual(mock_copy.call_count, 2)
