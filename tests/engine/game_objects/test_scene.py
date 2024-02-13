import unittest

from engine.game_objects.action import Action, Choice
from engine.game_objects.character import Character
from engine.game_objects.scene import Scene


class TestScene(unittest.TestCase):

    def setUp(self):
        self.character = Character('Test Character', 'state', {'state': 'image.png'})
        self.action = Action(self.character, 'state')
        self.choice = Choice(self.character, 'Choose', [('1', 'One')], 'state')
        self.scene = Scene('Test Scene', 'background.png')

    def test_scene_init(self):
        self.assertEqual(self.scene.name, 'Test Scene')
        self.assertEqual(self.scene.background, 'background.png')
        self.assertEqual(self.scene.actions, [])
        self.assertEqual(self.scene.history, [])
        self.assertEqual(self.scene.action, 0)

    def test_scene_add_action(self):
        self.scene.add_action(self.action)
        self.assertEqual(self.scene.actions, [self.action])

    def test_scene_execute_next_action(self):
        self.scene.add_action(self.action)
        result = self.scene.execute_next_action()
        self.assertEqual(result, self.action)
        self.assertEqual(self.scene.history, [self.action])
        self.assertEqual(self.scene.action, 1)

    def test_scene_str(self):
        self.scene.add_action(self.action)
        result = str(self.scene)
        self.assertEqual(result, 'Test Scene - 1/1\n[\'1: action - Test Character[STATE]\']')

    def test_scene_add_action_exception(self):
        self.scene.add_action(self.choice)
        with self.assertRaises(Exception):
            self.scene.add_action(self.action)


if __name__ == '__main__':
    unittest.main()
