from importlib.resources import files
import json

def load_sample_text(lang_code: str) -> str:
    """Charge un texte d'exemple depuis les ressources"""
    try:
        return files('resources').joinpath(f'samples/{lang_code}.txt').read_text()
    except FileNotFoundError:
        return ""

def load_language_mapping() -> dict:
    """Charge le mapping des langues"""
    return json.loads(files('resources').joinpath('languages/mapping.json').read_text())