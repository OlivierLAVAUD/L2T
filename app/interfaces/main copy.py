#!/usr/bin/env python3
"""Point d'entrée principal de l'application L2T"""
import sys
import argparse
import logging
from typing import Optional, List
from app.core.commands import CommandHandler
from app.infrastructure.gpu import GPUManager
from app.utils.logger import setup_logging
from app.config import settings
from app.interfaces.cli import CLICommand

class L2TApplication:
    """Classe principale gérant le cycle de vie de l'application"""
    def __init__(self):
        self.logger = setup_logging()
        self.command_handler = CommandHandler()
        self.parser = self._create_parser()

    def _create_parser(self) -> argparse.ArgumentParser:
        """Configure le parser d'arguments CLI"""
        parser = argparse.ArgumentParser(
            prog="l2t",
            description="L2T - Outil de traduction avancé utilisant NLLB-200",
            epilog="Exemples d'utilisation:\n"
                   "  l2t 'Hello world' -t fra_Latn\n"
                   "  l2t document.txt -o traduction.txt",
            formatter_class=argparse.RawDescriptionHelpFormatter
        )
        # Arguments principaux
        parser.add_argument(
            'input',
            help="Texte à traduire ou chemin vers un fichier (.txt, .pdf)"
        )
        # Options de langue
        lang_group = parser.add_argument_group('Options de langue')
        lang_group.add_argument(
            '-t', '--target-lang',
            required=True,
            help="Code langue cible (ex: fra_Latn)"
        )
        lang_group.add_argument(
            '-s', '--source-lang',
            help="Code langue source (détection automatique si omis)"
        )
        # Options de sortie
        output_group = parser.add_argument_group('Options de sortie')
        output_group.add_argument(
            '-o', '--output',
            help="Fichier de sortie (généré automatiquement si omis)"
        )
        output_group.add_argument(
            '--verbose',
            action='store_true',
            help="Afficher les logs détaillés"
        )
        # Commandes spéciales
        parser.add_argument(
            '--list-languages',
            action='store_true',
            help="Lister les langues supportées"
        )
        parser.add_argument(
            '--version',
            action='store_true',
            help="Afficher la version"
        )
        return parser

    def run(self, argv: Optional[List[str]] = None) -> int:
        """
        Point d'entrée principal
        :param argv: Arguments CLI (sys.argv par défaut)
        :return: Code de sortie (0 = succès)
        """
        try:
            with GPUManager():
                args = self.parser.parse_args(argv)
                self._configure_logging(args.verbose)

                # Affichage version simple si demandé
                if args.version:
                    print(f"L2T - Version {settings.version}")
                    return 0

                return self._execute_command(args)
        except KeyboardInterrupt:
            self.logger.warning("Traduction interrompue par l'utilisateur")
            return 0
        except Exception as e:
            self.logger.critical(f"Erreur: {str(e)}", exc_info=settings.debug)
            return 1

    def _configure_logging(self, verbose: bool):
        """Configure le niveau de logging"""
        if verbose:
            self.logger.setLevel(logging.DEBUG)
            self.logger.debug("Mode verbeux activé")

    def _execute_command(self, args: argparse.Namespace) -> int:
        """Exécute la commande appropriée"""
        cli_command = CLICommand()
        cli_command.execute(args)
        return 0

def main():
    """Fonction d'entrée pour setuptools"""
    app = L2TApplication()
    sys.exit(app.run())

if __name__ == "__main__":
    main()
