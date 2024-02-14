"""
This module contains the initialization functionality for the game engine.
It includes the main project initialization function, functions to create resource, character, and scene files,
and a function to create the project folder.
"""

import base64
import os

from cli.project_init.validate_file import VALIDATE_FILE_CONTENT

from cli.project_init.build_file import BUILD_FILE_CONTENT
from cli.project_init.character_file import (
    CHARACTER_FILE_CONTENT,
    CHARACTER_B64_IMAGE,
    CHARACTER_INVERSE_B64_IMAGE,
    CHARACTER_JSON_CONTENT,
)
from cli.project_init.configuration_file import CONFIGURATION_FILE_CONTENT
from cli.project_init.main_file import MAIN_FILE_CONTENT
from cli.project_init.scene_file import (
    SCENE_FILE_CONTENT,
    SAMPLE_STARTING_SCENE_FILE_CONTENT,
    SAMPLE_SCENE_FILE_CONTENT,
    BACKGROUND_B64_IMAGE,
    SAMPLE_JSON_SCENE_FILE_CONTENT,
    SCENE_JSON_CONTENT,
)

base_paths = [
    'resources',
    'scenes',
    'characters',
]


def init_project(project_path: str, project_name: str):
    """
    Initializes the project by creating the necessary folders and files.

    :param project_path: The path where the project will be created.
    :param project_name: The name of the project.
    """
    print("Initializing project...")
    print("Project path:", project_path)
    _create_project_folder(project_path)

    for base_path in base_paths:
        match base_path:
            case 'scenes':
                _create_project_folder(os.path.join(project_path, base_path))
                create_scene_files(base_path, project_path)
            case 'characters':
                create_character_files(base_path, project_path)
            case "resources":
                _create_project_folder(os.path.join(project_path, base_path))
                create_resource_files(base_path, project_path)

    for file, content in {
        '__init__.py': '',
        '__main__.py': MAIN_FILE_CONTENT,
        'configuration.py': CONFIGURATION_FILE_CONTENT.format(game_title=project_name),
        'build.py': BUILD_FILE_CONTENT,
        'validate.py': VALIDATE_FILE_CONTENT,
    }.items():
        with open(os.path.join(project_path, file), 'w') as game_file:
            game_file.write(content)

    print("Project initialized.")


def create_resource_files(base_path, project_path):
    """
    Creates the resource files for the project.

    :param base_path: The base path for the resources.
    :param project_path: The path where the project is located.
    """
    _create_project_folder(os.path.join(project_path, base_path, 'characters'))
    with open(os.path.join(project_path, base_path, 'background.png'), 'wb') as bg_file:
        bg_file.write(base64.b64decode(BACKGROUND_B64_IMAGE))

    with open(os.path.join(project_path, base_path, 'your_character.png'), 'wb') as bg_file:
        bg_file.write(base64.b64decode(CHARACTER_B64_IMAGE))

    with open(os.path.join(project_path, base_path, 'your_character_inverse.png'), 'wb') as bg_file:
        bg_file.write(base64.b64decode(CHARACTER_INVERSE_B64_IMAGE))


def create_character_files(base_path, project_path):
    """
    Creates the character files for the project.

    :param base_path: The base path for the characters.
    :param project_path: The path where the project is located.
    """
    with open(os.path.join(project_path, 'characters.py'), 'w') as example_character_file:
        example_character_file.write(CHARACTER_FILE_CONTENT.replace(
            '<path>', os.path.join(project_path, 'resources', base_path)
        ))

    path = os.path.join(project_path, 'resources', base_path, 'your_character_json.json')
    with open(path, 'w') as example_json_character_file:
        example_json_character_file.write(CHARACTER_JSON_CONTENT)


def create_scene_files(base_path, project_path):
    """
    Creates the scene files for the project.

    :param base_path: The base path for the scenes.
    :param project_path: The path where the project is located.
    """
    with open(os.path.join(project_path, base_path, '__init__.py'), 'w') as scenes_init_file:
        scenes_init_file.write(SCENE_FILE_CONTENT)
    with open(os.path.join(project_path, base_path, 'starting_scene.py'), 'w') as starting_scene_file:
        starting_scene_file.write(SAMPLE_STARTING_SCENE_FILE_CONTENT.format(project=project_path))
    with open(os.path.join(project_path, base_path, 'example_scene.py'), 'w') as example_scene_file:
        example_scene_file.write(SAMPLE_SCENE_FILE_CONTENT.format(project=project_path))
    with open(os.path.join(project_path, base_path, 'example_scene_json.py'), 'w') as example_json_scene_file:
        example_json_scene_file.write(
            SAMPLE_JSON_SCENE_FILE_CONTENT.format(
                path=os.path.join(project_path, base_path),
                project=project_path
            )
        )
    with open(os.path.join(project_path, base_path, 'json_scene.json'), 'w') as json_scene:
        json_scene.write(SCENE_JSON_CONTENT)


def _create_project_folder(project_path):
    """
    Creates the project folder.

    :param project_path: The path where the project folder will be created.
    """
    try:
        os.makedirs(project_path, exist_ok=False)
    except FileExistsError:
        print(f"Error: {project_path} already exists.")
    except Exception as e:
        print(f"Error: {e}")
