import argparse
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Optional, List

from .logger import setup_logging, log_execution_time
from .translator import NLLBTranslationService
from .file_handlers import FileHandler
from .utils import ProgressVisualizer, TextSegmenter
import torch 

class NLLBTranslationCLI:
    """Interface en ligne de commande pour le service de traduction NLLB"""

    def __init__(self):
        self.logger = setup_logging()
        self.translation_service = NLLBTranslationService()
        self.command_args = self._setup_command_line_interface()
        self.execution_start_time = datetime.now()

    def _setup_command_line_interface(self) -> argparse.Namespace:
        """Configure les arguments de la ligne de commande"""
        argument_parser = argparse.ArgumentParser(
            description="Interface CLI pour le service de traduction NLLB (Optimisé GPU)",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )

        # Arguments principaux
        argument_parser.add_argument(
            'input',
            nargs='?',
            help="Texte à traduire ou chemin vers un fichier (.txt/.pdf)"
        )

        # Options de langue
        argument_parser.add_argument(
            '-t', '--target-language',
            help="Code de la langue cible (ex: fra_Latn)"
        )
        argument_parser.add_argument(
            '-s', '--source-language',
            help="Code de la langue source (détection automatique si omis)"
        )
        argument_parser.add_argument(
            '--list-languages',
            action='store_true',
            help="Affiche la liste des langues supportées"
        )

        # Options de traitement
        argument_parser.add_argument(
            '-o', '--output-file',
            help="Fichier de sortie pour la traduction"
        )
        argument_parser.add_argument(
            '-e', '--encoding',
            default='utf-8',
            help="Encodage des fichiers texte"
        )
        argument_parser.add_argument(
            '-c', '--chunk-size',
            type=int,
            default=500,
            help="Taille maximale des segments de texte à traduire"
        )
        argument_parser.add_argument(
            '--batch-size',
            type=int,
            default=8,
            help="Nombre de segments à traduire simultanément (optimisation GPU)"
        )
        argument_parser.add_argument(
            '--debug-mode',
            action='store_true',
            help="Active le mode debug pour le logging"
        )
        argument_parser.add_argument(
            '-f', '--file',
            action='store_true',
            help="Indique que l'entrée est un fichier"
        )

        return argument_parser.parse_args()

    def run(self) -> None:
        """Point d'entrée principal (compatibilité avec main.py)"""

        # Dans votre code principal
    #    translator = NLLBTranslationService()

        # Rechargement standard (utilise le cache si disponible)
    #    translator.reload_model()

        # Rechargement forcé + suppression cache local
    #    translator.reload_model(force_download=True)


        self.execute()

    def execute(self) -> None:
        """Nouveau point d'entrée principal de l'application CLI"""
        try:
            if self.command_args.list_languages:
                self._show_available_languages()
                return

            self._validate_command_arguments()
            input_content = self._load_input_content()
            translated_content = self._process_translation(input_content)
            self._save_or_display_result(translated_content)

        except KeyboardInterrupt:
            self.logger.info("Traduction annulée par l'utilisateur")
            sys.exit(0)
        except Exception as error:
            self.logger.critical(
                f"Erreur critique: {str(error)}",
                exc_info=self.command_args.debug_mode
            )
            sys.exit(1)
        finally:
            log_execution_time(
                self.execution_start_time,
                "Temps total d'exécution"
            )

    def _validate_command_arguments(self):
        """Valide les arguments fournis en ligne de commande"""
        if not self.command_args.input:
            raise ValueError("Aucune entrée spécifiée (texte ou fichier)")

        if not self.command_args.source_language:
            raise ValueError("Langue source non spécifiée (option -s/--source-language requise)")

        if not self.command_args.target_language:
            raise ValueError("Langue cible non spécifiée (option -t/--target-language requise)")

        # Validation des codes de langue
        for lang_type in ['source', 'target']:
            lang = getattr(self.command_args, f"{lang_type}_language")
            if not self.translation_service.is_language_supported(lang):
                raise ValueError(f"Langue {lang_type} non supportée: {lang}")

    """       if not self.translation_service.is_language_supported(self.command_args.target_language):
            raise ValueError(f"Langue cible non supportée: {self.command_args.target_language}")
    """

    def _show_available_languages(self):
        """Affiche les langues disponibles dans un format lisible"""
        languages = self.translation_service.get_supported_languages()
        print("\nLangues supportées par le service de traduction:")
        for language_code, language_name in languages.items():
            print(f"  {language_code:12} → {language_name}")

    def _load_input_content(self) -> str:
        """Charge le contenu à traduire depuis un fichier ou une chaîne directe"""
        if self.command_args.file:
            input_path = Path(self.command_args.input)
            if not input_path.exists():
                raise FileNotFoundError(f"Fichier introuvable: {input_path}")
            if input_path.is_dir():
                raise IsADirectoryError(f"Le chemin spécifié est un répertoire : {input_path}")
            return FileHandler.read_file(input_path, self.command_args.encoding)
        else:
            return self.command_args.input

    def _process_translation(self, content: str) -> str:
        """Gère le processus de traduction avec gestion des erreurs"""
        if not content.strip():
            raise ValueError("Le contenu à traduire est vide")

        # Traduction directe pour les petits textes
        if len(content) <= self.command_args.chunk_size:
            try:
                return self.translation_service.translate_text(
                    content,
                    self.command_args.target_language,
                    self.command_args.source_language
                )
            except Exception as error:
                self.logger.error(f"Échec de la traduction: {str(error)}")
                raise

        # Traduction segmentée pour les gros textes
        try:
            self.logger.info("Début de la traduction segmentée...")
            result = self._translate_large_content(content)
            self.logger.info("Traduction segmentée terminée avec succès")
            return result
        except Exception as error:
            self.logger.error(f"Échec de la traduction segmentée: {str(error)}")
            raise

    def _translate_large_content(self, content: str) -> str:
        """Traduit un contenu volumineux en gérant les erreurs de marqueurs et la mémoire
        
        Args:
            content: Texte source à traduire
            
        Returns:
            Texte traduit avec structure préservée
        """
        paragraphs = TextSegmenter.split_paragraphs(content)
        translated_segments = []
        start_time = time.time()
        total_paragraphs = len(paragraphs)
        
        self.logger.debug(f"Début traduction de {total_paragraphs} paragraphes")

        for idx, paragraph in enumerate(paragraphs, 1):
            try:
                # Gestion des paragraphes vides
                if not paragraph.strip():
                    translated_segments.append("")
                    ProgressVisualizer.display_progress(idx, total_paragraphs, start_time)
                    continue
               
                # Traduction avec suivi de mémoire
                if torch.cuda.is_available():
                    torch.cuda.empty_cache()
        
            
                translated = self.translation_service.translate_text(
                    paragraph,
                    self.command_args.target_language,
                    self.command_args.source_language
                )
                
                # Validation et correction du résultat
                final_text = translated.replace("[CONTECT", "[CONTEXT")
                if final_text != translated:
                    self.logger.debug(f"Corrigé marqueur dans le paragraphe {idx}")
                    
                translated_segments.append(final_text)
                
            except Exception as e:
                self.logger.error(f"Erreur paragraphe {idx}: {str(e)}")
                translated_segments.append(f"[ERROR: {paragraph[:50]}...]")
                
            ProgressVisualizer.display_progress(idx, total_paragraphs, start_time)

        self.logger.info(f"Traduction terminée - {total_paragraphs} paragraphes traités")
        return "\n".join(translated_segments)
    
    def _save_or_display_result(self, translated_text: str) -> None:
        """Gère la sortie du résultat (fichier ou affichage console)"""
        output_path = self._determine_output_path()

        if output_path:
            try:
                FileHandler.write_output(
                    translated_text,
                    output_path,
                    self.command_args.encoding
                )
                self.logger.info(f"Résultat sauvegardé dans: {output_path}")
            except Exception as error:
                raise IOError(f"Erreur lors de la sauvegarde: {str(error)}")
        else:
            # Affichage d'un aperçu si pas de fichier de sortie spécifié
            preview = (translated_text[:500] + "...") if len(translated_text) > 500 else translated_text
        #    print("\n=== RESULTAT DE LA TRADUCTION ===")
            print('[l2t]:<',preview,'>')
        #    print("===============================")

    def _determine_output_path(self) -> Optional[Path]:
        """Détermine le chemin de sortie automatiquement si besoin"""
        if self.command_args.output_file:
            return Path(self.command_args.output_file)

        if self.command_args.file:
            input_path = Path(self.command_args.input)
            if input_path.is_file():
                lang_code = self.command_args.target_language.replace('_', '-')
                return input_path.parent / f"{input_path.stem}_{lang_code}_translated.txt"

        return None