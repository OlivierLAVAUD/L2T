"""
Package principal de l'application L2T (Language 2 Translate)

Ce module initialise les composants principaux et expose l'API publique.
"""

__version__ = "2.1.0"
__author__ = "Olivier Lavaud"
__license__ = "MIT"

# Import des composants principaux
from app.core.translator import NLLBTranslator
from app.interfaces.cli import CLICommand
from app.interfaces.main import L2TApplication

# API publique
__all__ = [
    'NLLBTranslator',
    'CLICommand',
    'L2TApplication',
    'configure',
    'get_version'
]

# Configuration initiale
def configure(debug: bool = False):
    """
    Configure l'application globalement
    
    Args:
        debug (bool): Active le mode debug (False par défaut)
    """
    from app.config import settings
    settings.debug = debug

def get_version() -> str:
    """
    Retourne la version actuelle du package
    
    Returns:
        str: Version sous forme 'X.Y.Z'
    """
    return __version__

# Initialisation au chargement du module
from app.utils.logger import setup_logging
setup_logging()

# Vérification de la configuration GPU
try:
    from app.infrastructure.gpu import GPUManager
    if GPUManager().get_available_devices():
        print(f"L2T {__version__} - GPU support enabled")
    else:
        print(f"L2T {__version__} - Running in CPU mode")
except ImportError:
    print(f"L2T {__version__} - GPU dependencies not installed")