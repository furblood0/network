#!/usr/bin/env python3
"""
BeQuickChat İstemci Başlatma Scripti

Bu script, BeQuickChat istemcisini başlatmak için kullanılır.
"""

import sys
import os

# src klasörünü Python path'ine ekle
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from client import main

if __name__ == "__main__":
    print("BeQuickChat İstemcisi Başlatılıyor...")
    print("Varsayılan sunucu: 127.0.0.1:8000")
    print("-" * 40)
    
    try:
        main()
    except KeyboardInterrupt:
        print("\nİstemci kapatılıyor...")
    except Exception as e:
        print(f"Hata: {e}")
        sys.exit(1) 