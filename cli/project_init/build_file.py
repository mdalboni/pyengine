BUILD_FILE_CONTENT = """
from engine.game_ui.game import Game
from engine.game_ui.game_builder import GameBuilder

from characters import CHARACTERS
from configuration import GAME_CONFIGURATION
from scenes import load_scenes

GAME_CONFIGURATION.build = True
game = Game(configuration=GAME_CONFIGURATION)

if __name__ == "__main__":
    scenes = load_scenes()
    for scene in scenes:
        game.add_scene(scenes[scene])
    GameBuilder(game).build(characters=CHARACTERS, output_folder='output')
"""
