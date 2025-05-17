from dataclasses import dataclass
from typing import Callable, Dict
from pathlib import Path
from app.core.translator import NLLBTranslator
from app.infrastructure.file_handlers import FileHandler
from app.config import settings
import logging

@dataclass
class Command:
    """Représente une commande exécutable"""
    execute: Callable
    description: str
    needs_input: bool = True

class CommandHandler:
    """Gestionnaire des commandes CLI"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.translator = NLLBTranslator()
        self.file_handler = FileHandler()
        self.commands = self._register_commands()

    def _register_commands(self) -> Dict[str, Command]:
        """Enregistre toutes les commandes disponibles"""
        return {
            'translate': Command(
                execute=self._execute_translation,
                description="Traduit un texte ou fichier",
                needs_input=True
            ),
            'list-langs': Command(
                execute=self._list_languages,
                description="Liste les langues supportées",
                needs_input=False
            ),
            'version': Command(
                execute=self._show_version,
                description="Affiche la version",
                needs_input=False
            )
        }

    def _execute_translation(self, args) -> None:
        """Commande de traduction principale"""
        input_path = Path(args.input)
        
        if input_path.exists() and input_path.is_file():
            content = self.file_handler.sync_read(input_path)
        else:
            content = args.input

        translated = self.translator.translate(
            content,
            args.target_lang,
            args.source_lang
        )

        if args.output:
            output_path = Path(args.output)
        else:
            output_path = input_path.with_suffix(settings.auto_output_ext)

        self.file_handler.write(translated, output_path)
        self.logger.info(f"Traduction sauvegardée dans {output_path}")

    def _list_languages(self, _) -> None:
        """Affiche les langues supportées"""
        langs = self.translator.get_supported_languages()
        print("Langues supportées:")
        for code, name in sorted(langs.items()):
            print(f"  {code:<10} {name}")

    def _show_version(self, _) -> None:
        """Affiche la version"""
        from app import __version__
        print(f"L2T Version: {__version__}")