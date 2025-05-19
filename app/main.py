
from app.cli import NLLBTranslationCLI
from .optimizations import configure_environment

import os, sys, io

from dotenv import load_dotenv
from pathlib import Path
import logging

def load_and_verify_env():
    """Charge et vérifie les variables d'environnement"""
    env_path = Path(__file__).parent / '.env'
    loaded = load_dotenv(env_path)
    
    if not loaded:
        logging.warning("Aucun fichier .env trouvé, utilisation des valeurs par défaut")
    
    # Liste des variables critiques à vérifier
    required_vars = {
        'MODEL_NAME': 'facebook/nllb-200-distilled-600M',
        'BATCH_SIZE': 8,
        'MAX_LENGTH': 512,
        'USE_GPU': True
    }
    
    # Configuration du logger
    logging.basicConfig(level=os.getenv('LOG_LEVEL', 'INFO'))
    logger = logging.getLogger('ENV_LOADER')
    
    # Affichage des valeurs
    logger.info("=== Configuration Chargée ===")
    for var, default in required_vars.items():
        value = os.getenv(var, str(default))
        logger.info(f"{var.ljust(20)} = {value}")
    
    # Validation des types
    try:
        batch_size = int(os.getenv('BATCH_SIZE', 8))
        max_length = int(os.getenv('MAX_LENGTH', 512))
        use_gpu = os.getenv('USE_GPU', 'True').lower() in ('true', '1', 't')
    except ValueError as e:
        logger.error(f"Erreur de type dans les variables: {str(e)}")

def main():

    sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
    

    load_and_verify_env()

    """Point d'entrée avec optimisations"""
    configure_environment()
    try:
        cli = NLLBTranslationCLI()
        cli.run()
    except KeyboardInterrupt:
        print("\nTraduction interrompue")
        sys.exit(0)
    except Exception as e:
        print(f"Erreur: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()