import argparse
from pathlib import Path
from typing import Optional
from datetime import datetime
import logging
from app.config import settings
from app.core.translator import NLLBTranslator
from app.infrastructure.file_handlers import FileHandler
from app.core.models import TranslationInput, TranslationResult

class CLICommand:
    def __init__(self):
        self.logger = self._setup_logging()
        self.translator = NLLBTranslator()
        self.file_handler = FileHandler()

    def _setup_logging(self) -> logging.Logger:
        logging.basicConfig(
            filename=settings.log_path / settings.log_file,
            level=logging.DEBUG if settings.debug else logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        return logging.getLogger("L2T_CLI")

    def execute(self, args: argparse.Namespace) -> None:
        """Point d'entrée principal"""
        start_time = datetime.now()

        try:
            if args.list_languages:
                self._list_languages()
                return

            content = self._get_content(args.input)
            translated = self._translate(content, args.target_lang, args.source_lang)
            self._output_result(translated, args.output, args.input)

        except Exception as e:
            self.logger.error(f"Erreur: {str(e)}", exc_info=settings.debug)
            raise
        finally:
            self.logger.info(f"Temps d'exécution: {datetime.now() - start_time}")

    def _get_content(self, input_path: str) -> str:
        """Récupère le contenu depuis un fichier ou texte direct"""
        path = Path(input_path)
        if path.exists() and path.is_file():
            return self.file_handler.sync_read(path)
        return input_path

    def _translate(self, content: str, target_lang: str, source_lang: Optional[str]) -> str:
        """Gère la traduction avec gestion des chunks"""
        if len(content) <= settings.chunk_size:
            input_data = TranslationInput(text=content, source_lang=source_lang, target_lang=target_lang)
            return self.translator.translate(input_data).translated_text

        # Traduction par chunks pour les gros textes
        paragraphs = content.split("\n")
        translated = []
        for i, para in enumerate(paragraphs, 1):
            if para.strip():
                input_data = TranslationInput(text=para, source_lang=source_lang, target_lang=target_lang)
                translated.append(self.translator.translate(input_data).translated_text)
            else:
                translated.append("")
            self._log_progress(i, len(paragraphs))
        return "\n".join(translated)

    def _output_result(self, content: str, output_path: Optional[str], input_path: str) -> None:
        """Gère la sortie vers fichier ou console"""
        if output_path:
            path = Path(output_path)
        else:
            path = Path(input_path).with_suffix(settings.auto_output_ext)

        if path.suffix:
            self.file_handler.write(content, path)
            self.logger.info(f"Résultat sauvegardé dans {path}")
        else:
            print(content[:1000] + ("..." if len(content) > 1000 else ""))

    def _list_languages(self) -> None:
        """Affiche les langues supportées"""
        langs = self.translator.get_supported_languages()
        print("Langues supportées:")
        for code, name in sorted(langs.items()):
            print(f"  {code:<10} {name}")

    def _log_progress(self, current: int, total: int) -> None:
        """Affiche la progression"""
        if current % 10 == 0 or current == total:
            self.logger.info(f"Progression: {current}/{total} ({current/total:.1%})")