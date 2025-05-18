import sys
import time
from typing import List

class ProgressVisualizer:
    """Gestion simplifiée de la progression"""
    
    @staticmethod
    def display_progress(current: int, total: int, start_time: float) -> None:
        """Affiche la barre de progression"""
        elapsed = time.time() - start_time
        percent = (current / total) * 100
        bar_length = 40
        filled = int(bar_length * current // total)
        bar = '█' * filled + '-' * (bar_length - filled)
        
        sys.stdout.write(
            f'\r|{bar}| {percent:.1f}% ({current}/{total}) '
            f'[Elapsed: {elapsed:.1f}s]'
        )
        sys.stdout.flush()

class TextSegmenter:
    """Simplification de l'ancien TextProcessor"""
    
    @staticmethod
    def split_paragraphs(text: str) -> List[str]:
        """Sépare le texte en paragraphes (identique à l'ancienne version)"""
        return [p.strip() for p in text.split('\n') if p.strip()]
    
    @staticmethod
    def split_into_segments(text: str, chunk_size: int) -> List[str]:
        """Découpe en segments de taille fixe (identique à l'ancienne version)"""
        return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]