import torch
from torch.utils.data import Dataset, DataLoader

class TranslationDataset(Dataset):
    """Dataset optimisé pour le chargement"""
    def __init__(self, texts):
        self.texts = texts
        
    def __len__(self):
        return len(self.texts)
        
    def __getitem__(self, idx):
        return self.texts[idx]

def configure_environment():
    torch.backends.cudnn.benchmark = False  # Désactivé pour la stabilité
    torch.set_float32_matmul_precision('medium')  # Équilibre précision/performance
    
    if torch.cuda.is_available():
        # Nettoyage approfondi
        torch.cuda.synchronize()
        torch.cuda.empty_cache()
        # Limite l'utilisation mémoire
        torch.cuda.set_per_process_memory_fraction(0.8)