import torch
from app.config import settings
import logging

logger = logging.getLogger(__name__)

def configure_torch():
    """Configure PyTorch pour des performances optimales"""
    if settings.use_gpu and torch.cuda.is_available():
        torch.backends.cudnn.benchmark = True
        torch.backends.cudnn.deterministic = False
        torch.set_float32_matmul_precision(settings.torch_precision)
        logger.debug("Optimisations GPU activées")

def clear_cache():
    """Vide le cache GPU"""
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        logger.debug("Cache GPU vidé")

def get_memory_usage() -> dict:
    """Retourne l'utilisation mémoire GPU"""
    if not torch.cuda.is_available():
        return {}
    
    return {
        'allocated': torch.cuda.memory_allocated() / 1024**2,
        'reserved': torch.cuda.memory_reserved() / 1024**2,
        'free': torch.cuda.memory_reserved() - torch.cuda.memory_allocated()
    }