"""
This module contains the build functionality for the game engine.
It includes the main build function, a function to build the application,
a function to build the game JSON files, and a function to validate the necessary files.
"""

import os
import shutil
import subprocess

import PyInstaller.__main__ as py_installer


def build(
        output_path: str,
        project_path: str,
        platforms: list[str],
        resolutions: list[str],
        languages: list[str]
):
    """
    Main build function. Prepares for building, validates files, builds game JSONs and the application.

    :param output_path: The path where the built application will be output.
    :param project_path: The path of the project to be built.
    :param platforms: The platforms for which the game will be built.
    :param resolutions: The resolutions for which the game will be built.
    :param languages: The languages for which the game will be built.
    """
    print("Preparing for building...")
    print("Platforms:", platforms)  # TODO select the platforms to be used
    print("Resolutions:", resolutions)  # TODO select the resolutions to be used
    print("Languages:", languages)  # TODO display languages

    validate_files(project_path)
    build_main_path, game_name = build_game_jsons()
    data_path = os.path.dirname(build_main_path)
    build_app(build_main_path, data_path, game_name, output_path)


def build_app(build_main_path, data_path, game_name, output_path):
    """
    Builds the application using PyInstaller.

    :param build_main_path: The path of the main build file.
    :param data_path: The path of the data files.
    :param game_name: The name of the game.
    :param output_path: The path where the built application will be output.
    """
    options = [
        build_main_path,
        '--onefile',  # Create a single executable file
        '--clean',  # Clean PyInstaller cache and temporary files
        f'--distpath={output_path}',  # Output path
        f'--name={game_name}',  # Name of the executable
    ]
    data_files = [
        f'--add-data={data_path};.',  # Add the resources folder to the executable
    ]
    py_installer.run(options + data_files)
    shutil.rmtree(data_path, ignore_errors=True)


def build_game_jsons():
    """
    Builds the game JSON files by running the build.py script.

    :return: The path of the main build file and the name of the game.
    """
    cmd = 'python build.py'
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    out, err = p.communicate()
    build_main_path, game_name = out.decode().split('\n')[-2:][0].split('#')[1:3]
    return build_main_path, game_name


def validate_files(project_path):
    """
    Validates the necessary files for building the game.

    :param project_path: The path of the project to be validated.
    """
    files = os.listdir(project_path)
    required_files = [
        '__init__.py',
        '__main__.py',
        'configuration.py',
        'build.py',
        'characters.py'
    ]
    for file in required_files:
        if file not in files:
            print("Missing file:", file)
            raise Exception("Missing file")  # TODO improve exceptions
