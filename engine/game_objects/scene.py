"""
This module contains the Scene class for the game engine.
It includes methods for adding actions to a scene, executing the next action, loading a scene from a file, and translating and dumping a scene.
"""
import json
import os

from engine.game_objects.action import Action, Choice, Talk, GoTo
from engine.game_objects.base import BaseGameObject
from engine.game_objects.character import Character


class Scene(BaseGameObject):
    """
    Scene class. It represents a scene in the game engine.

    :param name: The name of the scene.
    :param background: The background of the scene.
    """
    name: str
    background: str
    action: int
    actions: list[Action]
    history: list[Action]
    outcomes: list[str]

    def __init__(self, name, background, *args, **kwargs):
        """
        Initializes the Scene instance.

        :param name: The name of the scene.
        :param background: The background of the scene.
        :param args: Additional positional arguments.
        :param kwargs: Additional keyword arguments.
        """
        super().__init__(*args, **kwargs)
        self.name = name
        self.background = background
        self.actions = []
        self.history = []
        self.action = 0
        self.outcomes = []

    def __str__(self):
        return (
            f"{self.name} - {self.action + 1}/{len(self.actions)}\n"
            f"{[f'{idx}: ' + str(action) for idx, action in enumerate(self.actions, start=1)]}"
        )

    def add_action(self, action: Action):
        """
        Adds an action to the scene.

        :param action: The action to be added.
        """
        if (
                self.actions
                and type(self.actions[len(self.actions) - 1]) in {Choice, GoTo}
        ):
            raise Exception("You cannot add more actions to this scene")
        if action.go_to():
            self.outcomes.extend(action.go_to())
        self.actions.append(action)

    def execute_next_action(self) -> Action | None:
        """
        Executes the next action in the scene.

        :return: The next action in the scene, or None if there are no more actions.
        """
        if self.action < len(self.actions):
            action = self.actions[self.action]
            self.history.append(action)
            self.action += 1
            return action
        self.action = 0
        return None

    @classmethod
    def load(cls, path: str, characters: dict[str, Character] = None, *args, **kwargs) -> 'Scene':
        """
        Loads a scene from a file.

        :param path: The path to the file.
        :param characters: A dictionary mapping character names to Character instances.
        :param args: Additional positional arguments.
        :param kwargs: Additional keyword arguments.
        :return: A Scene instance.
        """
        with open(path, "r", encoding='utf-8') as file:
            content = json.load(file)
            scene = cls(**content)
        for action in content.get('actions'):
            action_type = action.pop('type')
            if not action_type:
                raise Exception("Action type not found")
            action['character'] = characters.get(action['character'].upper())
            if action_type == "choice":
                choices = [
                    (choice['go_to'], choice['text'])
                    for choice in action.pop('choices')
                ]
                scene.add_action(Choice(choices=choices, **action))
            elif action_type == "go_to":
                scene.add_action(GoTo(**action))
            elif action_type == "talk":
                scene.add_action(Talk(**action))
        return scene

    def translate_and_dump(self, path: str, source: str, target: str, *args, **kwargs):
        """
        Translates and dumps the scene.

        :param path: The path to the scene.
        :param source: The source language.
        :param target: The target language.
        :param args: Additional positional arguments.
        :param kwargs: Additional keyword arguments.
        """
        snapshot = self.__dict__.copy()
        output = {
            "name": snapshot["name"],
            "background": snapshot["background"],
            "actions": [
                action.dump(source, target)
                for action in snapshot["actions"]
            ]
        }
        output_path = os.path.join(path, target)
        output_file = os.path.join(output_path, f"{snapshot['name']}.json")
        os.makedirs(output_path, exist_ok=True)
        with open(output_file, "w", encoding='utf-8') as file:
            json.dump(output, file, ensure_ascii=False)
