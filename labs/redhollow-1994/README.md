# Night Hatch — Redhollow 1994

1994’te hiç açılmayan bir dinozor parkı. Dr. Lara Lock kayıtlara göre kayıp; sen arşivcisin. Park mühürlenmeden önce geride işaretler bırakılmış. Hepsi localhost’ta.

## Kurulum

```bash
docker compose up -d --build
```

Tarayıcı: http://localhost:8080

Kapatmak için:

```bash
docker compose down -v
```

Numune etiketleyici Linux ELF’tir. Windows’ta doğrudan çalışmaz:

```bash
docker compose run --rm analyzer
./bone_tagger
```

Hoparlörü aç. İlerleme tarayıcıda tutulur; konteyneri kapatmak kaydı silmez.

## Hedef

On iki işaret, biçim: `TUGA{...}`

Bulduklarını [TÜGA katalog sitesindeki](https://fevziegeyurtsevenler.github.io/tuga-ctf-laboratuvarlari/) doğrulama kutusuna yazabilirsin. Flag’ler sitede gösterilmez.

Sahnedeki noktalara tıkla. Diyalogda flag yazmaz. Kaynak, stil, indirilen dosya, metadata, ses, dizin ve ikiliye bak. Sağ altta işaret gir. Önceki bölüm bitmeden sonrakine geçilmez.

## Uyarı

Bu lab eğitim için kasıtlı zafiyetlidir. Yalnızca localhost’ta / izinli ortamda çalıştır, internete açma. Ayrıntı: [SECURITY.md](../../SECURITY.md).
