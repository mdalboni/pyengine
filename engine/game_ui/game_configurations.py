"""
This module contains the Configuration class for the game engine.
It includes properties for game title, resource folder, language, languages, and build.
"""

from engine.utils.files import resource_path


class Configuration:
    """
    Configuration class. It represents the configuration for the game engine.
    """
    game_title: str
    resource_folder: str
    language: str
    languages: list[str]
    build: bool

    def __init__(
            self,
            game_title: str,
            resource_folder: str = 'resources',
            language: str = 'pt',
            languages: list[str] = None,
            build: bool = False,
    ):
        """
        Initializes the Configuration instance.

        :param game_title: The title of the game.
        :param resource_folder: The resource folder for the game.
        :param language: The language of the game.
        :param languages: The languages available for the game.
        :param build: A flag indicating whether the game is in build mode.
        """
        self._resource_folder = resource_folder
        self.language = language
        self.languages = languages or [language]
        self.game_title = game_title
        self.build = build

    @property
    def resource_folder(self):
        """
        Returns the resource folder for the game depending on the settings

        :return: The resource folder for the game.
        """
        if not self.build:
            return resource_path(self._resource_folder)
        else:
            return self._resource_folder
