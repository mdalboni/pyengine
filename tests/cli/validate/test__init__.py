import unittest
from unittest.mock import MagicMock, patch

from cli.parser import validate, validate_parsers


class TestMainModule(unittest.TestCase):
    def setUp(self):
        self.parser = MagicMock()
        self.subparsers = MagicMock()
        self.parser.add_subparsers.return_value = self.subparsers

    @patch('subprocess.Popen')
    @patch('sys.exit')
    def test_validate(self, mock_sys, mock_popen):
        mock_process = MagicMock()
        mock_process.communicate.return_value = (
            b'pygame 2.5.2 (SDL 2.28.3, Python 3.11.8)\nHello from the pygame community. '
            b'https://www.pygame.org/contribute.html\nAnalyzing the graph...\n##########\nScene [new_scene_2] is not '
            b'reachable\n##########\n',
            'error'
        )
        mock_popen.return_value = mock_process
        validate()
        mock_sys.assert_called_once_with(-1)

    def test_validate_parsers(self):
        validate_parsers(self.subparsers)
        self.subparsers.add_parser.assert_called_once_with("validate", help="Validate something")
