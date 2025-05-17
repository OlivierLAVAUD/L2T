import subprocess
import torch

def fix_gpu():
    print("=== Diagnostic GPU ===")
    
    # 1. Vérification des drivers NVIDIA
    try:
        smi = subprocess.check_output('nvidia-smi').decode()
        print("[OK] Drivers NVIDIA installés")
        print(smi.split('\n')[0])  # Affiche la version du driver
    except:
        print("[ERREUR] Drivers NVIDIA non installés")
        return False

    # 2. Vérification CUDA toolkit
    try:
        cuda = subprocess.check_output('nvcc --version').decode()
        print("[OK] CUDA Toolkit installé")
        print(cuda.split('\n')[3])  # Affiche la version CUDA
    except:
        print("[ERREUR] CUDA Toolkit non installé")
        return False

    # 3. Vérification PyTorch
    print(f"\nPyTorch version: {torch.__version__}")
    print(f"CUDA disponible: {torch.cuda.is_available()}")
    
    if torch.cuda.is_available():
        print(f"GPU: {torch.cuda.get_device_name(0)}")
        return True
    else:
        print("[ERREUR] PyTorch ne détecte pas CUDA")
        print("Solution possible: réinstaller PyTorch avec:")
        print("pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118")
        return False

if __name__ == "__main__":
    if fix_gpu():
        print("\n=> Le GPU est prêt à être utilisé")
    else:
        print("\n=> Problème de configuration GPU détecté")