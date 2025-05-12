import argparse
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Optional

from .logger import setup_logging, log_execution_time
from .translator import NLLBTranslator
from .file_handlers import FileHandler
from .utils import ProgressHandler, TextProcessor

class TranslationCLI:
    """Interface CLI optimisée pour la traduction NLLB-200"""

    def __init__(self):
        self.logger = setup_logging()
        self.translator = NLLBTranslator()
        self.args = self._parse_arguments()
        self.start_time = datetime.now()

    def _parse_arguments(self) -> argparse.Namespace:
        """Configure les arguments CLI"""
        parser = argparse.ArgumentParser(
            description="Traducteur CLI NLLB-200 (Optimisé GPU)",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )

        # Arguments principaux
        parser.add_argument('input', nargs='?', help="Texte ou fichier à traduire (.txt/.pdf)")

        # Options de langue
        parser.add_argument('-l', '--lang', help="Code langue cible (ex: fra_Latn)")
        parser.add_argument('-s', '--source-lang', help="Code langue source")
        parser.add_argument('--list-languages', action='store_true', help="Affiche les langues supportées")

        # Options techniques
        parser.add_argument('-o', '--output', help="Fichier de sortie")
        parser.add_argument('-e', '--encoding', default='utf-8', help="Encodage des fichiers")
        parser.add_argument('-c', '--chunk-size', type=int, default=500, help="Taille des segments")
        parser.add_argument('--batch-size', type=int, default=8, help="Taille des batchs GPU")
        parser.add_argument('--debug', action='store_true', help="Mode debug")

        return parser.parse_args()

    def run(self) -> None:
        """Point d'entrée principal"""
        try:
            if self.args.list_languages:
                self._display_supported_languages()
                return

            self._validate_arguments()
            content = self._load_content()
            translated = self._translate_content(content)
            self._handle_output(translated)

        except KeyboardInterrupt:
            self.logger.info("Traduction interrompue")
            sys.exit(0)
        except Exception as e:
            self.logger.critical(f"Erreur: {str(e)}", exc_info=self.args.debug)
            sys.exit(1)
        finally:
            log_execution_time(self.start_time, "Traduction terminée")

    def _validate_arguments(self):
        """Valide les arguments"""
        if not self.args.input:
            raise ValueError("Aucun texte ou fichier spécifié")

        if not self.translator.is_language_supported(self.args.lang):
            raise ValueError(f"Langue cible non supportée: {self.args.lang}")

    def _display_supported_languages(self):
        """Affiche les langues disponibles"""
        langs = self.translator.get_supported_languages()
        print("\nLangues supportées:")
        for code, name in langs.items():
            print(f"  {code}: {name}")

    def _load_content(self) -> str:
        """Charge le contenu à traduire"""
        input_path = Path(self.args.input)

        if not input_path.exists() and len(self.args.input) < 1000:
            return self.args.input

        try:
            if input_path.is_file():
                return FileHandler.read_file(input_path, self.args.encoding)
            raise FileNotFoundError(f"Fichier introuvable: {input_path}")
        except Exception as e:
            raise IOError(f"Erreur lecture: {str(e)}")

    def _translate_content(self, content: str) -> str:
        """Gère la traduction avec optimisations et progression"""
        if not content.strip():
            raise ValueError("Contenu vide")

        # Petit texte : traduction directe sans progression
        if len(content) <= self.args.chunk_size:
            try:
                return self.translator.translate(content, self.args.lang, self.args.source_lang)
            except Exception as e:
                self.logger.error(f"Échec traduction: {str(e)}")
                raise

        # Gros texte : avec barre de progression
        try:
            self.logger.info("Lancement de la traduction segmentée...")
            result = self._translate_in_chunks(content)
            self.logger.info("Traduction segmentée terminée avec succès")
            return result
        except Exception as e:
            self.logger.error(f"Échec traduction segmentée: {str(e)}")
            raise

    def _translate_in_chunks(self, content: str) -> str:
        # Traduction par segments avec progression visuelle
        paragraphs = TextProcessor.split_paragraphs(content)
        total = len(paragraphs)
        results = []
        start_time = time.time()

        print(f"\nTraduction de {total} segments:")
        ProgressHandler.display_progress(0, total, start_time)

        for i, para in enumerate(paragraphs, 1):
            if not para.strip():
                results.append("")
                continue

            try:
                # Traduction du segment
                translated = self.translator.translate(para, self.args.lang, self.args.source_lang)
                results.append(translated)
            except Exception as e:
                self.logger.warning(f"Erreur segment {i}: {str(e)}")
                results.append("[ERREUR]")

            # Mise à jour de la progression (optimisée pour performance)
            if i % max(1, total//100) == 0 or i == total:  # 100 updates max
                ProgressHandler.display_progress(i, total, start_time)

        print()  # Retour à la ligne final
        return "\n".join(results)

    def _handle_output(self, translated_text: str) -> None:
        """Gère la sortie avec génération automatique du nom de fichier"""
        input_path = Path(self.args.input)
        output_path = self._generate_output_path(input_path)

        if output_path:
            try:
                FileHandler.write_output(translated_text, output_path, self.args.encoding)
                self.logger.info(f"Traduction sauvegardée dans {output_path}")
            except Exception as e:
                raise IOError(f"Erreur sauvegarde: {str(e)}")
        else:
            # Affichage console si pas de fichier source
            preview = translated_text[:500] + ("..." if len(translated_text) > 500 else "")
            print("\n=== TRADUCTION ===")
            print(preview)
            print("=================")

    def _generate_output_path(self, input_path: Path) -> Path:
        """Génère le chemin de sortie automatiquement si -o non spécifié"""
        if not self.args.output and input_path.is_file():
            lang_code = self.args.lang.replace('_', '-')  # Pour éviter les problèmes de fichiers
            return input_path.parent / f"{input_path.stem}.{lang_code}.T2L.txt"
        return Path(self.args.output) if self.args.output else None