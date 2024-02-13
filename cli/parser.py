import argparse
import os

from cli.installer.build import build
from cli.project_init import init_project


def validate():
    """
    Validates the project. The specific validation steps are not implemented in this function.
    """
    print("Validating...")
    # TODO implement the validation steps


def main():
    """
    The main entry point for the CLI.
    It parses the command line arguments and calls the appropriate function based on the command.
    """
    parser = argparse.ArgumentParser(description="CLI for building and validating something.")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    project_init_parsers(subparsers)
    build_parsers(subparsers)
    validate_parsers(subparsers)

    args = parser.parse_args()
    match args.command:
        case "init":
            init_project(args.project_path, args.project_name)
        case "build":
            build(args.output, os.getcwd(), args.platforms, args.resolutions, args.languages)
        case "validate":
            validate()
        case _:
            parser.print_help()


def validate_parsers(subparsers):
    """
    Adds a subparser for the "validate" command.

    :param subparsers: The ArgumentParser object to which the subparser will be added.
    """
    parser_validate = subparsers.add_parser("validate", help="Validate something")


def build_parsers(subparsers):
    """
    Adds a subparser for the "build" command.

    :param subparsers: The ArgumentParser object to which the subparser will be added.
    """
    parser_build = subparsers.add_parser("build", help="Build the project executable")
    parser_build.add_argument("--output", help="Output location for the executable file", required=True)
    parser_build.add_argument("--platforms", nargs="+", help="List of platforms")
    parser_build.add_argument("--resolutions", nargs="+", help="List of resolutions")
    parser_build.add_argument("--languages", nargs="+", help="List of languages")


def project_init_parsers(subparsers):
    """
    Adds a subparser for the "init" command.

    :param subparsers: The ArgumentParser object to which the subparser will be added.
    """
    parser_init = subparsers.add_parser("init", help="Generate project structure")
    parser_init.add_argument("project_path", help="Path where the project will be initialized")
    parser_init.add_argument("project_name", help="The name of your game project")
