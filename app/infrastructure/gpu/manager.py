import torch
from contextlib import contextmanager
from app.config import settings
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class GPUManager:
    """Gestionnaire contextuel des ressources GPU"""

    def __init__(self, device_id: Optional[int] = None):
        self.device_id = device_id
        self.original_device = None

    def __enter__(self):
        if settings.use_gpu and torch.cuda.is_available():
            self.original_device = torch.cuda.current_device()
            device = f'cuda:{self.device_id}' if self.device_id else 'cuda'
            torch.cuda.set_device(device)
            logger.info(f"GPU activé sur {torch.cuda.get_device_name()}")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if settings.use_gpu and torch.cuda.is_available():
            if self.original_device:
                torch.cuda.set_device(self.original_device)
            torch.cuda.empty_cache()
            logger.info("Mémoire GPU libérée")

    @staticmethod
    def get_available_devices() -> list:
        """Liste les devices GPU disponibles"""
        return [
            f"cuda:{i}" for i in range(torch.cuda.device_count())
        ] if torch.cuda.is_available() else []