# Katkıda Bulunma Rehberi

BeQuickChat projesine katkıda bulunmak istediğiniz için teşekkürler! Bu rehber, projeye nasıl katkıda bulunabileceğinizi açıklar.

## 🚀 Başlarken

1. Bu depoyu fork edin
2. Yerel makinenizde klonlayın:
   ```bash
   git clone https://github.com/YOUR_USERNAME/bequickchat.git
   cd bequickchat
   ```
3. Geliştirme ortamınızı kurun:
   ```bash
   pip install -r requirements.txt
   ```

## 🔧 Geliştirme Süreci

### 1. Yeni Bir Dal Oluşturun
```bash
git checkout -b feature/your-feature-name
# veya
git checkout -b fix/your-bug-fix
```

### 2. Değişikliklerinizi Yapın
- Kod yazarken PEP 8 stil rehberini takip edin
- Yeni özellikler için testler yazın
- Mevcut testlerin geçtiğinden emin olun

### 3. Testleri Çalıştırın
```bash
# İşlevsel testler
python tests/test_functional.py

# Kapsamlı testler
python tests/test_full.py

# Performans testleri
python tests/test_performance.py
```

### 4. Değişikliklerinizi Commit Edin
```bash
git add .
git commit -m "feat: yeni özellik eklendi"
git commit -m "fix: hata düzeltildi"
git commit -m "docs: dokümantasyon güncellendi"
```

### 5. Push Edin ve Pull Request Oluşturun
```bash
git push origin feature/your-feature-name
```

## 📝 Commit Mesaj Formatı

Commit mesajlarınızı şu formatta yazın:
- `feat:` Yeni özellik
- `fix:` Hata düzeltmesi
- `docs:` Dokümantasyon değişiklikleri
- `style:` Kod formatı değişiklikleri
- `refactor:` Kod yeniden düzenleme
- `test:` Test ekleme veya düzenleme
- `chore:` Yapılandırma değişiklikleri

## 🧪 Test Yazma

### Yeni Test Ekleme
1. `tests/` klasöründe uygun test dosyasını bulun
2. Test fonksiyonunuzu ekleyin
3. Testin açıklayıcı bir adı olduğundan emin olun
4. Test senaryosunu dokümante edin

### Test Örneği
```python
def test_new_feature():
    """Test yeni özelliğin doğru çalıştığını doğrular."""
    # Test setup
    client = ChatClient("test_user")
    
    # Test execution
    result = client.new_feature()
    
    # Assertions
    assert result is not None
    assert result.status == "success"
```

## 🔍 Kod İnceleme Süreci

1. Pull Request'inizi oluşturun
2. Açıklayıcı bir başlık ve açıklama yazın
3. Değişikliklerinizi detaylandırın
4. Test sonuçlarını ekleyin
5. Gerekirse ekran görüntüleri ekleyin

## 📋 Pull Request Şablonu

```markdown
## Değişiklik Türü
- [ ] Hata düzeltmesi
- [ ] Yeni özellik
- [ ] Dokümantasyon güncellemesi
- [ ] Performans iyileştirmesi

## Açıklama
Bu PR'ın ne yaptığını açıklayın.

## Test Edildi mi?
- [ ] Evet, tüm testler geçiyor
- [ ] Yeni testler eklendi
- [ ] Manuel test yapıldı

## Ekran Görüntüleri (varsa)
[Buraya ekran görüntüleri ekleyin]

## Kontrol Listesi
- [ ] Kod PEP 8 standartlarına uygun
- [ ] Yeni özellikler için testler eklendi
- [ ] Dokümantasyon güncellendi
- [ ] Commit mesajları açıklayıcı
```

## 🐛 Hata Bildirme

Hata bildirirken şu bilgileri ekleyin:
- İşletim sistemi ve sürümü
- Python sürümü
- Hata mesajı
- Hatanın nasıl oluştuğu
- Beklenen davranış

## 💡 Özellik Önerileri

Yeni özellik önerirken:
- Özelliğin amacını açıklayın
- Kullanım senaryolarını belirtin
- Varsa tasarım önerilerini ekleyin
- Öncelik seviyesini belirtin

## 📞 İletişim

Sorularınız için:
- GitHub Issues kullanın
- Pull Request'lerde tartışın
- Gerekirse e-posta gönderin

## 🙏 Teşekkürler

BeQuickChat projesine katkıda bulunduğunuz için teşekkürler! Her katkınız projeyi daha iyi hale getiriyor. 