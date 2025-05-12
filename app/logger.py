import logging
from datetime import datetime
from typing import Optional

def setup_logging(log_file: str = 'translation_log.txt') -> logging.Logger:
    """Configure le système de logging avec sortie fichier et console."""
    logger = logging.getLogger('T2L')
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # Handler fichier
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)

    # Handler console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # Ajout des handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

def log_execution_time(start_time: datetime, action_name: str) -> None:
    """Log le temps d'exécution d'une action."""
    duration = datetime.now() - start_time
    logging.info(f"{action_name} terminé en {duration.total_seconds():.2f} secondes")