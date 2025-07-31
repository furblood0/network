# BeQuickChat - UDP Tabanlı Çok Kullanıcılı Sohbet Uygulaması

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![PyQt5](https://img.shields.io/badge/PyQt5-5.15+-green.svg)](https://pypi.org/project/PyQt5/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

BeQuickChat, Python ve PyQt5 kullanılarak geliştirilmiş modern, çok kullanıcılı bir sohbet uygulamasıdır. UDP soketleri ve özel protokol kullanarak güvenilir mesajlaşma sağlar.

## 🌟 Özellikler

- **Çok Kullanıcılı Sohbet:** Genel ve özel mesajlaşma
- **Güvenilir UDP Mesajlaşma:** ACK ve yeniden iletim mekanizması
- **Gerçek Zamanlı Kullanıcı Listesi:** Bağlı kullanıcıları anlık görüntüleme
- **Sistem Mesajları:** Katılma/ayrılma bildirimleri
- **Modern GUI:** Sohbet baloncukları, kullanıcı listesi, özel pencere ikonu
- **Çapraz Platform Desteği:** Windows ve Linux'ta çalışır
- **Uçtan Uca Şifreleme:** AES ile tüm mesajlar şifrelenir
- **Özel Mesajlaşma:** Kullanıcıya çift tıklayarak özel sohbet sekmesi açma

## 📋 Gereksinimler

- Python 3.8+
- PyQt5 >= 5.15.0
- matplotlib >= 3.5.0 (performans testleri için)
- pycryptodome (şifreleme için)

## 🚀 Kurulum

### 1. Projeyi klonlayın
```bash
git clone https://github.com/yourusername/bequickchat.git
cd bequickchat
```

### 2. Bağımlılıkları yükleyin
```bash
pip install -r requirements.txt
```

## 💻 Kullanım

### Sunucuyu Başlatın
```bash
python src/server.py
```

### İstemciyi Başlatın
```bash
python src/client.py
```

1. Kullanıcı adınızı ve sunucu adresini girin (varsayılan: 127.0.0.1:8000)
2. Genel sohbette mesajlaşmaya başlayın
3. Özel mesaj için kullanıcı listesinden birine çift tıklayın

## 📁 Proje Yapısı

```
bequickchat/
├── src/
│   ├── client.py          # PyQt5 GUI istemcisi
│   ├── server.py          # UDP sunucu
│   └── protocol.py        # Mesaj protokolü ve şifreleme
├── tests/
│   ├── test_functional.py # Temel işlevsellik testleri
│   ├── test_full.py       # Kapsamlı testler
│   └── test_performance.py # Performans testleri
├── docs/
│   ├── README.md          # Detaylı dokümantasyon
│   └── USER_MANUAL.md     # Kullanıcı kılavuzu
├── assets/
│   ├── bequickchat.png    # Uygulama ikonu
│   ├── close.png          # Sekme kapatma ikonu
│   └── [test_results]/    # Test sonuçları
├── reports/
│   ├── Report.pdf         # Proje raporu
│   └── Presentation.pptx  # Sunum
├── requirements.txt       # Python bağımlılıkları
└── README.md             # Bu dosya
```

## 🔧 Protokol Tasarımı

### Mesaj Yapısı
Her mesaj şunları içerir:
- `username`: Gönderen kullanıcı adı
- `message`: Mesaj içeriği
- `seq`: Benzersiz sıra numarası
- `msg_type`: Mesaj türü (join, leave, chat, private)
- `timestamp`: Zaman damgası

### Güvenilirlik
- Her mesajın benzersiz bir sıra numarası vardır
- Alıcı her mesaj için ACK gönderir
- ACK alınmazsa gönderici yeniden iletir (N kez)
- Çift mesaj önleme: Her istemci gönderen başına görülen sıra numaralarını takip eder

### Şifreleme
- Tüm mesajlar AES (CBC modu) ile şifrelenir
- Ağ üzerinde gizlilik sağlanır

## 🧪 Testler

### İşlevsel Test
```bash
python tests/test_functional.py
```
Temel katılma, sohbet ve ayrılma işlevselliğini kontrol eder.

### Kapsamlı Test
```bash
python tests/test_full.py
```
İki simüle edilmiş istemci ile daha kapsamlı test.

### Performans Testi
```bash
python tests/test_performance.py
```
Gecikme ve başarı oranı grafikleri oluşturur (matplotlib gerekli).

## 🎨 Özelleştirme

- **Uygulama İkonu:** `assets/bequickchat.png` dosyasını değiştirin
- **Sekme Kapatma İkonu:** `assets/close.png` dosyasını değiştirin
- **Sohbet Baloncuk Stilleri:** `src/client.py` dosyasındaki `ChatBubble` sınıfını düzenleyin

## ⚠️ Sınırlamalar

- Kimlik doğrulama yok (ek özellik olarak eklenebilir)
- MacOS'ta test edilmemiş (Windows/Linux'ta çalışır)
- Dosya transferi veya emoji desteği yok

## 🐛 Sorun Giderme

- `ConnectionResetError` alırsanız, sunucunun çalıştığından ve erişilebilir olduğundan emin olun
- GUI sorunları için PyQt5'in yüklü olduğundan ve Python sürümünün uyumlu olduğundan emin olun
- İkonlar görünmüyorsa `assets/bequickchat.png` ve `assets/close.png` dosyalarının var olduğunu ve geçerli PNG dosyaları olduğunu kontrol edin

## 👥 Geliştiriciler

- **Beyza Nur Selvi** - 222010020057
- **Furkan Fidan** - 212010020002

## 📄 Lisans

Bu proje eğitim amaçlıdır. MIT lisansı altında lisanslanmıştır.

## 🤝 Katkıda Bulunma

1. Bu depoyu fork edin
2. Yeni bir özellik dalı oluşturun (`git checkout -b feature/amazing-feature`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add some amazing feature'`)
4. Dalınıza push edin (`git push origin feature/amazing-feature`)
5. Bir Pull Request oluşturun

## 📞 İletişim

Proje hakkında sorularınız için:
- GitHub Issues: [Proje Issues Sayfası](https://github.com/yourusername/bequickchat/issues)

---

⭐ Bu projeyi beğendiyseniz yıldız vermeyi unutmayın! 