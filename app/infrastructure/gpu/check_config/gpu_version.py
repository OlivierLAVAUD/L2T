import torch, subprocess, sys

def get_versions():
    print("=== Versions log ===")
    
    # 1. System info
    print(f"\nSystème: {sys.platform}")
    
    # 2. GPU info
    try:
        smi = subprocess.check_output(['nvidia-smi']).decode()
        driver_line = [l for l in smi.split('\n') if 'Driver Version' in l][0]
        print(f"\nGPU Info:\n{driver_line}")
    except:
        print("\nAucune information GPU trouvée (nvidia-smi non disponible)")

    # 3. CUDA info
    try:
        cuda = subprocess.check_output(['nvcc', '--version']).decode()
        print(f"\nCUDA Compiler:\n{cuda.split('release ')[1].split(',')[0]}")
    except:
        print("\nCUDA Toolkit non détecté")

    # 4. PyTorch info
    print("\nPyTorch:")
    print(f"Version: {torch.__version__}")
    print(f"CUDA disponible: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"Version CUDA de PyTorch: {torch.version.cuda}")
        print(f"GPU: {torch.cuda.get_device_name(0)}")
    else:
        print("Aucun GPU détecté par PyTorch")

    # 5. Librairies complémentaires
    try:
        import transformers
        print(f"\nTransformers: {transformers.__version__}")
    except:
        pass

if __name__ == "__main__":
    get_versions()