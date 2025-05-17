import sys
from typing import Iterable, TypeVar
from app.config import settings
import time

T = TypeVar('T')

class ProgressBar:
    """Affiche une barre de progression élégante"""
    
    def __init__(self, iterable: Iterable[T], desc: str = ""):
        self.iterable = iterable
        self.desc = desc
        self.length = len(iterable) if hasattr(iterable, '__len__') else None
        self.start_time = time.time()

    def __iter__(self):
        for i, item in enumerate(self.iterable, 1):
            yield item
            self._update_progress(i)

    def _update_progress(self, current: int) -> None:
        """Met à jour l'affichage de la progression"""
        if not settings.debug and self.length:
            percent = current / self.length
            bar = '█' * int(50 * percent)
            elapsed = time.time() - self.start_time
            remaining = (elapsed / current) * (self.length - current) if current > 0 else 0
            
            sys.stdout.write(
                f"\r{self.desc} |{bar.ljust(50)}| "
                f"{current}/{self.length} "
                f"[{elapsed:.1f}s<{remaining:.1f}s]"
            )
            sys.stdout.flush()

            if current == self.length:
                print()