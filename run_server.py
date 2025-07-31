#!/usr/bin/env python3
"""
BeQuickChat Sunucu Başlatma Scripti

Bu script, BeQuickChat sunucusunu başlatmak için kullanılır.
"""

import sys
import os

# src klasörünü Python path'ine ekle
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from server import main

if __name__ == "__main__":
    print("BeQuickChat Sunucusu Başlatılıyor...")
    print("Sunucu: 0.0.0.0:8000")
    print("Çıkmak için Ctrl+C tuşlayın")
    print("-" * 40)
    
    try:
        main()
    except KeyboardInterrupt:
        print("\nSunucu kapatılıyor...")
    except Exception as e:
        print(f"Hata: {e}")
        sys.exit(1) 