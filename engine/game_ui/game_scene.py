"""
This module contains the function play_scene for the game engine.
It includes methods for playing a scene, rendering actions, handling user inputs, and managing game states.
"""

import pygame

from engine.game_objects.scene import Scene
from engine.game_ui.game_renderer import GameSceneRenderer


def play_scene(scene: Scene, renderer: GameSceneRenderer) -> (str, str):
    """
    Plays a scene in the game.

    :param scene: The scene to be played.
    :param renderer: The renderer for the game scene.
    :return: A tuple containing the next scene and the next game state.
    """
    action = scene.execute_next_action()
    while action:
        rendered_action = action.render()
        choices = rendered_action.get('choices')
        go_to = rendered_action.get('go_to')
        selected_item = 0
        running = True
        while running:
            renderer.render(
                background=scene.background,
                selected_item=selected_item,
                **action.render()
            )

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None, "quit"
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return None, "menu"
                    elif choices:
                        if event.key == pygame.K_UP:
                            selected_item = (selected_item - 1) % len(choices)
                        elif choices and event.key == pygame.K_DOWN:
                            selected_item = (selected_item + 1) % len(choices)
                        elif choices and event.key == pygame.K_RETURN:
                            return choices[selected_item][0], 'gameplay' if choices[selected_item][0] else 'game_over'
                    elif go_to:
                        return go_to, 'gameplay'
                    else:
                        running = False

            pygame.display.flip()

        action = scene.execute_next_action()
    return None, 'game_over'
