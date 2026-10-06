import base64
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "game" / "js" / "bolum"
ROOT.mkdir(parents=True, exist_ok=True)

chapters = {
    1: {
        "etiket": "BÖLÜM I · FIRTINA ÖNCESİ",
        "baslik": "NIGHT HATCH",
        "alt": "bölüm I — gişe",
        "foto": "assets/ch1-gise.jpg",
        "giris": [
            {"k": "", "t": "Yağmur. Tel örgü. Uzakta bir jeneratör son nefesini veriyor.", "ic": True},
            {
                "k": "",
                "t": "Night Hatch Dino Park. 1994’te açılacaktı. Açılmadı. Bir gece her şey mühürlendi.",
                "ic": True,
            },
            {
                "k": "",
                "t": "Dr. Lara Lock — paleogenetikçi — kayıtlara göre kayıp. Geride sadece işaretler bıraktı.",
            },
            {
                "k": "",
                "t": "Sen arşivcisin. Görevin: onun bıraktığı üç izi bulup gişe kapısını açmak. Fenerin var.",
            },
        ],
        "noktalar": [
            {
                "id": "tabela",
                "x": "46%",
                "y": "28%",
                "ad": "tabela",
                "konus": [
                    {
                        "k": "",
                        "t": "Lara buraya tabelalar bırakırdı. Görünen yazı her zaman doğru değildi.",
                        "ic": True,
                    },
                    {
                        "k": "tabela",
                        "t": "YAKINDA AÇILIYOR. Boya taze, yalan eski. Tabelanın arkası sayfanın başına sinmiş.",
                    },
                ],
            },
            {
                "id": "tel",
                "x": "72%",
                "y": "44%",
                "ad": "tel örgü",
                "konus": [
                    {
                        "k": "",
                        "t": "Çit, parkı içeridekilerden değil… dışarıdakilerden korumak içindi. İşe yaramadı.",
                        "ic": True,
                    },
                    {
                        "k": "tel",
                        "t": "Çit ölü. Üst bant hâlâ fısıldıyor; boya değil, stil dosyasının içine gömülü.",
                    },
                ],
            },
            {
                "id": "bilet",
                "x": "22%",
                "y": "64%",
                "ad": "bilet",
                "dosya": "files/bilet.txt",
                "konus": [
                    {
                        "k": "",
                        "t": "Gişe hiç açılmadı. Yine de birileri bilet basmış.",
                        "ic": True,
                    },
                    {
                        "k": "gişe",
                        "t": "Islak bilet. Sıra satırı garip — sayılar harf gibi dizilmiş.",
                    },
                ],
            },
            {
                "id": "kapi",
                "x": "84%",
                "y": "58%",
                "ad": "kapı",
                "konus": [
                    {
                        "k": "kapı",
                        "t": "İçeri ancak üç işaretle girilir. Lara’nın personel paneli hâlâ boş — izleri sen toplayacaksın.",
                    }
                ],
            },
        ],
    },
    2: {
        "etiket": "BÖLÜM II · ÇİT DÜŞTÜ",
        "baslik": "NIGHT HATCH",
        "alt": "bölüm II — kemik sergisi",
        "foto": "assets/ch2-sergi.jpg",
        "giris": [
            {
                "k": "",
                "t": "Sergi salonu. Toz. Camların arkasında fosiller — ya da öyle sanılıyor.",
                "ic": True,
            },
            {
                "k": "",
                "t": "Lara’nın notu: “SF-074 yanlış yerde. Kimse dokunmasın.” Dokunmuşlar.",
            },
            {
                "k": "",
                "t": "Dışarıda bir şey yürüyor. Ayak sesi… çok ağır. Üç iz daha var burada.",
            },
        ],
        "noktalar": [
            {
                "id": "vitrin",
                "x": "44%",
                "y": "40%",
                "ad": "vitrin",
                "vinyet": "assets/vitrin.jpg",
                "konus": [
                    {
                        "k": "",
                        "t": "Vitrindeki etiket ziyaretçi içindi. Asıl kayıt başka yerde dururdu.",
                        "ic": True,
                    },
                    {
                        "k": "etiket",
                        "t": "SF-074. Etiket yalan söylüyor. Raf çiziminin içine bir şey sıkışmış.",
                    },
                ],
            },
            {
                "id": "kamera",
                "x": "72%",
                "y": "30%",
                "ad": "kamera",
                "dosya": "assets/vitrin.jpg",
                "konus": [
                    {
                        "k": "",
                        "t": "Güvenlik kamerası son kareyi kaydetmiş. Lara ‘fotoğraf konuşur’ derdi — bazen sessizce.",
                        "ic": True,
                    },
                    {
                        "k": "kamera",
                        "t": "Son kare. Kaydet. Görüntü yalan söylemez ama özellikleri bazen yalan söyler — başlık en gürültülüsü.",
                    },
                ],
            },
            {
                "id": "koridor",
                "x": "12%",
                "y": "48%",
                "ad": "koridor",
                "konus": [
                    {
                        "k": "",
                        "t": "Koridor personel kafesine iner. Çit o gece buradan düşmüş.",
                        "ic": True,
                    },
                    {"k": "", "t": "Işıklar düştü.", "ic": True},
                ],
            },
        ],
    },
    3: {
        "etiket": "BÖLÜM III · PERSONEL KAFESİ",
        "baslik": "NIGHT HATCH",
        "alt": "bölüm III — amber ve kaset",
        "foto": "assets/ch3-amber.jpg",
        "giris": [
            {
                "k": "",
                "t": "Personel kafesi. Milkshake makinesi hâlâ vızıldıyor. Elektrik kesik olmalıydı.",
                "ic": True,
            },
            {
                "k": "",
                "t": "Rachel Mia — Lara’nın asistanı — son vardiyada burada kalmış. Sonra susmuş.",
            },
            {
                "k": "Rachel",
                "t": "Lara vitrine yazma dedi. Her şeyi last-call’a gömdü. Eski takma adını hâlâ kullanıyordu.",
            },
            {
                "k": "",
                "t": "Üç iz kaldı: Rachel’ın notu, saha kaseti, Lara’nın açık bıraktığı bir şey.",
            },
        ],
        "altSahne": {"foto": "assets/ch3-baraka.jpg", "tetik": "jenerator"},
        "noktalar": [
            {
                "id": "menu",
                "x": "30%",
                "y": "58%",
                "ad": "tezgâh",
                "dosya": "files/last-call.html",
                "konus": [
                    {
                        "k": "",
                        "t": "Tezgâhın altı Rachel’ın sığınağıydı. Lara’ya son mesajını oraya sıkıştırmış.",
                        "ic": True,
                    },
                    {
                        "k": "not",
                        "t": "Sayfa last-call. Üstteki metin eksik; altında başka bir dil var.",
                    },
                ],
            },
            {
                "id": "jenerator",
                "x": "70%",
                "y": "42%",
                "ad": "arka kapı",
                "konus": [
                    {
                        "k": "",
                        "t": "Arka kapı barakaya açılıyor. Jeneratör ve kaset odası — Lara’nın saha laboratuvarı.",
                        "ic": True,
                    },
                    {"k": "", "t": "Kapı aralık. İçeriden metal ve yağ kokusu geliyor."},
                ],
            },
            {
                "id": "kaset",
                "x": "52%",
                "y": "68%",
                "ad": "kasetçalar",
                "gizli": True,
                "dosya": "assets/saha_kaydi_1994.wav",
                "vinyet": "assets/kaset.jpg",
                "konus": [
                    {
                        "k": "",
                        "t": "Bu kaset dışarıdaki kükremeyi kaydetmiş. Lara spektruma bakmadan dinlemezdi.",
                        "ic": True,
                    },
                    {
                        "k": "kaset",
                        "t": "LED yanıyor. Dinlemek yetmez — frekansına bak. Parkın dizininde bir spektrum sayfası da duruyor.",
                    },
                ],
            },
            {
                "id": "kutu",
                "x": "20%",
                "y": "36%",
                "ad": "kaset kutusu",
                "gizli": True,
                "dosya": "assets/kaset_kutu.jpg",
                "vinyet": "assets/kaset_kutu.jpg",
                "konus": [
                    {
                        "k": "",
                        "t": "Lara bir şeyleri kasıtlı açık bırakmıştı. ‘Kapalı park, açık kayıt’ derdi.",
                        "ic": True,
                    },
                    {
                        "k": "kutu",
                        "t": "İç kapak fotoğrafı. Kaydet. Etiket yalan — dosyanın kendi notuna bak.",
                    },
                ],
            },
        ],
    },
    4: {
        "etiket": "BÖLÜM IV · MÜHÜR",
        "baslik": "NIGHT HATCH",
        "alt": "bölüm IV — park kapısı",
        "foto": "assets/ch4-kapi.jpg",
        "giris": [
            {
                "k": "",
                "t": "Ana kapı. Zincir. Sis. Pençe izi taze — ya da taze bırakılmış.",
                "ic": True,
            },
            {
                "k": "",
                "t": "Arşivin son katmanı burada. Lara parkı mühürlemeden önce üç son işaret bıraktı.",
            },
            {
                "k": "",
                "t": "Gişede unutulan program: bone_tagger. Numune kodu hâlâ aynı: SF-074.",
            },
            {
                "k": "Lara",
                "t": "Çıkışa acele etme. Önce izleri tamamla. Sonra… dışarı çıkma. Beni dinle.",
            },
        ],
        "noktalar": [
            {
                "id": "program",
                "x": "22%",
                "y": "62%",
                "ad": "program",
                "dosya": "downloads/bone_tagger",
                "konus": [
                    {
                        "k": "",
                        "t": "Etiketleyici, numuneleri okumak içindi. Lara onu kasıtlı bırakmış.",
                        "ic": True,
                    },
                    {
                        "k": "etiketleyici",
                        "t": "İndir. Bu makinede uyanmaz — kafeste, numune etiketiyle konuşur.",
                    },
                ],
            },
            {
                "id": "derin",
                "x": "74%",
                "y": "40%",
                "ad": "mühür",
                "konus": [
                    {
                        "k": "",
                        "t": "Mühür tek katmanlı değildi. İkinci anahtar derinde uyuyor.",
                        "ic": True,
                    },
                    {
                        "k": "mühür",
                        "t": "İkinci mühür paketin içinde uyuyor. Kısa bir dizi — harfler sayı kılığına girmiş.",
                    },
                ],
            },
            {
                "id": "cikis",
                "x": "48%",
                "y": "46%",
                "ad": "çıkış",
                "konus": [
                    {
                        "k": "",
                        "t": "Kapının ötesi orman. Botlar bu parkı taramasın diye Lara bir dizin yasağı bırakmış.",
                        "ic": True,
                    },
                    {
                        "k": "Lara",
                        "t": "Sicili açıkta bırakmadım. Sadece tarayıcıların görmemesi gereken bir yol var. Sonra dışarı çıkma.",
                    },
                ],
            },
        ],
    },
}

flags = {
    1: {
        "I-1": "1d0618ecb1e2b0c499be9033464b5ad1de38dcb16cce1dd4bbab90d5f9f15a20",
        "I-2": "3a13949ecec6a4ef935b0acdae597bd0f1a1269b36b2fb286eb40b46f10d6a8f",
        "I-3": "155c8d1cd6780ce7f5faa7b5846a5140d522e8dd25d28cbdc87f5d40d5112159",
    },
    2: {
        "II-1": "21ed4458771e260c6cf31d85a7777962f31ac561b0e969a9f5379ded1a2ecd31",
        "II-2": "e7d469d0f53791e7ac973a3871a3c0acd2593b64758317369c0c482b0da3a3fd",
        "II-3": "057c85a6d46c9caffd9cfaff8eef5aad85872551c9ec5a1dbdfe2d65fad8600c",
    },
    3: {
        "III-1": "d1012c641cba30f6058db15fe466ac495db067c2f64508764832484d6b9ceeee",
        "III-2": "073ecd1e1baf415b6797f37b6ced5cc4644b0f5ad450e0ef82768d3c0a8cc906",
        "III-3": "294ea550ea4bc5f45d65d379bd21f02bc1fdde8cfd20d7126b8301e9c7f9d722",
    },
    4: {
        "IV-1": "edf3a8186b00c07866768c4184612e788d10f07859b54656325dabb660404c73",
        "IV-2": "87b8fa18123ef08acc6d5e4c80023d9968b93ed8320800f33e6cf6fa695a724c",
        "IV-3": "fd4ac05ea7dba3d2ccf2b8485f9b2fe9a2a684faf5806b74401a38f4988ae3d5",
    },
}

slots = {
    1: ["I-1", "I-2", "I-3"],
    2: ["II-1", "II-2", "II-3"],
    3: ["III-1", "III-2", "III-3"],
    4: ["IV-1", "IV-2", "IV-3"],
}

for n, data in chapters.items():
    payload = {"story": data, "flags": flags[n], "slots": slots[n], "giz": {}}
    if n == 1:
        payload["giz"] = {
            "generator": "TUGA{g1s3_h1c_4c1lm4d1}",
            "kapanis": "Gişe açıldı. İlk üç iz tamam. Sergi seni bekliyor — ve dışarıdaki ayak sesleri.",
        }
    if n == 2:
        payload["giz"] = {
            "raf": "84 85 71 65 123 115 102 48 55 52 95 121 52 110 49 49 115 95 114 52 102 125",
            "cerez": [
                84,
                85,
                71,
                65,
                123,
                99,
                49,
                116,
                95,
                100,
                117,
                115,
                116,
                117,
                95,
                107,
                117,
                107,
                114,
                51,
                109,
                51,
                125,
            ],
            "kopru": [
                {"k": "", "t": "Gişenin ardı sergi salonu. Lara’nın fosil odası.", "ic": True},
                {
                    "k": "",
                    "t": "Çit düşmeden önce burada turlar planlanmıştı. Şimdi sadece toz ve yanlış yerleştirilmiş kemikler var.",
                },
                {"k": "", "t": "Üç iz daha. Sonra personel kafesine inebilirsin."},
            ],
            "sonra": [
                {
                    "k": "",
                    "t": "Çit düştü. Kükreme dışarıdan değil — belki içeriden de.",
                    "ic": True,
                },
                {
                    "k": "",
                    "t": "Bir şey tarayıcıda kaldı. Kaset değil. İzi kaçırma.",
                    "ic": True,
                },
            ],
            "kapanis": "Sergi mühürlendi. Kükreme uzaklaştı — ya da saklandı. Rachel’ın kafesi sırada.",
        }
    if n == 3:
        payload["giz"] = {
            "kopru": [
                {
                    "k": "",
                    "t": "Personel kafesi. Lara ve Rachel son geceyi burada geçirmiş. Baraka arka kapıda.",
                    "ic": True,
                },
                {
                    "k": "",
                    "t": "Amber vitrinler, kasetler, açık kaynak… Lara her şeyi ‘iz bırakarak’ kaçırmış.",
                },
                {"k": "", "t": "Üç iz. Sonra ana kapı."},
            ],
            "sonra": [
                {"k": "", "t": "Baraka. Yağ, demir, eski kaset kokusu.", "ic": True},
                {"k": "", "t": "Bir an bir şeyin nefes aldığını sanıyorsun. Çok yakın."},
                {"k": "", "t": "Hayır. Kasetçalar. Kırmızı LED. Lara’nın saha kaydı hâlâ burada."},
            ],
            "kilit": [
                {
                    "k": "",
                    "t": "Arka kapı kilitli. Rachel tezgâha bir şey bırakmış — önce o izi mühürle.",
                }
            ],
            "geri": [
                {"k": "", "t": "Kafe. Milkshake makinesi, toz, tezgâh.", "ic": True},
                {"k": "", "t": "Baraka arka kapıdan duruyor. İstersen yine girersin."},
            ],
            "kapanis": "Kafe ve baraka kapandı. Lara’nın son mühürü park kapısında bekliyor.",
        }
    if n == 4:
        payload["giz"] = {
            "m": [83, 70, 45, 48, 55, 52, 45, 68, 69, 69, 80],
            "kopru": [
                {
                    "k": "",
                    "t": "Ana kapı. Zincirler 1994’ten beri hiç açılmamış olmalı.",
                    "ic": True,
                },
                {
                    "k": "",
                    "t": "Ama pençe izi taze. Ya bir şey çıktı… ya da birisi öyle görünmesini istedi.",
                },
                {
                    "k": "Lara",
                    "t": "Son üç işaret. Sonra kaydımı dinle. Dışarı çıkma. Lütfen.",
                },
            ],
        }
    raw = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    key = f"nh{n}".encode()
    xored = bytes(b ^ key[i % len(key)] for i, b in enumerate(raw))
    xb64 = base64.b64encode(xored).decode("ascii")
    (ROOT / f"{n}.js").write_text(f"window.__PACK={json.dumps(xb64)};\n", encoding="utf-8")
    print("wrote", n, len(xb64))
