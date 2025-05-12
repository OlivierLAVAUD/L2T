
import torch
from app.translator import NLLBTranslator
    
torch.cuda.empty_cache()
translator = NLLBTranslator()
text = "Hello world"
    
print("=== Test Device Sync ===")
print(f"GPU available: {torch.cuda.is_available()}")
    
result = translator.translate(text, "fra_Latn")
print(f"Résultat: {result}")
print(f"Device final: {next(translator.model.parameters()).device}")