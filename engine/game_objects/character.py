"""
This module contains the Character classes for the game engine.
It includes the base Character class, and a dataclass _GameCharacter.
"""

import os
from dataclasses import dataclass

from engine.game_objects.base import BaseGameObject
from engine.utils.files import dump


@dataclass
class _GameCharacter:
    """
    _GameCharacter dataclass. It represents a snapshot of a game character's state.

    :param name: The name of the character.
    :param image: The image of the character.
    :param state: The state of the character.
    """
    name: str
    image: str
    state: str


class Character(BaseGameObject):
    """
    Character class. It represents a character in the game engine.

    :param name: The name of the character.
    :param state: The initial state of the character.
    :param states: A dictionary mapping states to images.
    """
    name: str
    state: str
    states: dict[str, str]
    mood: str

    def __init__(self, name, state='default', states: dict[str, str] = None, *args, **kwargs):
        """
        Initializes the Character instance.

        :param name: The name of the character.
        :param state: The initial state of the character.
        :param states: A dictionary mapping states to images.
        :param args: Additional positional arguments.
        :param kwargs: Additional keyword arguments.
        """
        super().__init__(*args, **kwargs)
        self.name = name
        self.state = state.upper()
        self.states = {state.upper(): states[state] for state in states} if states else {}

    def validate_states(self, game_path: str):
        """
        Validates the states of the character.

        :param game_path: The path to the game.
        """
        # TODO add the way to validate the assets properly
        if not self.state:
            return
        for state, path in self.states.items():
            if not os.path.exists(os.path.join(game_path, path)):
                raise ValueError(f"Invalid image for {state}. Image path {path} does not exist.")

    def snapshot(self, state: str = None) -> _GameCharacter:
        """
        Returns a snapshot of the character's state.

        :param state: The state of the character.
        :return: An instance of _GameCharacter representing the snapshot.
        """
        if state:
            state = state.upper()
            return _GameCharacter(self.name, self.states[state], state)
        return _GameCharacter(self.name, self.states[self.state], self.state)

    def __str__(self):
        return f"{self.name}[{self.state}]"

    def translate_and_dump(self, path: str, source: str, target: str, *args, **kwargs):
        """
        Translates and dumps the character.

        :param path: The path to the character.
        :param source: The source language.
        :param target: The target language.
        :param args: Additional positional arguments.
        :param kwargs: Additional keyword arguments.
        """
        output = self.__dict__.copy()
        dump(os.path.join(path, target, f'{self.name.upper()}.json'), output)
