from deep_translator import GoogleTranslator


def translate(value: str, source: str, target: str):
    return GoogleTranslator(source=source, target=target).translate(value)
