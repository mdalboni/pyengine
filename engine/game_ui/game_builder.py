"""
This module contains the GameBuilder class for the game engine.
It includes methods for building the game, including translating and dumping characters and scenes, and moving files to the output folder.
"""

import os
import shutil

from engine.game_objects.character import Character
from engine.game_ui.game import Game
from engine.game_ui.game_configurations import Configuration
from engine.utils.files import dump

OUTPUT_EXECUTABLE = """
from engine.game_ui.game import Game

from configuration import GAME_CONFIGURATION

if __name__ == "__main__":
    game = Game.load_assets(GAME_CONFIGURATION)
    game.start()
"""


class GameBuilder:
    """
    GameBuilder class. It represents a builder for the game engine.
    """
    game: Game
    config: Configuration

    def __init__(self, game: Game):
        """
        Initializes the GameBuilder instance.

        :param game: The game to be built.
        """
        self.game = game
        self.config = game.configuration

    def build(self, characters: dict[str, Character], output_folder: str = None):
        """
        Builds the game.

        :param characters: A dictionary mapping character names to Character instances.
        :param output_folder: The output folder for the game.
        """
        output_char_folder = os.path.join(output_folder, self.config.resource_folder, 'characters')
        output_scene_folder = os.path.join(output_folder, self.config.resource_folder, 'scenes')
        languages = self.config.languages
        for language in languages:
            for name, character in characters.items():
                for target_language in self.config.languages:
                    character.translate_and_dump(output_char_folder, language, target=target_language)

            for name, scene in self.game.scenes.items():
                for target_language in self.config.languages:
                    scene.translate_and_dump(output_scene_folder, language, target=target_language)

        assets_file = os.path.join(output_folder, self.config.resource_folder, 'assets.json')
        dump(
            assets_file,
            {
                "scenes": list(self.game.scenes.keys()),
                "characters": list(characters.keys())
            }
        )
        self._move_to_output_folder(
            self.config.resource_folder,
            os.path.join(output_folder, self.config.resource_folder)
        )

        files_to_generate = {
            os.path.join(output_folder, '__init__.py'): '',
            os.path.join(output_folder, '__main__.pyw'): OUTPUT_EXECUTABLE,
        }
        for file, content in files_to_generate.items():
            with open(file, 'w') as game_file:
                game_file.write(content)

        files_to_copy = [
            'configuration.py',
        ]

        for file in files_to_copy:
            shutil.copy(file, os.path.join(output_folder, file))
        print('Game assets built successfully')
        print(f"#{os.path.join(output_folder, '__main__.pyw')}#{self.config.game_title}#")

    def _move_to_output_folder(self, source_folder: str, output_path: str = None):
        """
        Moves files to the output folder.

        :param source_folder: The source folder.
        :param output_path: The output path.
        :return: None
        """
        if output_path is None:
            output_path = os.path.join('output', self.config.resource_folder)
        os.makedirs(output_path, exist_ok=True)
        for file_name in os.listdir(source_folder):
            source = os.path.join(source_folder, file_name)
            destination = os.path.join(output_path, file_name)
            if os.path.isfile(source):
                shutil.copy(source, destination)
                print('Copying file: ', source)
            elif os.path.isdir(source) and not source.endswith(('characters', 'scenes')):
                self._move_to_output_folder(source, destination)
