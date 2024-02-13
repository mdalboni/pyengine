MAIN_FILE_CONTENT = """
from engine.game_ui.game import Game, Configuration
from scenes import load_scenes
from configuration import GameConfiguration

game = Game(configuration=configuration)

if __name__ == "__main__":
    scenes = load_scenes()
    for scene in scenes:
        game.add_scene(scenes[scene])
    game.start()
"""
