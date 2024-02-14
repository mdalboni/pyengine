import unittest
from unittest.mock import MagicMock, patch

from cli.parser import (
    build_parsers,
    main,
    project_init_parsers,
    validate,
    validate_parsers,
)


class TestMainModule(unittest.TestCase):
    def setUp(self):
        self.parser = MagicMock()
        self.subparsers = MagicMock()
        self.parser.add_subparsers.return_value = self.subparsers

    @patch('cli.parser.argparse.ArgumentParser')
    def test_main(self, mock_argparse):
        mock_argparse.return_value = self.parser
        main()
        self.parser.add_subparsers.assert_called_once()
        self.parser.parse_args.assert_called_once()

    @patch('subprocess.Popen')
    @patch('sys.exit')
    def test_validate(self, mock_sys, mock_popen):
        mock_process = MagicMock()
        mock_process.communicate.return_value = (
            b'pygame 2.5.2 (SDL 2.28.3, Python 3.11.8)\nHello from the pygame community. https://www.pygame.org/contribute.html\nAnalyzing the graph...\n##########\nScene [new_scene_2] is not reachable\n##########\n',
            # noqa
            'error'
        )
        mock_popen.return_value = mock_process
        validate()
        mock_sys.assert_called_once_with(-1)

    def test_validate_parsers(self):
        validate_parsers(self.subparsers)
        self.subparsers.add_parser.assert_called_once_with("validate", help="Validate something")

    def test_build_parsers(self):
        build_parsers(self.subparsers)
        self.subparsers.add_parser.assert_called_once_with("build", help="Build the project executable")
        assert self.subparsers.add_parser().add_argument.call_count == 4

    def test_project_init_parsers(self):
        project_init_parsers(self.subparsers)
        self.subparsers.add_parser.assert_called_once_with("init", help="Generate project structure")
        assert self.subparsers.add_parser().add_argument.call_count == 2
