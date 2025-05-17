import torch
print(f"Version: {torch.__version__}")  # Doit afficher "2.x.0+cu118"
print(f"GPU disponible: {torch.cuda.is_available()}")  # Doit être True