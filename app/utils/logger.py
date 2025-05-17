import logging
from pathlib import Path
from app.config import settings

def setup_logging() -> logging.Logger:
    """Configure le système de logging avec gestion des erreurs de fichiers"""
    
    logger = logging.getLogger("L2T")
    logger.setLevel(logging.DEBUG if settings.debug else logging.INFO)

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    if logger.hasHandlers():
            return logger  # évite de dupliquer les handlers

    # Handler console (toujours actif)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Handler fichier (avec gestion d'erreur)
    try:
        log_file = settings.log_path / settings.log_file
        log_file.parent.mkdir(parents=True, exist_ok=True)

        file_handler = logging.FileHandler(
            filename=log_file,
            encoding=settings.encoding,
            mode='a'  # Mode append
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    except PermissionError:
        logger.warning(
            f"Impossible d'écrire dans {log_file}, "
            "seul le logging console sera disponible"
        )
    except Exception as e:
        logger.error(f"Erreur configuration fichier de log: {str(e)}")

    return logger

def log_execution_time(func):
    """Décorateur pour logger le temps d'exécution"""
    def wrapper(*args, **kwargs):
        import time
        start = time.time()
        result = func(*args, **kwargs)
        duration = time.time() - start
        logging.getLogger("L2T.timer").info(
            f"'{func.__name__}' exécuté en {duration:.2f}s"
        )
        return result
    return wrapper