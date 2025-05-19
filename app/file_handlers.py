import PyPDF2
from pathlib import Path
from typing import Optional, Union
import logging
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

class FileHandler:
    """Gestionnaire de fichiers pour la lecture/écriture de différents formats."""

    @staticmethod
    def read_file(file_path: Union[str, Path], encoding: str = 'utf-8') -> Optional[str]:
        """Lecture avec gestion robuste des encodages"""
        try:
            with open(file_path, 'rb') as f:
                raw_data = f.read()
                for enc in ['utf-8', 'iso-8859-1', 'cp1252']:  # Essai des encodages courants
                    try:
                        return raw_data.decode(enc)
                    except UnicodeDecodeError:
                        continue
                raise ValueError(f"Encodage non reconnu pour {file_path}")
        except Exception as e:
            logging.error(f"Erreur lors de la lecture du fichier {file_path}: {str(e)}")
            return None

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
    def write_output(content: str, output_path: Path, encoding: str = 'utf-8') -> None:
        """Écriture sécurisée avec vérification d'intégrité"""
        try:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w', encoding=encoding) as f:
                # Vérification proactive des marqueurs
            #    content = content.replace("CONTECT", "CONTEXT")
                f.write(content)
            # Validation a posteriori
            with open(output_path, 'r', encoding=encoding) as f:
                if "CONTECT" in f.read():
                    raise IOError("Échec de correction des marqueurs")
        except Exception as e:
            raise IOError(f"Erreur d'écriture validée : {str(e)}")