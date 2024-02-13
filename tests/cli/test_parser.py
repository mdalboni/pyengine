import unittest
from unittest.mock import patch, MagicMock

from cli.parser import main, validate, validate_parsers, build_parsers, project_init_parsers


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

    def test_validate(self):
        with patch('cli.parser.print') as mock_print:
            validate()
            mock_print.assert_called_once_with("Validating...")

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
