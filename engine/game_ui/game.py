"""
This module contains the Game class for the game engine.
It includes methods for game state management, scene management, and user interface (UI) rendering.
"""

import json
import os
import sys

import pygame

from engine.game_objects.character import Character
from engine.game_objects.scene import Scene
from engine.game_ui.constants.window_constants import SCREEN_WIDTH, SCREEN_HEIGHT
from engine.game_ui.game_configurations import Configuration
from engine.game_ui.game_renderer import (
    GameSceneRenderer,
    BackgroundRenderer,
    ForegroundRenderer,
    HUDRenderer,
    MenuRenderer
)
from engine.game_ui.game_scene import play_scene


class Game:
    """
    Game class. It represents the game engine.
    """
    scenes: dict[str, Scene]
    active_scene: str | None
    configuration: Configuration
    debug: bool

    def __init__(self, configuration: Configuration, debug=False):
        """
        Initializes the Game instance.

        :param configuration: The configuration of the game.
        :param debug: A flag indicating whether the game is in debug mode.
        """
        self.scenes = {}
        self.active_scene = 'start'
        self.configuration = configuration
        self.debug = debug
        if not self.configuration.build:
            pygame.init()
            self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.menu_renderer = MenuRenderer(self.screen, self.configuration.resource_folder)
            self.renderer = GameSceneRenderer(
                background_renderer=BackgroundRenderer(self.screen, self.configuration.resource_folder),
                foreground_renderer=ForegroundRenderer(self.screen, self.configuration.resource_folder),
                hud_renderer=HUDRenderer(self.screen, self.configuration.resource_folder)
            )
            pygame.display.set_caption(self.configuration.game_title)
        self._user_folder_path = os.path.join(os.path.expanduser("~"), self.configuration.game_title)
        os.makedirs(self._user_folder_path, exist_ok=True)
        self._save_file_path = os.path.join(self._user_folder_path, 'game_data')

    def select_language(self):
        """
        Allows the user to select a language for the game.

        :return: The next game state.
        """
        selected_item = 0
        menu_items = self.configuration.languages
        running = True
        while running:
            self.menu_renderer.render(selected_item, menu_items)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                elif event.type == pygame.KEYDOWN:
                    print('selected_item:', selected_item, menu_items[selected_item - 1])
                    if event.key == pygame.K_UP:
                        selected_item = (selected_item - 1) % len(menu_items)
                    elif event.key == pygame.K_DOWN:
                        selected_item = (selected_item + 1) % len(menu_items)
                    elif event.key == pygame.K_RETURN:
                        self.configuration.language = menu_items[selected_item]
                        return "menu"
                    elif event.key == pygame.K_ESCAPE:
                        return "quit"
            pygame.display.flip()

    def show_menu(self):
        """
        Displays the game menu to the user.

        :return: The next game state.
        """
        selected_item = 0
        menu_items = ["Start Game", "Load Game", "Quit"]
        if not self._has_save_file():
            menu_items.pop(1)
        running = True
        while running:
            self.menu_renderer.render(selected_item, menu_items)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        selected_item = (selected_item - 1) % len(menu_items)
                    elif event.key == pygame.K_DOWN:
                        selected_item = (selected_item + 1) % len(menu_items)
                    elif event.key == pygame.K_RETURN:
                        match menu_items[selected_item]:
                            case "Start Game":
                                return 'gameplay'
                            case "Load Game":
                                return "load_game"
                            case _:
                                return 'quit'
                    elif event.key == pygame.K_ESCAPE:
                        return "quit"
            pygame.display.flip()

    def _has_save_file(self) -> bool:
        return os.path.exists(self._save_file_path)

    def start(self):
        """
        Starts the game.

        :return: None
        """
        game_state = "select_language"
        running = True
        if self.debug:
            print('Debug mode active, skipping language selection.')
            game_state = "menu"
        while running:
            if game_state == "select_language":
                default_lang = self.configuration.language
                game_state = self.select_language()
                if default_lang != self.configuration.language:
                    self.scenes = {}
                    self.active_scene = 'start'
                    self.load_assets(self.configuration, game=self)
            elif game_state == "menu":
                self.active_scene = 'start'
                game_state = self.show_menu()
            elif game_state == "gameplay":
                game_state, output = self._gameplay(game_state)
                self._handle_save_file(game_state, output)
            elif game_state == "load_game":
                game_state = self._load_game_data(game_state)
            elif game_state == "game_over":
                game_state = 'menu'
            elif game_state == "quit":
                running = False

            pygame.display.flip()

    def _handle_save_file(self, game_state, output):
        if game_state == 'game_over' and self._has_save_file():
            print('Removing save file, game was completed')
            os.remove(self._save_file_path)
        elif output and game_state != 'game_over':
            with open(self._save_file_path, 'w') as file:
                file.write(output)

    def _gameplay(self, game_state):
        print('Scene:', self.scenes[self.active_scene].name)
        # TODO Move to a class with the common interface
        output, game_state = play_scene(
            self.scenes[self.active_scene],
            self.renderer,
        )
        self.scenes[self.active_scene].action = 0
        self.active_scene = output
        return game_state, output

    def _load_game_data(self, game_state):
        with open(self._save_file_path, 'r') as file:
            loaded_scene = file.read()
            if loaded_scene in self.scenes:
                self.active_scene = loaded_scene
                game_state = 'gameplay'
        return game_state

    def add_scene(self, scene: Scene):
        """
        Adds a scene to the game.

        :param scene: The scene to be added.
        :return: None
        """
        if scene.name in self.scenes:
            raise Exception("Scene already exists")
        self.scenes[scene.name] = scene

    @staticmethod
    def load_assets(configuration: Configuration, game: 'Game' = None) -> 'Game':
        """
        Loads the assets for the game.

        :param configuration: The configuration of the game.
        :param game: An optional Game instance.
        :return: A Game instance with the loaded assets.
        """
        assets_path = os.path.join(configuration.resource_folder, 'assets.json')
        with open(assets_path, 'r') as assets_file:
            assets = json.load(assets_file)
        characters = {}
        char_folder = os.path.join(configuration.resource_folder, 'characters', configuration.language)
        for character in assets['characters']:
            character_path = os.path.join(char_folder, f"{character}.json")
            with open(character_path, 'r') as character_file:
                data = json.load(character_file)
                characters[data['name'].upper()] = Character(**data)

        scene_folder = os.path.join(configuration.resource_folder, 'scenes', configuration.language)
        if game is None:
            game = Game(configuration, debug=False)
        else:
            game.scenes = {}
        for scene in assets['scenes']:
            scene_path = os.path.join(scene_folder, f"{scene}.json")
            game.add_scene(Scene.load(scene_path, characters=characters))
        return game

    def quit(self):
        """
        Quits the game.
        """
        pygame.quit()
        sys.exit()

    def run(self):
        """
        Runs the game.

        :return: None
        """
        try:
            self.start()
        except Exception as ex:
            with open('error.log', 'w') as error_file:
                error_file.write(f'An error occurred:\n{ex}')
        finally:
            self.quit()
