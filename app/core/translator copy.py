import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, logging
from functools import lru_cache
from typing import Dict, Optional, List
from app.config import settings
from app.core.models import TranslationInput, TranslationResult
import time

logging.set_verbosity_error()

class NLLBTranslator:
    _instance: Optional['NLLBTranslator'] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        self._init_hardware()
        self.model = None
        self.tokenizer = None
        self._load_model()

    def _init_hardware(self):
        """Initialisation matérielle avec gestion forcée du CPU si demandé"""
        self.use_gpu = settings.use_gpu and torch.cuda.is_available()
        if not settings.use_gpu:  # Force CPU si USE_GPU=False dans .env
            self.use_gpu = False
            torch.cuda.is_available = lambda: False  # Patch pour forcer CPU
        
        self.device = torch.device("cuda:0" if self.use_gpu else "cpu")
        print(f"Initialized device: {self.device} (USE_GPU={settings.use_gpu})")

    @lru_cache(maxsize=1)
    def get_supported_languages(self) -> Dict[str, str]:
        return {
            'eng_Latn': 'English',
            'fra_Latn': 'French',
            # ... (autres langues)
        }

    def _load_model(self):
        if self.model is not None:
            return

        print(f"Loading model on {self.device}")

        # Configuration commune
        kwargs = {
            "cache_dir": str(settings.cache_dir),
            "torch_dtype": torch.float32  # Toujours float32 pour stabilité
        }

        try:
            # Chargement différencié CPU/GPU
            if self.use_gpu:
                self.model = AutoModelForSeq2SeqLM.from_pretrained(
                    settings.model_name,
                    device_map="auto",
                    **kwargs
                )
            else:
                self.model = AutoModelForSeq2SeqLM.from_pretrained(
                    settings.model_name,
                    low_cpu_mem_usage=True,
                    **kwargs
                ).to(self.device)

            self.tokenizer = AutoTokenizer.from_pretrained(
                settings.model_name,
                cache_dir=str(settings.cache_dir),
                use_fast=True
            )

            print(f"Model successfully loaded on {self.device}")

        except Exception as e:
            print(f"Model loading failed: {str(e)}")
            raise

    def translate(self, input: TranslationInput) -> TranslationResult:
        if not input.text.strip():
            return TranslationResult(
                original=input.text,
                translated_text=input.text,
                source_lang=input.source_lang,
                target_lang=input.target_lang,
                processing_time=0.0
            )

        start_time = time.time()

        try:
            # Configuration de la langue source
            if input.source_lang:
                self.tokenizer.src_lang = input.source_lang

            # Préparation des entrées avec vérification du device
            inputs = self.tokenizer(
                input.text,
                return_tensors="pt",
                truncation=True,
                max_length=settings.max_length
            ).to(self.device)

            # Génération de la traduction
            outputs = self.model.generate(
                **inputs,
                forced_bos_token_id=self.tokenizer.convert_tokens_to_ids([input.target_lang]),
                max_length=settings.max_length,
                num_beams=2
            )

            # Décodage du résultat
            translated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            return TranslationResult(
                original=input.text,
                translated_text=translated_text,
                source_lang=input.source_lang,
                target_lang=input.target_lang,
                processing_time=time.time() - start_time
            )

        except Exception as e:
            print(f"Translation failed: {str(e)}")
            raise

    def translate_batch(self, inputs: List[TranslationInput]) -> List[TranslationResult]:
        return [self.translate(input) for input in inputs]