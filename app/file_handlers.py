import PyPDF2
from pathlib import Path
from typing import Optional, Union
import logging

class FileHandler:
    """Gestionnaire de fichiers pour la lecture/écriture de différents formats."""

    @staticmethod
    def read_file(file_path: Union[str, Path], encoding: str = 'utf-8') -> Optional[str]:
        """Lit un fichier texte ou PDF."""
        path = Path(file_path)
        try:
            if path.suffix.lower() == '.pdf':
                return FileHandler._read_pdf(path)
            return FileHandler._read_text_file(path, encoding)
        except Exception as e:
            logging.error(f"Erreur lecture fichier {path}: {str(e)}")
            raise

    @staticmethod
    def _read_pdf(pdf_path: Path) -> str:
        """Extrait le texte d'un fichier PDF."""
        text = []
        try:
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                for page in reader.pages:
                    text.append(page.extract_text() or "")
            return '\n'.join(text)
        except Exception as e:
            raise IOError(f"Erreur PDF: {str(e)}")

    @staticmethod
    def _read_text_file(file_path: Path, encoding: str) -> str:
        """Lit un fichier texte avec l'encodage spécifié."""
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                return f.read()
        except UnicodeDecodeError:
            raise ValueError(f"Erreur d'encodage (essayez avec --encoding)")
        except Exception as e:
            raise IOError(f"Erreur lecture fichier: {str(e)}")

    @staticmethod
    def write_output(content: str, output_path: Union[str, Path], encoding: str = 'utf-8') -> None:
        """Écrit le contenu dans un fichier."""
        path = Path(output_path)
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            with open(path, 'w', encoding=encoding) as f:
                f.write(content)
        except Exception as e:
            raise IOError(f"Erreur écriture fichier {path}: {str(e)}")