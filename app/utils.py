import sys
import time
from typing import List

class ProgressHandler:
    """Gestionnaire d'affichage de progression."""

    @staticmethod
    def display_progress(current: int, total: int, start_time: float) -> None:
        """Affiche une barre de progression en console."""
        elapsed = time.time() - start_time
        percent = (current / total) * 100
        bar_length = 40
        filled = int(bar_length * current // total)
        bar = '█' * filled + '-' * (bar_length - filled)
        
        sys.stdout.write(
            f'\r|{bar}| {percent:.1f}% ({current}/{total}) '
            f'[Temps: {elapsed:.1f}s]'
        )
        sys.stdout.flush()

class TextProcessor:
    """Utilitaire de traitement de texte."""

    @staticmethod
    def chunk_text(text: str, chunk_size: int) -> List[str]:
        """Découpe un texte en segments de taille fixe."""
        return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

    @staticmethod
    def split_paragraphs(text: str) -> List[str]:
        """Sépare le texte en paragraphes."""
        return [p.strip() for p in text.split('\n')]