# Draft Eğitim Web Sitesi

Bu proje, Draft Eğitim Danışmanlığı için geliştirilmiş modern bir web sitesidir. Flask framework'ü kullanılarak oluşturulmuştur.

## Özellikler

- Responsive tasarım
- Kullanıcı kayıt ve giriş sistemi
- Danışmanlık başvuru formu
- Modern ve kullanıcı dostu arayüz
- Bootstrap 5 entegrasyonu
- SQLite veritabanı

## Kurulum

1. Python 3.8 veya daha yüksek bir sürümün yüklü olduğundan emin olun.

2. Gerekli paketleri yükleyin:
```bash
pip install -r requirements.txt
```

3. Uygulamayı çalıştırın:
```bash
python app.py
```

4. Tarayıcınızda `http://localhost:5000` adresine gidin.

## Proje Yapısı

```
draft-egitim/
├── app.py                  # Ana uygulama dosyası
├── requirements.txt        # Gerekli Python paketleri
├── static/                 # Statik dosyalar
│   └── css/
│       └── style.css      # CSS stilleri
└── templates/             # HTML şablonları
    ├── base.html          # Ana şablon
    ├── home.html          # Ana sayfa
    └── contact.html       # İletişim sayfası
```

## Geliştirme

1. Veritabanını sıfırlamak için:
```python
with app.app_context():
    db.drop_all()
    db.create_all()
```

2. Yeni bir sayfa eklemek için:
   - `templates/` klasörüne yeni bir HTML şablonu ekleyin
   - `app.py` dosyasına yeni bir route ekleyin
   - Gerekirse `base.html` dosyasındaki navigasyon menüsünü güncelleyin

## Lisans

Bu proje MIT lisansı altında lisanslanmıştır. 