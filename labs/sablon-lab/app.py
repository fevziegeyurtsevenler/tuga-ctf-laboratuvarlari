"""
TÜGA İç Portalı — ŞABLON LAB (Web / Kolay)
==========================================
Bu, "TÜGA CTF Laboratuvarları" reposunun KOPYALANABİLİR ŞABLONUDUR.
Kendi labını yaparken bu klasörü kopyala, senaryonu ve zafiyetlerini buraya yaz.

Senaryo (kurgu): TÜGA'nın küçük bir iç personel portalı. Herkesin notları var,
bir de "selamlama" özelliği. İçeride KASITLI olarak 2 farklı zafiyet gizli.

⚠️ Bu uygulama EĞİTİM amacıyla kasıtlı olarak zafiyetlidir.
   YALNIZCA localhost'ta / izinli lab ortamında çalıştır. İnternete AÇMA.
"""
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# ── Flag'ler ──────────────────────────────────────────────────────────────
#  Not: Flag'ler açık kaynak bir labda kaynak kodda görünür — bu normaldir,
#  amaç flag'i ZAFİYETİ SÖMÜREREK bulmayı öğretmek. Katalog sitesi flag'i
#  ASLA göstermez; lab.yml içinde yalnızca sha256 HASH'i tutulur.
FLAG1 = "TUGA{idor_ile_baskasinin_notunu_okudum}"
FLAG2 = "TUGA{jinja2_ssti_ile_config_sizdirdim}"

# Gizli flag'i uygulama konfigürasyonuna koyuyoruz — SSTI ile sızacak.
app.config["GIZLI_BAYRAK"] = FLAG2

# Sahte veritabanı: her notun bir sahibi var. 42 numaralı not yöneticiye ait.
NOTLAR = {
    1:  {"sahip": "misafir", "baslik": "Hoş geldin", "icerik": "Portala hoş geldin! Kendi notların id 1-2."},
    2:  {"sahip": "misafir", "baslik": "Yapılacaklar", "icerik": "Kahve al, log'lara bak."},
    42: {"sahip": "admin",   "baslik": "GİZLİ — yönetici notu", "icerik": f"Sunucu bakım flag'i: {FLAG1}"},
}

ANA_SAYFA = """
<!doctype html><html lang=tr><meta charset=utf-8>
<title>TÜGA İç Portalı</title>
<style>body{font-family:system-ui;max-width:640px;margin:60px auto;padding:0 20px;color:#1B2340}
code{background:#F4F6FB;padding:2px 6px;border-radius:6px}a{color:#2E4FD0}</style>
<h1>🏢 TÜGA İç Portalı <small>(şablon lab)</small></h1>
<p>Merhaba <b>misafir</b>. Bu küçük portalda 2 farklı zafiyet gizli, her biri bir flag veriyor.</p>
<h3>Notların</h3>
<ul>
  <li><a href="/api/not/1">/api/not/1</a> — kendi notun</li>
  <li><a href="/api/not/2">/api/not/2</a> — kendi notun</li>
</ul>
<h3>Selamlama</h3>
<p>Adınla selam ver: <a href="/selamla?ad=Fevzi">/selamla?ad=Fevzi</a></p>
<hr>
<p style="color:#5C6683;font-size:14px">Hedef: yetkin olmayan yerlere ulaş. Flag formatı <code>TUGA{...}</code></p>
"""

@app.get("/")
def ana():
    return ANA_SAYFA

# ── ZAFİYET 1: IDOR (Insecure Direct Object Reference) ──────────────────────
#  Not id'si doğrudan alınıyor, "bu not senin mi?" kontrolü YOK.
#  Kullanıcı /api/not/42 diyerek yöneticinin notunu okuyabilir → FLAG1.
@app.get("/api/not/<int:not_id>")
def not_getir(not_id):
    n = NOTLAR.get(not_id)
    if not n:
        return jsonify({"hata": "not yok"}), 404
    # ❌ Yetki kontrolü olması gereken yer burası (kasıtlı eksik).
    return jsonify(n)

# ── ZAFİYET 2: SSTI (Server-Side Template Injection) ────────────────────────
#  Kullanıcı girdisi doğrudan şablon dizesine gömülüyor (render_template_string).
#  {{7*7}} → 49 gelirse enjeksiyon var. {{ config }} config'i döker → FLAG2.
@app.get("/selamla")
def selamla():
    ad = request.args.get("ad", "misafir")
    # ❌ Girdi doğrudan şablona gömülüyor (kasıtlı SSTI).
    kalip = "<h2>Merhaba " + ad + " 👋</h2><p><a href='/'>&larr; ana sayfa</a></p>"
    return render_template_string(kalip)

if __name__ == "__main__":
    # 0.0.0.0: container içinden dışarı (localhost eşlemesi) erişilebilsin diye.
    app.run(host="0.0.0.0", port=8080)
