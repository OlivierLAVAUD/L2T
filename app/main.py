import sys
from app.cli import NLLBTranslationCLI
from .optimizations import configure_environment

def main():
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