import aiofiles
import PyPDF2
from pathlib import Path
from typing import Union, Optional
from app.config import settings
import logging

logger = logging.getLogger(__name__)

class FileHandler:
    @staticmethod
    async def async_read(file_path: Path) -> str:
        """Lecture asynchrone optimisée"""
        try:
            if file_path.suffix.lower() == ".pdf":
                return await FileHandler._async_read_pdf(file_path)
            
            async with aiofiles.open(file_path, "r", encoding=settings.encoding) as f:
                return await f.read()
                
        except Exception as e:
            logger.error(f"Erreur lecture async: {file_path}: {str(e)}")
            raise

    @staticmethod
    def sync_read(file_path: Path) -> str:
        """Lecture synchrone standard"""
        try:
            if file_path.suffix.lower() == ".pdf":
                return FileHandler._sync_read_pdf(file_path)
                
            with open(file_path, "r", encoding=settings.encoding) as f:
                return f.read()
                
        except Exception as e:
            logger.error(f"Erreur lecture sync: {file_path}: {str(e)}")
            raise

    @staticmethod
    async def _async_read_pdf(pdf_path: Path) -> str:
        async with aiofiles.open(pdf_path, "rb") as f:
            reader = PyPDF2.PdfReader(await f.read())
            return "\n".join(page.extract_text() or "" for page in reader.pages)

    @staticmethod
    def _sync_read_pdf(pdf_path: Path) -> str:
        with open(pdf_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            return "\n".join(page.extract_text() or "" for page in reader.pages)

    @staticmethod
    def write(content: str, output_path: Path) -> None:
        """Écriture synchrone avec création de répertoire"""
        try:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, "w", encoding=settings.encoding) as f:
                f.write(content)
        except Exception as e:
            logger.error(f"Erreur écriture: {output_path}: {str(e)}")
            raise