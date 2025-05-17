from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from pathlib import Path
from datetime import datetime

class LanguageCode(str, Enum):
    """
    Codes de langue standardisés selon la norme NLLB.
    Format: code_SCRIPT (ex: fra_Latn, ara_Arab)
    """
    ENGLISH = "eng_Latn"
    FRENCH = "fra_Latn"
    SPANISH = "spa_Latn"
    GERMAN = "deu_Latn"
    ITALIAN = "ita_Latn"
    CHINESE_SIMP = "zho_Hans"
    CHINESE_TRAD = "zho_Hant"
    JAPANESE = "jpn_Jpan"
    RUSSIAN = "rus_Cyrl"
    PORTUGUESE = "por_Latn"

class TranslationInput(BaseModel):
    """
    Modèle pour les données d'entrée de traduction
    """
    text: str = Field(..., min_length=1, description="Texte à traduire")
    target_lang: LanguageCode = Field(..., description="Langue cible")
    source_lang: Optional[LanguageCode] = Field(
        None, 
        description="Langue source (détection automatique si omis)"
    )
    chunk_size: Optional[int] = Field(
        None,
        ge=100,
        le=1000,
        description="Taille des segments pour le découpage"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "text": "Hello world",
                "target_lang": "fra_Latn",
                "source_lang": "eng_Latn",
                "chunk_size": 500
            }
        }

class TranslationResult(BaseModel):
    """
    Modèle pour les résultats de traduction
    """
    original: str = Field(..., description="Texte original")
    translated_text: str = Field(..., description="Texte traduit")
    source_lang: Optional[LanguageCode] = Field(None, description="Langue source détectée")
    target_lang: LanguageCode = Field(..., description="Langue cible")
    processing_time: float = Field(
        ...,
        ge=0,
        description="Temps de traitement en secondes"
    )
    confidence: Optional[float] = Field(
        None,
        ge=0,
        le=1,
        description="Confiance de la traduction (0-1)"
    )
    model: str = Field(
        "facebook/nllb-200-distilled-600M",
        description="Modèle utilisé"
    )

class FileMetadata(BaseModel):
    """
    Métadonnées pour les fichiers traités
    """
    path: Path = Field(..., description="Chemin du fichier")
    size: int = Field(..., ge=0, description="Taille en octets")
    encoding: str = Field("utf-8", description="Encodage du fichier")
    detected_lang: Optional[LanguageCode] = Field(
        None,
        description="Langue détectée dans le fichier"
    )
    last_modified: Optional[datetime] = Field(
        None,
        description="Date de dernière modification"
    )

class BatchTranslationRequest(BaseModel):
    """
    Modèle pour les requêtes de traduction par lots
    """
    inputs: List[TranslationInput] = Field(
        ...,
        min_items=1,
        max_items=100,
        description="Liste des textes à traduire"
    )
    batch_size: int = Field(
        8,
        ge=1,
        le=32,
        description="Taille des lots pour le traitement"
    )

class SupportedLanguagesResponse(BaseModel):
    """
    Modèle pour la réponse des langues supportées
    """
    languages: Dict[str, str] = Field(
        ...,
        description="Dictionnaire des langues supportées (code: nom)"
    )
    count: int = Field(
        ...,
        description="Nombre total de langues supportées"
    )
    default_target: LanguageCode = Field(
        ...,
        description="Langue cible par défaut"
    )