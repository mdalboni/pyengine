VALIDATE_FILE_CONTENT = """
from engine.game_ui.game import Game

from configuration import GAME_CONFIGURATION
from scenes import load_scenes

GAME_CONFIGURATION.build = True
game = Game(configuration=GAME_CONFIGURATION)

if __name__ == "__main__":
    scenes = load_scenes()
    hit_list = {scene.name: {'go_to': [], 'origins': []} for scene in scenes.values()}
    hit_list[None] = {'go_to': [], 'origins': []}
    graph = []
    for name, scene in scenes.items():
        for action in scene.actions:
            outcomes = action.go_to() or []
            for outcome in outcomes:
                graph.append((scene.name, outcome))
                hit_list[scene.name]['go_to'].append(outcome)
                hit_list[outcome]['origins'].append(scene.name)

    print('Analyzing the graph...')
    print('#' * 10)
    for scene, data in hit_list.items():
        if scene == 'start':
            continue
        if len(data['origins']) == 0:
            print(f"Scene [{scene}] is not reachable")
    print('#' * 10)
"""