import unittest
from unittest.mock import patch

from engine.game_objects.scene import Scene
from engine.game_ui.game import Game
from engine.game_ui.game_configurations import Configuration


class TestGame(unittest.TestCase):

    def setUp(self):
        self.configuration = Configuration(game_title='Test Game', resource_folder='resources', languages=['en', 'fr'])
        self.game = Game(self.configuration, debug=False)

    def test_game_init(self):
        self.assertEqual(self.game.scenes, {})
        self.assertEqual(self.game.active_scene, 'start')
        self.assertEqual(self.game.configuration, self.configuration)
        self.assertEqual(self.game.debug, False)

    @patch('engine.game_ui.game.Game.select_language')
    def test_game_start_select_language(self, mock_select_language):
        mock_select_language.return_value = "quit"
        self.game.start()
        mock_select_language.assert_called_once()

    @patch('engine.game_ui.game.Game.select_language')
    @patch('engine.game_ui.game.Game.show_menu')
    def test_game_start_show_menu(self, mock_show_menu, mock_select_language):
        mock_select_language.return_value = "menu"
        mock_show_menu.return_value = "quit"
        self.game.start()
        mock_show_menu.assert_called_once()

    def test_game_add_scene(self):
        scene = Scene('Test Scene', 'background.png')
        self.game.add_scene(scene)
        self.assertEqual(self.game.scenes, {'Test Scene': scene})

    def test_game_add_scene_exception(self):
        scene = Scene('Test Scene', 'background.png')
        self.game.add_scene(scene)
        with self.assertRaises(Exception):
            self.game.add_scene(scene)

    @patch('engine.game_ui.game.Game.load_assets')
    def test_game_load_assets(self, mock_load_assets):
        mock_load_assets.return_value = self.game
        result = Game.load_assets(self.configuration)
        self.assertEqual(result, self.game)
        mock_load_assets.assert_called_once_with(self.configuration)

    def test_game_quit(self):
        with self.assertRaises(SystemExit):
            self.game.quit()
