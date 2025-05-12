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
    """Configure l'environnement pour performance maximale"""
    torch.backends.cudnn.benchmark = True
    torch.set_float32_matmul_precision('high')
    
    if torch.cuda.is_available():
        torch.cuda.empty_cache()