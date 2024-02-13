"""
This module contains the BaseGameObject class for the game engine.
It includes the base class for all game objects and methods for loading and dumping game objects.
"""

import json


class BaseGameObject:
    """
    BaseGameObject class. It represents a base game object in the game engine.

    :param args: Additional positional arguments.
    :param kwargs: Additional keyword arguments.
    """

    def __init__(self, *args, **kwargs):
        """
        Initializes the BaseGameObject instance.

        :param args: Additional positional arguments.
        :param kwargs: Additional keyword arguments.
        """
        pass

    @classmethod
    def load(cls, path: str, *args, **kwargs):
        """
        Loads a game object from a JSON file.

        :param path: The path to the JSON file.
        :param args: Additional positional arguments.
        :param kwargs: Additional keyword arguments.
        :return: An instance of the class.
        """
        with open(path, "r", encoding='utf-8') as file:
            return cls(**json.load(file))

    def translate_and_dump(self, *args, **kwargs):
        """
        Translates and dumps the game object. This method should be implemented in a subclass.

        :param args: Additional positional arguments.
        :param kwargs: Additional keyword arguments.
        :raises NotImplementedError: If the method is not implemented in a subclass.
        """
        raise NotImplementedError
