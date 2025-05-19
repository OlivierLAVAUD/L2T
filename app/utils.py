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
    @staticmethod
    def split_paragraphs(text: str, min_chunk=3) -> List[str]:
        """Regroupe les petits paragraphes pour maintenir le contexte"""
        lines = text.split('\n')
        chunks = []
        current_chunk = []
        
        for line in lines:
            stripped = line.strip()
            if not stripped:
                if current_chunk:
                    chunks.append('\n'.join(current_chunk))
                    current_chunk = []
                chunks.append("")  # Préserve les sauts de ligne
            else:
                current_chunk.append(line)
                # Force un nouveau chunk après min_chunk lignes non vides
                if len(current_chunk) >= min_chunk:
                    chunks.append('\n'.join(current_chunk))
                    current_chunk = []
        
        if current_chunk:
            chunks.append('\n'.join(current_chunk))
            
        return chunks

        @staticmethod
        def split_into_segments(text: str, chunk_size: int) -> List[str]:
            """Découpe en segments de taille fixe en respectant les sauts de ligne"""
            # Implémentation inchangée mais à utiliser avec précaution
            return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]