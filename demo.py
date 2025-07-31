#!/usr/bin/env python3
"""
BeQuickChat Demo Scripti

Bu script, BeQuickChat uygulamasının özelliklerini demo etmek için kullanılır.
"""

import sys
import os
import subprocess
import time
import threading

def print_banner():
    """Proje banner'ını yazdır."""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                    BeQuickChat Demo                          ║
    ║              UDP Tabanlı Çok Kullanıcılı Sohbet              ║
    ║                                                              ║
    ║  Geliştiriciler:                                             ║
    ║  - Beyza Nur Selvi (222010020057)                           ║
    ║  - Furkan Fidan (212010020002)                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def check_dependencies():
    """Gerekli bağımlılıkları kontrol et."""
    print("🔍 Bağımlılıklar kontrol ediliyor...")
    
    try:
        import PyQt5
        print("✅ PyQt5 yüklü")
    except ImportError:
        print("❌ PyQt5 yüklü değil. Lütfen 'pip install PyQt5' komutunu çalıştırın.")
        return False
    
    try:
        import matplotlib
        print("✅ matplotlib yüklü")
    except ImportError:
        print("❌ matplotlib yüklü değil. Lütfen 'pip install matplotlib' komutunu çalıştırın.")
        return False
    
    try:
        from Crypto.Cipher import AES
        print("✅ pycryptodome yüklü")
    except ImportError:
        print("❌ pycryptodome yüklü değil. Lütfen 'pip install pycryptodome' komutunu çalıştırın.")
        return False
    
    return True

def run_tests():
    """Testleri çalıştır."""
    print("\n🧪 Testler çalıştırılıyor...")
    
    test_files = [
        "tests/test_functional.py",
        "tests/test_full.py",
        "tests/test_performance.py"
    ]
    
    for test_file in test_files:
        if os.path.exists(test_file):
            print(f"📋 {test_file} çalıştırılıyor...")
            try:
                result = subprocess.run([sys.executable, test_file], 
                                      capture_output=True, text=True, timeout=30)
                if result.returncode == 0:
                    print(f"✅ {test_file} başarıyla tamamlandı")
                else:
                    print(f"❌ {test_file} başarısız: {result.stderr}")
            except subprocess.TimeoutExpired:
                print(f"⏰ {test_file} zaman aşımına uğradı")
            except Exception as e:
                print(f"❌ {test_file} hatası: {e}")
        else:
            print(f"⚠️ {test_file} bulunamadı")

def show_features():
    """Özellikleri listele."""
    print("\n🌟 BeQuickChat Özellikleri:")
    features = [
        "✅ Çok kullanıcılı sohbet (genel ve özel)",
        "✅ Güvenilir UDP mesajlaşma (ACK ve yeniden iletim)",
        "✅ Gerçek zamanlı kullanıcı listesi",
        "✅ Sistem mesajları (katılma/ayrılma bildirimleri)",
        "✅ Modern GUI (sohbet baloncukları, kullanıcı listesi)",
        "✅ Çapraz platform desteği (Windows/Linux)",
        "✅ Uçtan uca şifreleme (AES)",
        "✅ Özel mesajlaşma (çift tıklama ile)",
        "✅ Duplicate mesaj önleme",
        "✅ Responsive tasarım"
    ]
    
    for feature in features:
        print(f"  {feature}")

def show_usage():
    """Kullanım talimatlarını göster."""
    print("\n💻 Kullanım Talimatları:")
    print("1. Sunucuyu başlatın:")
    print("   python run_server.py")
    print("   veya")
    print("   python src/server.py")
    print()
    print("2. İstemciyi başlatın:")
    print("   python run_client.py")
    print("   veya")
    print("   python src/client.py")
    print()
    print("3. Kullanıcı adınızı ve sunucu adresini girin")
    print("4. Sohbete başlayın!")
    print()
    print("📝 Özel mesaj için: Kullanıcı listesinden birine çift tıklayın")

def main():
    """Ana demo fonksiyonu."""
    print_banner()
    
    if not check_dependencies():
        print("\n❌ Gerekli bağımlılıklar eksik. Lütfen requirements.txt dosyasındaki")
        print("   paketleri yükleyin: pip install -r requirements.txt")
        return
    
    show_features()
    show_usage()
    
    # Testleri çalıştır
    run_tests()
    
    print("\n🎉 Demo tamamlandı!")
    print("BeQuickChat'i kullanmaya başlamak için yukarıdaki talimatları takip edin.")

if __name__ == "__main__":
    main() 