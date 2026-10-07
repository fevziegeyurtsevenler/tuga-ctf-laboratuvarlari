# İpucu
**Aşama 1: Sinyal Analizi**
Sızdırılan ses dosyası standart bir oynatıcıda dinlendiğinde sadece arka plan gürültüsü ve müzik duyulur. Ancak dijital ses dosyaları sadece duyulabilen frekanslardan ibaret değildir. Dosyayı detaylı bir ses analiz aracına (örn. Audacity) yükleyip frekansların görsel haritasını (Spectrogram) incelediğinizde, üst frekans bandına sentetik olarak işlenmiş bir mesajı fark edeceksiniz. Bu mesaj size hem ilk bayrağı verecek hem de saldırganın izini sürebileceğiniz gizli web dizinini işaret edecektir.
1. Bayrak: f298aacb94029d65caea064bff0b2ea203cc7acdf0ddb680c0d2440e4d03df0e

**Aşama 2: Dijital Kalıntı (Metadata) İncelemesi**
Sinyal analizinden elde ettiğiniz gizli rotaya eriştiğinizde, sisteme sızan şüpheliye ait bir güvenlik kamerası karesi ile karşılaşacaksınız. Bir adli bilişim uzmanı, görsel dosyalarının sadece piksellerden ibaret olmadığını bilir; dosyalar oluşturulma süreçlerine dair birçok gizli üst veri (EXIF/Metadata) barındırır. İlgili görseli bilgisayarınıza indirip metadata okuyucu araçlarla (örn. exiftool veya strings) telif/yorum katmanlarını analiz ettiğinizde, sabotajcının dijital imzasına ve ikinci bayrağa ulaşacaksınız.
2. Bayrak: d09f041fcb01b32f7fab5e20db4f7686b83f864528427a66397ef61b178e16ab