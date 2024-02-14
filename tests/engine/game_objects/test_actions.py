import unittest

from engine.game_objects.action import Action, Talk, Choice, GoTo
from engine.game_objects.character import Character


class TestAction(unittest.TestCase):

    def setUp(self):
        self.character = Character('Test Character', state='state', states={'state': 'image.png'})
        self.action = Action(self.character, 'state')

    def test_action_init(self):
        self.assertEqual(self.action.character.name, 'Test Character')
        self.assertEqual(self.action.character.state, 'STATE')
        self.assertEqual(self.action.type, 'action')

    def test_action_render(self):
        result = self.action.render()
        self.assertEqual(result['character_name'], 'Test Character')
        self.assertEqual(result['character_image'], 'image.png')
        self.assertEqual(result['type'], 'action')

    def test_action_dump(self):
        result = self.action.dump()
        self.assertEqual(result['character'], 'TEST CHARACTER')
        self.assertEqual(result['state'], 'STATE')
        self.assertEqual(result['type'], 'action')

    def test_action_str(self):
        result = str(self.action)
        self.assertEqual(result, f"{self.action.type} - {self.character.name}[{self.character.state}]")

    def test_go_to(self):
        self.assertEqual(self.action.go_to(), None)


class TestTalk(unittest.TestCase):

    def setUp(self):
        self.character = Character('Test Character', state='state', states={'state': 'image.png'})
        self.talk = Talk(self.character, 'Hello', 'state')

    def test_talk_init(self):
        self.assertEqual(self.talk.character.name, 'Test Character')
        self.assertEqual(self.talk.character.state, 'STATE')
        self.assertEqual(self.talk.text, 'Hello')
        self.assertEqual(self.talk.type, 'talk')

    def test_talk_render(self):
        result = self.talk.render()
        self.assertEqual(result['character_name'], 'Test Character')
        self.assertEqual(result['character_image'], 'image.png')
        self.assertEqual(result['text'], 'Hello')
        self.assertEqual(result['type'], 'talk')

    def test_talk_dump(self):
        result = self.talk.dump('en', 'fr')
        self.assertEqual(result['character'], 'TEST CHARACTER')
        self.assertEqual(result['state'], 'STATE')
        self.assertEqual(result['type'], 'talk')
        self.assertEqual(result['text'], 'Bonjour')

    def test_go_to(self):
        self.assertEqual(self.talk.go_to(), None)


class TestChoice(unittest.TestCase):

    def setUp(self):
        self.character = Character('Test Character', state='state', states={'state': 'image.png'})
        self.choice = Choice(self.character, 'Choose', [('1', 'One')], 'state')

    def test_choice_init(self):
        self.assertEqual(self.choice.character.name, 'Test Character')
        self.assertEqual(self.choice.character.state, 'STATE')
        self.assertEqual(self.choice.text, 'Choose')
        self.assertEqual(self.choice.choices, [('1', 'One')])
        self.assertEqual(self.choice.type, 'choice')

    def test_choice_render(self):
        result = self.choice.render()
        self.assertEqual(result['character_name'], 'Test Character')
        self.assertEqual(result['character_image'], 'image.png')
        self.assertEqual(result['text'], 'Choose')
        self.assertEqual(result['choices'], [('1', 'One')])
        self.assertEqual(result['type'], 'choice')

    def test_choice_dump(self):
        result = self.choice.dump('en', 'fr')
        self.assertEqual(result['character'], 'TEST CHARACTER')
        self.assertEqual(result['state'], 'STATE')
        self.assertEqual(result['type'], 'choice')
        self.assertEqual(result['text'], 'Choisir')
        self.assertEqual(result['choices'], [{'go_to': '1', 'text': 'Un'}])

    def test_go_to(self):
        self.assertEqual(self.choice.go_to(), ['1'])


class TestGoTo(unittest.TestCase):

    def setUp(self):
        self.character = Character('Test Character', state='state', states={'state': 'image.png'})
        self.goto = GoTo(self.character, 'Go', '1', 'state')

    def test_goto_init(self):
        self.assertEqual(self.goto.character.name, 'Test Character')
        self.assertEqual(self.goto.character.state, 'STATE')
        self.assertEqual(self.goto.text, 'Go')
        self.assertEqual(self.goto._go_to, '1')
        self.assertEqual(self.goto.type, 'go_to')

    def test_goto_render(self):
        result = self.goto.render()
        self.assertEqual(result['character_name'], 'Test Character')
        self.assertEqual(result['character_image'], 'image.png')
        self.assertEqual(result['text'], 'Go')
        self.assertEqual(result['go_to'], '1')
        self.assertEqual(result['type'], 'go_to')

    def test_goto_dump(self):
        result = self.goto.dump('en', 'fr')
        self.assertEqual(result['character'], 'TEST CHARACTER')
        self.assertEqual(result['state'], 'STATE')
        self.assertEqual(result['type'], 'go_to')
        # Assuming the translation function works correctly, 'Go' in English translates to 'Aller' in French
        self.assertEqual(result['text'], 'Aller')
        self.assertEqual(result['go_to'], '1')

    def test_go_to(self):
        self.assertEqual(self.goto.go_to(), ['1'])
