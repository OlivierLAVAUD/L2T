import time
import torch
from typing import Dict, Optional
import logging
from threading import Thread, Event

logger = logging.getLogger(__name__)

class GPUMonitor(Thread):
    """Surveillance en temps réel de l'utilisation GPU"""

    def __init__(self, interval: float = 1.0):
        super().__init__(daemon=True)
        self.interval = interval
        self.stop_event = Event()
        self.stats: Dict[str, list] = {
            'allocated': [],
            'reserved': [],
            'utilization': []
        }

    def run(self):
        """Lance la surveillance"""
        logger.info("Démarrage du moniteur GPU")
        while not self.stop_event.is_set():
            self._record_stats()
            time.sleep(self.interval)

    def _record_stats(self):
        """Enregistre les statistiques actuelles"""
        if torch.cuda.is_available():
            mem = {
                'allocated': torch.cuda.memory_allocated() / 1024**2,
                'reserved': torch.cuda.memory_reserved() / 1024**2,
                'utilization': torch.cuda.utilization()
            }
            for k, v in mem.items():
                self.stats[k].append(v)

    def stop(self):
        """Arrête la surveillance"""
        self.stop_event.set()
        logger.info("Moniteur GPU arrêté")

    def get_report(self) -> dict:
        """Génère un rapport d'utilisation"""
        if not self.stats['allocated']:
            return {}
        
        return {
            'max_allocated': max(self.stats['allocated']),
            'avg_reserved': sum(self.stats['reserved']) / len(self.stats['reserved']),
            'peak_utilization': max(self.stats['utilization'])
        }