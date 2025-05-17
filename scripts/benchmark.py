#!/usr/bin/env python3
import time
from app.core.translator import NLLBTranslator
from app.infrastructure.gpu import GPUManager
from app.utils.logger import setup_logging

logger = setup_logging()

def run_benchmark():
    translator = NLLBTranslator()
    test_text = "This is a benchmark test " * 50  # 500 mots
    
    with GPUManager():
        # Test GPU
        start = time.time()
        result = translator.translate(test_text, "fra_Latn")
        gpu_time = time.time() - start
        
        # Test CPU
        translator.device = "cpu"
        start = time.time()
        result = translator.translate(test_text, "fra_Latn")
        cpu_time = time.time() - start
    
    logger.info(f"Résultats du benchmark:")
    logger.info(f"GPU: {gpu_time:.2f}s")
    logger.info(f"CPU: {cpu_time:.2f}s")
    logger.info(f"Ratio: {cpu_time/gpu_time:.1f}x plus rapide")

if __name__ == "__main__":
    run_benchmark()