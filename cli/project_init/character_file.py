CHARACTER_FILE_CONTENT = """
from engine.game_objects.character import Character

YOUR_CHARACTER = Character('your character', states={'default': 'your_character.png'})
YOUR_CHARACTER_FROM_JSON = Character.load('resources/characters/your_character_json.json')

CHARACTERS = {
    'YOUR_CHARACTER': YOUR_CHARACTER,
    'YOUR_CHARACTER_FROM_JSON': YOUR_CHARACTER_FROM_JSON,
}
"""

CHARACTER_JSON_CONTENT = """
{
  "name": "your_character_from_json",
  "state": "default",
  "states": {
    "default": "your_character.png",
    "inverse": "your_character_inverse.png"
  }
}
"""


