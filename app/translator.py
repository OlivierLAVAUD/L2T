from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, pipeline
import torch
import os
import json
from dotenv import load_dotenv

load_dotenv()  # Charge les variables d'environnement depuis le fichier .env

class NLLBTranslationService:
    """
    Service de traduction utilisant le modèle NLLB (No Language Left Behind) de Facebook/Meta.
    Gère le chargement du modèle, la traduction et la gestion des langues supportées.
    """
    
    def __init__(self):
        """Initialise le service de traduction."""
        self.translation_model = None
        self.tokenizer = None
        self._is_model_loaded = False
        self.translation_pipeline = None
        self.supported_languages = self._load_language_support_config()
    
    def _load_language_support_config(self) -> dict:
        """
        Charge la configuration des langues supportées depuis un fichier JSON.
        
        Returns:
            dict: Dictionnaire des langues supportées
            
        Raises:
            RuntimeError: Si le chargement du fichier échoue
        """
        config_path = os.getenv('SUPPORTED_LANGUAGES_FILE', 'app/supported_languages.json')
        try:
            with open(config_path, 'r', encoding='utf-8') as config_file:
                return json.load(config_file)
        except Exception as error:
            raise RuntimeError(f"Erreur lors du chargement des langues supportées: {str(error)}")

    def initialize_translation_model(self):
        """
        Charge et configure le modèle de traduction avec des optimisations de performance.
        
        Raises:
            RuntimeError: Si le chargement du modèle échoue
        """
        if self._is_model_loaded:
            return

        try:
            # Configuration pour performance optimale
            precision = torch.float16 if torch.cuda.is_available() else torch.float32
            model_name = os.getenv('MODEL_NAME', "facebook/nllb-200-distilled-600M")

            # Chargement du modèle
            self.translation_model = AutoModelForSeq2SeqLM.from_pretrained(
                model_name,
                device_map="auto",
                torch_dtype=precision
            )

            # Chargement du tokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(
                model_name,
                use_fast=True  # Tokenizer rapide
            )

            # Configuration du pipeline de traduction
            self.translation_pipeline = pipeline(
                "translation",
                model=self.translation_model,
                tokenizer=self.tokenizer,
                truncation=True,
                max_length=int(os.getenv('MAX_LENGTH', 512))
            )

            self._is_model_loaded = True
            
        except Exception as error:
            raise RuntimeError(f"Erreur lors du chargement du modèle: {str(error)}")

    def batch_translate_texts(self, texts: list[str], target_language: str, source_language: str = None) -> list[str]:
        """
        Traduit une liste de textes en batch pour une meilleure performance.
        
        Args:
            texts: Liste des textes à traduire
            target_language: Code langue cible
            source_language: Code langue source (optionnel)
            
        Returns:
            Liste des textes traduits
            
        Raises:
            RuntimeError: Si la traduction échoue
        """
        if not self._is_model_loaded:
            self.initialize_translation_model()

        try:
            # Préfixe de langue pour NLLB
            source_prefix = f"{source_language}>" if source_language else ""

            translations = self.translation_pipeline(
                texts,
                src_lang=source_prefix,
                tgt_lang=target_language,
                batch_size=int(os.getenv('BATCH_SIZE', 8)),
                num_beams=int(os.getenv('NUM_BEAMS', 2)),
                early_stopping=True
            )
            
            return [result['translation_text'] for result in translations]
            
        except Exception as error:
            raise RuntimeError(f"Erreur de traduction: {str(error)}")

    def get_supported_languages(self) -> dict:
        """Retourne la liste des langues supportées avec leurs codes."""
        return self.supported_languages

    def is_language_supported(self, language_code: str) -> bool:
        """Vérifie si une langue est supportée par le service."""
        return language_code in self.supported_languages

    def translate_text(self, text: str, target_language: str, source_language: str = None) -> str:
        """
        Traduit un texte unique avec gestion explicite du device (GPU/CPU).
        
        Args:
            text: Texte à traduire
            target_language: Code langue cible
            source_language: Code langue source (optionnel)
            
        Returns:
            Texte traduit
            
        Raises:
            RuntimeError: Si la traduction échoue
        """
        if not self._is_model_loaded:
            self.initialize_translation_model()

        try:
            # Sélection du device (GPU si disponible)
            device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            self.translation_model.to(device)

            if source_language:
                self.tokenizer.src_lang = source_language

            # Tokenization sur le bon device
            input_tokens = self.tokenizer(
                text,
                return_tensors="pt",
                truncation=True,
                max_length=int(os.getenv('MAX_LENGTH', 1024))
            ).to(device)

            # Génération de la traduction
            translated_tokens = self.translation_model.generate(
                **input_tokens,
                forced_bos_token_id=self.tokenizer.convert_tokens_to_ids([target_language]),
                max_length=int(os.getenv('MAX_LENGTH', 1024))
            )

            return self.tokenizer.decode(translated_tokens[0], skip_special_tokens=True)

        except Exception as error:
            raise RuntimeError(f"Erreur de traduction: {str(error)}")