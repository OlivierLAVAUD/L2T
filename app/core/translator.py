import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, logging
from functools import lru_cache
from typing import Dict, Optional, List
from app.config import settings
from app.core.models import TranslationInput, TranslationResult
import time
import warnings
import importlib.metadata  # Import manquant ajouté

logging.set_verbosity_error()
warnings.filterwarnings("ignore", category=UserWarning)

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
        """Initialisation matérielle avec vérification approfondie"""
        self.use_gpu = False
        
        if settings.use_gpu:
            try:
                if torch.cuda.is_available():
                    current_device = torch.cuda.current_device()
                    self.device = torch.device(f"cuda:{current_device}")
                    
                    # Test complet du device
                    test_tensor = torch.tensor([1.0], device=self.device)
                    assert str(test_tensor.device).startswith("cuda:")
                    
                    self.use_gpu = True
                    print(f"GPU initialized: {torch.cuda.get_device_name(current_device)}")
                    print(f"PyTorch CUDA version: {torch.version.cuda}")
                    print(f"GPU Memory: {torch.cuda.get_device_properties(current_device).total_memory/1024**3:.2f} GB")
                else:
                    print("CUDA not available despite settings.use_gpu=True")
                    self.device = torch.device("cpu")
            except Exception as e:
                print(f"GPU initialization failed, falling back to CPU: {str(e)}")
                self.device = torch.device("cpu")
        else:
            self.device = torch.device("cpu")
        
        print(f"Final initialized device: {str(self.device)}")

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

        print(f"\n=== Loading model on {str(self.device)} ===")
        print(f"PyTorch version: {torch.__version__}")
        print(f"Transformers version: {importlib.metadata.version('transformers')}")

        try:
            # Configuration spéciale pour éviter les problèmes de device
            kwargs = {
                "cache_dir": str(settings.cache_dir),
                "torch_dtype": torch.float32,
                "device_map": None  # Désactive le device_map automatique
            }

            # Chargement de base sur CPU puis déplacement contrôlé
            self.model = AutoModelForSeq2SeqLM.from_pretrained(
                settings.model_name,
                **kwargs
            ).to(self.device)  # Déplacement explicite

            # Nettoyage mémoire et configuration GPU
            if self.use_gpu:
                torch.cuda.empty_cache()
                self.model.config.use_cache = False  # Désactive le cache pour économiser de la mémoire

            # Charge le tokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(
                settings.model_name,
                cache_dir=str(settings.cache_dir),
                use_fast=True
            )

            # Vérification finale
            model_device = next(self.model.parameters()).device
            print(f"Model successfully loaded on device: {model_device}")

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

            # Préparation des entrées avec conversion device ultra-contrôlée
            inputs = self.tokenizer(
                input.text,
                return_tensors="pt",
                truncation=True,
                max_length=settings.max_length
            )
            
            # Conversion device avec vérification
            inputs = {k: v.to(self.device) for k, v in inputs.items()}

            # Vérification finale du device modèle
            if next(self.model.parameters()).device != self.device:
                self.model = self.model.to(self.device)

            # Génération avec gestion d'erreur améliorée
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    forced_bos_token_id=self.tokenizer.convert_tokens_to_ids([input.target_lang]),
                    max_length=settings.max_length,
                    num_beams=2
                )
            
            # Décodage avec gestion device explicite
            translated_text = self.tokenizer.decode(outputs[0].cpu(), skip_special_tokens=True)
            
            return TranslationResult(
                original=input.text,
                translated_text=translated_text,
                source_lang=input.source_lang,
                target_lang=input.target_lang,
                processing_time=time.time() - start_time
            )

        except torch.cuda.OutOfMemoryError:
            print("CUDA out of memory - Try reducing max_length or using CPU")
            raise
        except Exception as e:
            print(f"Translation failed: {str(e)}")
            raise

    def translate_batch(self, inputs: List[TranslationInput]) -> List[TranslationResult]:
        return [self.translate(input) for input in inputs]


# Patch global pour les devices (optionnel)
if torch.cuda.is_available():
    import torch.nn as nn
    original_to = nn.Module.to
    def patched_to(self, *args, **kwargs):
        if len(args) > 0 and isinstance(args[0], str) and args[0] == "cuda":
            args = (f"cuda:{torch.cuda.current_device()}",) + args[1:]
        return original_to(self, *args, **kwargs)
    nn.Module.to = patched_to