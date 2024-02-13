import unittest

from engine.game_objects.character import Character, _GameCharacter


class TestCharacter(unittest.TestCase):

    def setUp(self):
        self.character = Character('Test Character', 'state', {'state': 'image.png'})

    def test_character_init(self):
        self.assertEqual(self.character.name, 'Test Character')
        self.assertEqual(self.character.state, 'STATE')
        self.assertEqual(self.character.states, {'STATE': 'image.png'})

    def test_character_snapshot(self):
        snapshot = self.character.snapshot()
        self.assertEqual(snapshot.name, 'Test Character')
        self.assertEqual(snapshot.image, 'image.png')
        self.assertEqual(snapshot.state, 'STATE')

    def test_character_str(self):
        result = str(self.character)
        self.assertEqual(result, 'Test Character[STATE]')


class TestGameCharacter(unittest.TestCase):

    def setUp(self):
        self.game_character = _GameCharacter('Test Character', 'image.png', 'state')

    def test_game_character_init(self):
        self.assertEqual(self.game_character.name, 'Test Character')
        self.assertEqual(self.game_character.image, 'image.png')
        self.assertEqual(self.game_character.state, 'state')
