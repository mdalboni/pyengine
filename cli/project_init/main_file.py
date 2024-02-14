MAIN_FILE_CONTENT = """
from engine.game_ui.game import Game
from scenes import load_scenes
from configuration import GAME_CONFIGURATION

game = Game(configuration=GAME_CONFIGURATION, debug=True)

if __name__ == "__main__":
    scenes = load_scenes()
    for scene in scenes:
        game.add_scene(scenes[scene])
    game.run()
"""
