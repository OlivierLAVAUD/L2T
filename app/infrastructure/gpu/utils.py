import torch
from pynvml import nvmlInit, nvmlDeviceGetHandleByIndex, nvmlDeviceGetMemoryInfo
from typing import Dict, Optional

def get_gpu_info(device_id: int = 0) -> Optional[Dict]:
    """Récupère les informations détaillées du GPU"""
    try:
        nvmlInit()
        handle = nvmlDeviceGetHandleByIndex(device_id)
        mem = nvmlDeviceGetMemoryInfo(handle)
        
        return {
            'name': torch.cuda.get_device_name(device_id),
            'total_memory': mem.total / 1024**2,
            'free_memory': mem.free / 1024**2,
            'used_memory': mem.used / 1024**2,
            'driver_version': torch.cuda.get_driver_version(),
            'cuda_version': torch.version.cuda
        }
    except:
        return None

def set_device_priority(device_id: int = 0):
    """Définit la priorité du device GPU"""
    if torch.cuda.is_available():
        torch.cuda.set_device(device_id)
        torch.cuda.empty_cache()