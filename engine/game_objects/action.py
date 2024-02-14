"""
This module contains the Action classes for the game engine.
It includes the base Action class, and specific action classes: Talk, Choice, and GoTo.
"""
from engine.game_objects.character import Character, _GameCharacter
from engine.utils.translation import translate


class Action:
    """
    Base Action class. It represents an action performed by a character in the game.

    :param character: The character performing the action.
    :param state: The state of the character.
    """
    character: _GameCharacter
    type: str = 'action'

    def __init__(self, character: Character, state: str = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.character = character.snapshot(state=state)

    def render(self) -> dict:
        return {
            'character_name': self.character.name,
            'character_image': self.character.image,
            'type': self.type
        }

    def dump(self, *args, **kwargs) -> dict:
        return {
            'character': self.character.name.upper(),
            'state': self.character.state.upper(),
            'type': self.type
        }

    def __str__(self):
        return f"{self.type} - {self.character.name}[{self.character.state}]"

    def go_to(self) -> list[str] | None:
        return None


class Talk(Action):
    """
    Talk Action class. It represents a talking action performed by a character in the game.

    :param character: The character performing the action.
    :param text: The text that the character says.
    :param state: The state of the character.
    """
    text: str
    type: str = 'talk'

    def __init__(self, character: Character, text: str, state: str = None, *args, **kwargs):
        super().__init__(character, state, *args, **kwargs)
        self.text = text

    def render(self) -> dict:
        output = super().render()
        output['text'] = self.text
        return output

    def dump(self, src: str, target: str, *args, **kwargs) -> dict:
        output = super().dump(*args, **kwargs)
        output['text'] = translate(self.text, src, target)
        return output


class Choice(Action):
    """
    Choice Action class. It represents a choice action performed by a character in the game.

    :param character: The character performing the action.
    :param text: The text that the character says.
    :param choices: The choices that the character can make.
    :param state: The state of the character.
    """
    text: str
    choices: list[tuple[str, str]]
    type: str = 'choice'

    def __init__(self, character: Character, text: str, choices: list[tuple[str, str]], state: str = None, *args,
                 **kwargs):
        super().__init__(character, state, *args, **kwargs)
        self.text = text
        self.choices = choices

    def render(self) -> dict:
        output = super().render()
        output['text'] = self.text
        output['choices'] = self.choices
        return output

    def dump(self, src: str, target: str, *args, **kwargs) -> dict:
        output = super().dump(*args, **kwargs)
        output['text'] = translate(self.text, src, target)
        output['choices'] = [
            {
                'go_to': choice[0],
                'text': translate(choice[1], src, target)
            }
            for choice in self.choices
        ]
        return output

    def go_to(self) -> list[str]:
        return [choice[0] for choice in self.choices]


class GoTo(Action):
    """
    GoTo Action class. It represents a go-to action performed by a character in the game.

    :param character: The character performing the action.
    :param text: The text that the character says.
    :param go_to: The scene that the character goes to.
    :param state: The state of the character.
    """
    text: str
    _go_to: str
    type: str = 'go_to'

    def __init__(
            self,
            character: Character,
            text: str,
            go_to: str = None,
            state: str = None,
            *args, **kwargs
    ):
        super().__init__(character, state, *args, **kwargs)
        self.text = text
        self._go_to = go_to

    def render(self) -> dict:
        output = super().render()
        output['text'] = self.text
        output['go_to'] = self._go_to
        return output

    def dump(self, src: str, target: str, *args, **kwargs) -> dict:
        output = super().dump(*args, **kwargs)
        output['text'] = translate(self.text, src, target)
        output['go_to'] = self._go_to
        return output

    def go_to(self) -> list[str] | None:
        return [self._go_to]
