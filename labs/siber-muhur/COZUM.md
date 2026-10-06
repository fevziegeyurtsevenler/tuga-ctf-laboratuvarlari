# ☩ Siber Mühür // Çözüm Anahtarı (Write-up)

> ⚠️ **UYARI:** SPOILER İÇERİR! Bu dokümanı laboratuvarı kendi başınıza çözmeyi denedikten sonra incelemeniz tavsiye edilir.

---

## Bölüm I: Ağ Çevresi İhlali (Initial Access)
**Hedef:** Saldırganın sisteme sızdığı zafiyeti ve web shell yüklemesini bulmak.
* **Analiz Edilen Dosya:** `access.log`
* **Adli Bilişim Süreci:** 
  1. Sunucu erişim günlükleri incelendiğinde, saldırganın (APT-Erebos) `python-requests` aracı ile sisteme brute-force denemeleri yaptığı ve `/api/v1/archive_auth.php` uç noktasından `401 Unauthorized` yanıtları aldığı görülür.
  2. Saldırganın, uygulamanın dosya indirme parametresini istismar ederek `/api/v1/download?file=../../../../etc/passwd` üzerinden LFI (Local File Inclusion) zafiyetini sömürdüğü tespit edilir.
  3. LFI sonrası saldırganın URL-encode edilmiş bir komut çalıştırdığı (Web Shell) log satırından yakalanır (`&cmd=auth&key=TUG%41...`). Analist bu URL verisini decode ettiğinde ilk mühre ulaşır.
* **Mühür 1:** `TUGA{b4nkcd00cl_4uth_s34l}`

---

## Bölüm II: Sistem İçi İzler ve Çalıştırma (Execution & Evasion)
**Hedef:** Tersine mühendislik ile gizlenmiş komut satırını deşifre etmek.
* **Analiz Edilen Dosya:** `.bash_history`
* **Adli Bilişim Süreci:** 
  1. Sisteme sızan aktörün Linux komut geçmişi incelendiğinde, `shred -u` komutu ile dosya silerek anti-forensic (iz kaybettirme) faaliyetlerinde bulunduğu saptanır.
  2. Dosyanın son satırlarında oldukça şüpheli, Base64 karakter setine benzeyen ancak tersine çevrilmiş (reversed) bir string dizgesi bulunur.
  3. Bu dizgenin borulama (pipe) mimarisiyle `rev | base64 -d` komutlarına aktarıldığı görülür. 
  4. Analist olarak bu kod parçası alınıp Linux terminalinde veya CyberChef aracı üzerinden (önce "Reverse", ardından "From Base64" işlemleri uygulanarak) çözüldüğünde gerçek zararlı yük (payload) ortaya çıkar.
* **Mühür 2:** `TUGA{s0w2N1bHRfZDczbTBuX2JjMzN4}`

---

## Bölüm III: Ağ Üzerinden Veri Sızdırma (Exfiltration)
**Hedef:** DNS tünelleme kanalıyla dışarı sızdırılan veriyi haritalamak.
* **Analiz Edilen Dosya:** `dns_queries.log`
* **Adli Bilişim Süreci:**
  1. Ağ logları incelendiğinde, belirli bir alan adına (`*.malicious-c2.com` gibi) normalden çok daha uzun, rastgele karakterler içeren alt alan adlarıyla (subdomain) TXT sorguları yapıldığı fark edilir.
  2. DNS tünelleme şüphesiyle bu alt alan adları incelendiğinde, karakterlerin HEX (Onaltılık) formatında olduğu anlaşılır. (Saldırgan veriyi dışarı kaçırmak için şifrelemiş ve parçalara bölmüştür).
  3. Logdaki tüm HEX değerleri (subdomain parçaları) sırasıyla kopyalanıp birleştirilir.
  4. Birleştirilen veri yığını CyberChef üzerinde "From Hex" modülü ile ASCII metnine dönüştürüldüğünde, çalınan verinin içeriği ve ağ bayrağı deşifre edilir.
* **Mühür 3:** `TUGA{3xf1ltr4t10n_v14_dn5_tunnel}`

---

## Bölüm IV: Kalıcılık ve Zararlı Yazılım Vektörleri (Persistence & C2)
**Hedef:** Systemd servisini ve arka planda çalışan Python C2 betiğini analiz etmek.
* **Analiz Edilen Dosya:** `sys_update.service` ve `system_worker.py`
* **Adli Bilişim Süreci:**
  1. Sistemin her yeniden başlatılmasında zararlının çalışması için oluşturulan sahte bir güncelleme servisi (`sys_update.service`) tespit edilir.
  2. Bu servisin tetiklediği Python betiği (`system_worker.py`) incelendiğinde, kodun içinde `C2_AUTH_BLOB` adında HEX (Onaltılık) formatta bir veri dikkat çeker. Ancak bu veri ASCII'ye çevrildiğinde `TUGA{n1c3_try_but_f4k3}` sonucunu verir (Bu, tecrübesiz analistleri yavaşlatmak için konulmuş bir "Rabbit Hole" tuzağıdır).
  3. Kodun daha derin statik analizi yapıldığında, asıl komuta-kontrol verisinin `P1`, `P2`, `P3` isimli değişkenlere parçalandığı ve çalışma zamanında (runtime) birleştirilerek çalıştırıldığı (Obfuscation) keşfedilir.
  4. Bu parçalar manuel olarak uç uca eklenip Base64 ile çözüldüğünde, asıl hedefe ulaşılarak tehdit mühürlenir.
* **Mühür 4:** `TUGA{p3rs1st3nc3_thr0ugh_5yst3md}`

