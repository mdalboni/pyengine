CONFIGURATION_FILE_CONTENT = """
from engine.game_ui.game import Configuration

GAME_CONFIGURATION = Configuration(
    resource_folder='./resources',
    language='en',
    languages=['pt', 'en'],
    game_title="{game_title}",
)
"""
