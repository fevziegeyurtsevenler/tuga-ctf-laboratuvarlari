# SPOILER — çözüm anahtarı

Oyuncu arşivine koyma. Görünür diyalogda flag yok. Bölüm paketleri XOR’ludur. Önceki bölüm bitmeden `?b=N` ile atlanamaz.

Dağılım: aynı kategori yan yana değil; OSINT = reverse = 2.

| Slot | Kategori | Flag | Yer |
|------|----------|------|-----|
| I-1 | Web | `TUGA{g1s3_h1c_4c1lm4d1}` | `<meta name="generator">` |
| I-2 | Kodlama | `TUGA{g3c3_v4rd1y4s1}` | `files/bilet.txt` hex |
| I-3 | Stego | `TUGA{f3n3r_t3l_0rgu}` | `css/game.css` `.bant.u::after` |
| II-1 | Kodlama | `TUGA{sf074_y4n11s_r4f}` | gizli `#raf` SVG (ondalık ASCII) |
| II-2 | Adli | `TUGA{v1tr1n_k4m3r4s1}` | `vitrin.jpg` UserComment hex (başlık sahte) |
| II-3 | Web | `TUGA{c1t_dustu_kukr3m3}` | kesinti `localStorage` / `k` hex |
| III-1 | Kodlama | `TUGA{l4r4_l0ck_1z1n1_4mb3rd3_b1r4kt1}` | `last-call.html` JSON `n` |
| III-2 | Stego | `TUGA{r04r_k4s3tt3_g1zl1}` | `saha_kaydi_1994.wav` spektrogram |
| III-3 | OSINT | `TUGA{s4h4_k1t1_4c1k_k4yn4k}` | `kaset_kutu.jpg` EXIF (GitHub) veya `robots.txt` → `/kit/` |
| IV-1 | Reverse | `TUGA{n1ght_h4tch_h1c_4c1lm4d1}` | `./bone_tagger SF-074` |
| IV-2 | OSINT | `TUGA{d0sy4_k4p4nd1_1994}` | `robots.txt` → `/files/sicil.html` |
| IV-3 | Reverse | `TUGA{0v3rl4y_sf074}` | `./bone_tagger SF-074-DEEP` (`_m`) |

Bitiş: Lara kaydı, ardından Rahile Pelin Yakar.

Baraka (bölüm III): önce III-1 mühürlenir; arka kapı açılır. Barakadan `kafe` ile dönülür.
