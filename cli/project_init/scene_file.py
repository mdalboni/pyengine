SCENE_FILE_CONTENT = """
import glob
from os.path import dirname, basename, isfile, join

from .starting_scene import SCENE as STARTING_SCENE

modules = glob.glob(join(dirname(__file__), "*.py"))
__all__ = [
    basename(f)[:-3]
    for f in modules
    if (
            isfile(f)
            and not f.endswith('__init__.py') and not f.endswith('starting_scene.py')
    )
]


def load_scenes():
    path = dirname(__file__)
    actual_module_name = basename(path)
    scenes = {STARTING_SCENE.name: STARTING_SCENE}
    for scene in __all__:
        module_ref = getattr(__import__(f'{actual_module_name}', fromlist=[scene]), scene)
        scenes[scene] = module_ref.SCENE
    return scenes

"""

SAMPLE_SCENE_FILE_CONTENT = """
from engine.game_objects.action import Choice, Talk, GoTo
from engine.game_objects.scene import Scene
from characters import YOUR_CHARACTER

SCENE = Scene('new_scene', background='background.png')

SCENE.add_action(Talk(character=YOUR_CHARACTER, text='This is a sample scene example'))
SCENE.add_action(GoTo(character=YOUR_CHARACTER, text='The end'))
"""

SAMPLE_STARTING_SCENE_FILE_CONTENT = """
\"\"\"
DO NOT DELETE THIS FILE
This file is used to define the characters of the game.
\"\"\"
from engine.game_objects.action import Choice, Talk, GoTo
from engine.game_objects.scene import Scene
from characters import YOUR_CHARACTER

SCENE = Scene('start', background='background.png')

SCENE.add_action(Talk(character=YOUR_CHARACTER, text='Hello, welcome to the sample game.'))

SCENE.add_action(
    Choice(
        character=YOUR_CHARACTER,
        text='This is the starting scene, where do you want to go?',
        choices=[
            ('new_scene', 'Scene #1'),
            ('json_scene', 'Scene #2')            
        ]
    )
)
"""

SAMPLE_JSON_SCENE_FILE_CONTENT = """
from engine.game_objects.scene import Scene
from characters import CHARACTERS

SCENE = Scene.load('scenes/json_scene.json', CHARACTERS)
"""

SCENE_JSON_CONTENT = """
{
  "name": "json_scene",
  "background": "background.png",
  "actions": [
    {
      "type": "talk",
      "character": "your_character_from_json",
      "state": "inverse",
      "text": "Scene loaded from JSON file, character with another state"
    },
    {
      "type": "choice",
      "character": "your_character",
      "state": "default",
      "text": "<TEXT>",
      "choices": [
        {
          "go_to": null,
          "text": "Back to the start"
        }
      ]
    }
  ]
}
"""

BACKGROUND_B64_IMAGE = b'iVBORw0KGgoAAAANSUhEUgAAAMgAAADICAYAAACtWK6eAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAPmSURBVHhe7dOhEQJBAATBCwRJMqQJBIfBkMAB9VVv/vyPaNFm7daMcX9NTjbGwftyJUAgBQLJEkiBQLIEUiCQLIEUCCRLIAUCyRJIgUCyBFIgkCyBFAgkSyAFAskSSIFAsgRSIJAsgRQIJEsgBQLJEkiBQLIEUiCQLIEUCCRLIAUCyRJIgUCyBFIgkCyBFAgkSyAFAskSSIFAsgRSIJAsgRQIJEsgBQLJEkiBQLIEUiCQLIEUCCRLIAUCyRJIgUCyBFIgkCyBFAgkSyAFAskSSIFAsgRSIJAsgRQIJEsgBQLJEkiBQLIEUiCQLIEUCCRLIAUCyRJIgUCyBFIgkCyBFAgkSyAFAskSSIFAsgRSIJAsgRQIJEsgBQLJEkiBQLIEUiCQLIEUCCRLIAUCyRJIgUCyBFIgkCyBFAgkSyAFAskSSIFAsgRSIJAsgRQIJEsgBQLJEkiBQLIEUiCQLIEUCCRLIAUCyRJIgUCyBFIgkCyBFAgkSyAFAskSSIFAsgRSIJAsgRQIJEsgBQLJEkiBQLIEUiCQLIEUCCRLIAUCyRJIgUCyBFIgkCyBFAgkSyAFAskSSIFAsgRSIJAsgRQIJEsgBQLJEkiBQLIEUiCQLIEUCCRLIAUCyRJIgUCyBFIgkCyBFAgkSyAFAskSSIFAsgRSIJAsgRQIJOv3xfEcYLccgc1yBDbLEdgsR+DvcXtOzrU6Zn4oEEiAQLoEEiCQLoEECKRLIAEC6RJIgEC6BBIgkC6BBAikSyABAukSSIBAugQSIJAugQQIpEsgAQLpEkiAQLoEEiCQLoEECKRLIAEC6RJIgEC6BBIgkC6BBAikSyABAukSSIBAugQSIJAugQQIpEsgAQLpEkiAQLoEEiCQLoEECKRLIAEC6RJIgEC6BBIgkC6BBAikSyABAukSSIBAugQSIJAugQQIpEsgAQLpEkiAQLoEEiCQLoEECKRLIAEC6RJIgEC6BBIgkC6BBAikSyABAukSSIBAugQSIJAugQQIpEsgAQLpEkiAQLoEEiCQLoEECKRLIAEC6RJIgEC6BBIgkC6BBAikSyABAukSSIBAugQSIJAugQQIpEsgAQLpEkiAQLoEEiCQLoEECKRLIAEC6RJIgEC6BBIgkC6BBAikSyABAukSSIBAugQSIJAugQQIpEsgAQLpEkiAQLoEEiCQLoEECKRLIAEC6RJIgEC6BBIgkC6BBAikSyABAukSSIBAugQSIJAugQQIpEsgAQLpEkiAQLoEEiCQLoEECKRLIAEC6RJIgEC6BBIgkC6BBAikSyABAukSSIBAugQSIJAugQQIpEsgAQLpEkiAQKrG/ALes87HlMahHwAAAABJRU5ErkJggg=='
