const $ = (s) => document.querySelector(s);

const params = new URLSearchParams(location.search);
let bolum = Math.min(4, Math.max(1, parseInt(params.get("b") || localStorage.getItem("nh-bolum") || "1", 10) || 1));
let bulunan = {};
try {
  bulunan = JSON.parse(localStorage.getItem("nh-flags") || "{}") || {};
} catch (e) {
  bulunan = {};
  localStorage.removeItem("nh-flags");
}

let FLAGS = {};
let BOLUM_SLOTS = [];
let STORY = null;
let GIZ = {};

const kutu = $("#kutu");
const metinEl = $("#metin");
const konusanEl = $("#konusan");
const devamEl = $("#devam");

let yaziliyor = false;
let tamMetin = "";
let tik = null;
let bekleyen = null;
let kesikYapildi = false;
let barakada = false;
let muzik = null;
let muzikAcik = false;
let sesIstemiyor = false;

function oncekiTam(n) {
  if (n <= 1) return true;
  return BOLUM_SLOT_IDS[n - 1].every((id) => bulunan[id]);
}

function acikBolum() {
  let max = 1;
  for (let i = 1; i <= 4; i++) {
    if (oncekiTam(i)) max = i;
    else break;
  }
  return max;
}

async function sha(t) {
  const b = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(t.trim()));
  return Array.from(new Uint8Array(b)).map((x) => x.toString(16).padStart(2, "0")).join("");
}

function kaydet() {
  localStorage.setItem("nh-flags", JSON.stringify(bulunan));
  localStorage.setItem("nh-bolum", String(bolum));
}

function slotCiz() {
  const el = $("#slotlar");
  if (!el) return;
  el.innerHTML = "";
  BOLUM_SLOTS.forEach((id) => {
    const s = document.createElement("div");
    s.className = "slot" + (bulunan[id] ? " dolu" : "");
    s.textContent = id + (bulunan[id] ? " alındı" : " boş");
    el.appendChild(s);
  });
}

function bolumTam() {
  return BOLUM_SLOTS.every((id) => bulunan[id]);
}

function ctfTam() {
  return [1, 2, 3, 4].every((n) => BOLUM_SLOT_IDS[n].every((id) => bulunan[id]));
}

function muzikKur() {
  if (muzik) return;
  muzik = new Audio("assets/gece.wav");
  muzik.loop = true;
  muzik.volume = 0.38;
}

function sesAc(kullanici) {
  if (!kullanici && sesIstemiyor) return;
  if (kullanici) sesIstemiyor = false;
  muzikKur();
  muzikAcik = true;
  muzik.play().catch(() => {});
  const b = $("#sesBtn");
  if (b) b.textContent = "ses açık";
}

function sesKapat(kullanici) {
  if (kullanici) sesIstemiyor = true;
  muzikAcik = false;
  if (muzik) {
    muzik.pause();
    muzik.currentTime = 0;
  }
  const b = $("#sesBtn");
  if (b) b.textContent = "ses";
}

function kukreme(dosya, maxMs) {
  const a = new Audio(dosya || "assets/kukreme.mp3");
  a.volume = 0.9;
  if (muzik && muzikAcik) muzik.volume = 0.08;
  const bitir = () => {
    try {
      a.pause();
      a.currentTime = 0;
    } catch (_) {}
    if (muzik && muzikAcik) muzik.volume = 0.38;
  };
  a.addEventListener("ended", bitir);
  a.play().catch(() => {});
  setTimeout(bitir, maxMs != null ? maxMs : 10000);
}

function sahneAc(id) {
  document.querySelectorAll(".sahne").forEach((s) => s.classList.remove("aktif"));
  const el = $(id);
  if (el) el.classList.add("aktif");
  document.body.classList.toggle("oda-modu", id === "#s-oda");
}

function karart(sonra) {
  const p = $("#perde");
  if (!p) {
    sonra();
    return;
  }
  p.style.opacity = "1";
  setTimeout(() => {
    sonra();
    p.style.opacity = "0";
  }, 700);
}

function yaz(metin, ic) {
  yaziliyor = true;
  tamMetin = metin || "";
  metinEl.textContent = "";
  metinEl.classList.toggle("ic", !!ic);
  devamEl.classList.remove("gorun");
  let i = 0;
  clearInterval(tik);
  tik = setInterval(() => {
    i += 1;
    metinEl.textContent = tamMetin.slice(0, i);
    if (i >= tamMetin.length) {
      clearInterval(tik);
      yaziliyor = false;
      devamEl.classList.add("gorun");
    }
  }, 16);
}

function konusma(dizi, bittiginde) {
  kutu.classList.add("acik");
  let n = 0;
  function adim() {
    if (n >= dizi.length) {
      bekleyen = null;
      if (bittiginde) bittiginde();
      return;
    }
    const s = dizi[n++];
    konusanEl.textContent = s.k || "";
    yaz(s.t, s.ic);
    bekleyen = adim;
  }
  adim();
}

function ilerle() {
  if (epilogBekliyor) {
    laraKaydiCal();
    return;
  }
  if (document.body.classList.contains("bitti")) return;
  if (!muzikAcik) sesAc();
  if (yaziliyor) {
    clearInterval(tik);
    metinEl.textContent = tamMetin;
    yaziliyor = false;
    devamEl.classList.add("gorun");
    return;
  }
  if (bekleyen) bekleyen();
}

function vinyetGoster(src, href) {
  const v = $("#vinyet");
  if (!src) {
    if (v) v.classList.remove("gorun");
    return;
  }
  $("#vinyetImg").src = src;
  const a = $("#vinyet a");
  if (href) {
    a.href = href;
    a.style.display = "block";
    a.textContent = "indir";
  } else {
    a.style.display = "none";
  }
  v.classList.add("gorun");
}

function sahneKutuAyar() {
  const wrap = $("#odaFoto");
  const img = $("#odaImg");
  const kat = $("#k-yakin");
  if (!wrap || !img || !kat || !img.naturalWidth) return;
  const cw = wrap.clientWidth;
  const ch = wrap.clientHeight;
  if (!cw || !ch) return;
  const scale = Math.min(cw / img.naturalWidth, ch / img.naturalHeight);
  const w = img.naturalWidth * scale;
  const h = img.naturalHeight * scale;
  kat.style.left = (cw - w) / 2 + "px";
  kat.style.top = (ch - h) / 2 + "px";
  kat.style.width = w + "px";
  kat.style.height = h + "px";
}

function elektrikKes(sonra) {
  const p = $("#perde");
  kukreme("assets/kukreme.mp3", 10000);
  document.body.classList.add("kesik");
  if (p) {
    p.style.transition = "none";
    p.style.opacity = "1";
  }
  setTimeout(() => {
    if (p) {
      void p.offsetWidth;
      p.style.transition = "opacity .25s ease";
      p.style.opacity = "0";
    }
    document.body.classList.remove("kesik");
    if (sonra) sonra();
  }, 1200);
}

function bolumHazirlik() {
  if (bolum === 1 && GIZ.generator) {
    let m = document.querySelector('meta[name="generator"]');
    if (!m) {
      m = document.createElement("meta");
      m.name = "generator";
      document.head.appendChild(m);
    }
    m.content = GIZ.generator;
  }
  if (bolum === 2 && GIZ.raf) {
    let raf = $("#raf");
    if (!raf) {
      raf = document.createElementNS("http://www.w3.org/2000/svg", "svg");
      raf.id = "raf";
      raf.setAttribute("hidden", "");
      raf.setAttribute("aria-hidden", "true");
      const t = document.createElementNS("http://www.w3.org/2000/svg", "text");
      t.textContent = GIZ.raf;
      raf.appendChild(t);
      document.body.appendChild(raf);
    }
  }
  if (bolum === 4 && GIZ.m) {
    window._m = GIZ.m;
  }
}

function izBirak(hex) {
  try {
    localStorage.setItem("k", hex);
  } catch (_) {}
  try {
    sessionStorage.setItem("k", hex);
  } catch (_) {}
  try {
    document.cookie = "k=" + hex + ";path=/;SameSite=Lax";
  } catch (_) {}
}

function sahne3Ayar(iceri) {
  barakada = !!iceri;
  const st = STORY;
  const img = $("#odaImg");
  if (img && st) {
    img.src = barakada && st.altSahne ? st.altSahne.foto : st.foto;
  }
  const kaset = $("#n-kaset");
  const kutuN = $("#n-kutu");
  const tez = $("#n-menu");
  const kapi = $("#n-jenerator");
  if (kaset) {
    kaset.style.display = barakada ? "block" : "none";
    if (barakada) kaset.classList.add("nabiz");
  }
  if (kutuN) kutuN.style.display = barakada ? "block" : "none";
  if (tez) tez.style.display = barakada ? "none" : "block";
  if (kapi) kapi.textContent = barakada ? "kafe" : "arka kapı";
}

function noktaOzel(n, st) {
  if (bolum === 2 && n.id === "koridor" && GIZ.cerez) {
    const k = GIZ.cerez.map((c) => c.toString(16).padStart(2, "0")).join("");
    izBirak(k);
    if (!kesikYapildi) {
      kesikYapildi = true;
      elektrikKes(() => {
        konusma(GIZ.sonra || []);
      });
    }
    return;
  }
  if (bolum === 3 && n.id === "jenerator" && st.altSahne) {
    const iceri = !barakada;
    karart(() => {
      sahne3Ayar(iceri);
      sahneKutuAyar();
      if (iceri) konusma(GIZ.sonra || []);
    });
  }
}

function noktaKur() {
  barakada = false;
  const kat = $("#k-yakin");
  kat.innerHTML = "";
  const st = STORY;
  st.noktalar.forEach((n) => {
    const d = document.createElement("div");
    d.className = "nokta";
    d.id = "n-" + n.id;
    d.style.left = n.x;
    d.style.top = n.y;
    d.textContent = n.ad;
    if (n.gizli) d.style.display = "none";
    d.addEventListener("click", (e) => {
      e.stopPropagation();
      if (bolum === 3 && n.id === "jenerator") {
        if (!barakada && !bulunan["III-1"]) {
          konusma(
            GIZ.kilit || [
              {
                k: "",
                t: "Arka kapı kilitli. Önce tezgâhtaki izi panele mühürle.",
              },
            ]
          );
          return;
        }
        $("#vinyet").classList.remove("gorun");
        const soz = barakada
          ? GIZ.geri || [{ k: "", t: "Kafe. Tezgâh duruyor.", ic: true }]
          : n.konus;
        konusma(soz, () => noktaOzel(n, st));
        return;
      }
      d.classList.add("gitti");
      if (n.vinyet) vinyetGoster(n.vinyet, n.dosya);
      else $("#vinyet").classList.remove("gorun");
      konusma(n.konus, () => {
        if (n.dosya) {
          const a = document.createElement("a");
          a.href = n.dosya;
          a.download = "";
          a.target = "_blank";
          a.rel = "noopener";
          a.click();
        }
        noktaOzel(n, st);
      });
    });
    kat.appendChild(d);
  });
}

function odaGiris() {
  const st = STORY;
  $(".bolum-eti").textContent = st.etiket;
  const img = $("#odaImg");
  img.onload = () => sahneKutuAyar();
  img.src = st.foto;
  img.onerror = () => {
    img.style.display = "none";
    $("#odaFoto").style.background = "linear-gradient(180deg,#1a140e,#050302)";
  };
  noktaKur();
  sahneKutuAyar();
  sahneAc("#s-oda");
  konusma(st.giris);
}

function baslikKarti() {
  const st = STORY;
  const g = $(".gbaslik");
  g.setAttribute("data-t", st.baslik);
  g.textContent = st.baslik;
  $(".altbas").textContent = st.alt;
  karart(() => {
    sahneAc("#s-baslik");
    setTimeout(() => {
      karart(() => odaGiris());
    }, 1800);
  });
}

function karanlikGiris() {
  sahneAc("#s-karanlik");
  kutu.classList.add("acik");
  if (bolum > 1) {
    const kopru =
      (GIZ && GIZ.kopru) ||
      [
        { k: "", t: "Fener hâlâ sende. Daha derine.", ic: true },
      ];
    konusma(kopru, () => baslikKarti());
    return;
  }
  konusma(
    [
      { k: "", t: "...soğuk.", ic: true },
      { k: "", t: "Çamur. Tel. Bir yerde cızırdayan jeneratör.", ic: true },
      {
        k: "",
        t: "Gözlerini açıyorsun. Night Hatch arşivine gönderildin — Lara Lock’un mühürlediği park.",
      },
      { k: "", t: "Fenerin cebinde. Ekrana tıkla. İzleri topla." },
    ],
    () => baslikKarti()
  );
}

async function isaretDene() {
  const v = $("#flagIn").value.trim();
  const h = await sha(v);
  let ok = null;
  BOLUM_SLOTS.forEach((id) => {
    if (FLAGS[id] === h) ok = id;
  });
  if (!ok) {
    $("#girisHata").textContent = "işaret uymuyor";
    return;
  }
  bulunan[ok] = true;
  kaydet();
  slotCiz();
  $("#girisHata").textContent = ok + " alındı";
  $("#flagIn").value = "";
  if (bolumTam()) {
    $("#panel").classList.remove("acik");
    $("#girisHata").textContent = ok + " alındı";
    if (+bolum === 4 || ctfTam()) {
      bitisBaslat();
    } else {
      setTimeout(() => sonraki(), 700);
    }
    return;
  }
}

function sonraki() {
  karart(() => {
    sahneAc("#s-son");
    const kapanis = (GIZ && GIZ.kapanis) || "üç işaret mühürlendi";
    $(".buyuk").textContent = "Bölüm " + bolum + " mühürlendi";
    const not = $("#sonNot");
    if (not) not.textContent = kapanis;
    const a = $(".sonraki");
    a.style.display = "inline-block";
    a.href = "?b=" + (bolum + 1);
    a.textContent = "bölüm " + (bolum + 1) + " — devam";
  });
}

let laraSes = null;
let epilogBekliyor = false;
const EPILOG_V = "4";

function finalEkran() {
  epilogBekliyor = false;
  document.body.classList.add("bitti");
  localStorage.setItem("nh-bitti", "1");
  localStorage.setItem("nh-epilog-done", "1");
  localStorage.setItem("nh-epilog-v", EPILOG_V);
  kutu.classList.remove("acik");
  $("#panel").classList.remove("acik");
  vinyetGoster(null);
  sesKapat();
  if (laraSes) {
    try {
      laraSes.pause();
    } catch (_) {}
  }
  const p = $("#perde");
  if (p) p.style.opacity = "0";
  sahneAc("#s-final");
  $("#finalYazi").textContent =
    "Tebrikler. Bütün işaretler mühürlendi. Park kapandı. Ama unuttuğun bir şey var. Arşivler… İzler kalır, izler kalırsın.";
  $("#finalImza").textContent = "Created by Rahile Pelin Yakar";
  const tekrar = $("#finalLaraBtn");
  if (tekrar) {
    tekrar.onclick = (e) => {
      e.preventDefault();
      e.stopPropagation();
      localStorage.removeItem("nh-epilog-done");
      bitisBaslat();
    };
  }
}

function laraKaydiCal() {
  epilogBekliyor = false;
  const btn = $("#epilogBaslat");
  if (btn) btn.hidden = true;
  const durum = $("#epilogDurum");
  if (durum) durum.textContent = "kayıt dinleniyor…";

  if (laraSes) {
    try {
      laraSes.pause();
    } catch (_) {}
  }
  laraSes = new Audio("assets/lara_son.mp3?v=3");
  laraSes.volume = 1;
  laraSes.onended = () => {
    if (durum) durum.textContent = "kayıt bitti";
    setTimeout(() => karart(() => finalEkran()), 700);
  };
  laraSes.onerror = () => {
    if (durum) durum.textContent = "kayıt okunamadı";
    setTimeout(() => finalEkran(), 900);
  };
  const p = laraSes.play();
  if (p && p.catch) {
    p.catch(() => {
      epilogBekliyor = true;
      if (btn) btn.hidden = false;
      if (durum) durum.textContent = "ses engellendi — kaydı dinle";
    });
  }
}

function bitisBaslat() {
  localStorage.removeItem("nh-epilog-done");
  localStorage.setItem("nh-epilog-v", EPILOG_V);
  document.body.classList.add("bitti");
  kutu.classList.remove("acik");
  $("#panel").classList.remove("acik");
  vinyetGoster(null);
  sesKapat();
  const p = $("#perde");
  if (p) p.style.opacity = "0";
  sahneAc("#s-epilog");
  epilogBekliyor = true;
  const durum = $("#epilogDurum");
  if (durum) durum.textContent = "Lara Lock — son saha kaydı";
  const btn = $("#epilogBaslat");
  if (btn) {
    btn.hidden = false;
    btn.textContent = "kaydı dinle";
    btn.onclick = (e) => {
      e.preventDefault();
      e.stopPropagation();
      laraKaydiCal();
    };
  }
}

function olum() {
  bitisBaslat();
}

function cozPaket(pack, n) {
  const raw = Uint8Array.from(atob(pack), (c) => c.charCodeAt(0));
  const key = new TextEncoder().encode("nh" + n);
  const out = new Uint8Array(raw.length);
  for (let i = 0; i < raw.length; i++) out[i] = raw[i] ^ key[i % key.length];
  return JSON.parse(new TextDecoder().decode(out));
}

function yukleBolum(n) {
  return new Promise((resolve, reject) => {
    const s = document.createElement("script");
    s.src = "js/bolum/" + n + ".js?v=9";
    s.onload = () => {
      try {
        const data = cozPaket(window.__PACK, n);
        delete window.__PACK;
        STORY = data.story;
        FLAGS = data.flags;
        BOLUM_SLOTS = data.slots;
        GIZ = data.giz || {};
        resolve();
      } catch (err) {
        reject(err);
      }
    };
    s.onerror = () => reject(new Error("bolum yuklenemedi"));
    document.head.appendChild(s);
  });
}

async function baslat() {
  const istenenBolum = params.get("b");
  if (ctfTam() && !istenenBolum) {
    const p = $("#perde");
    if (p) p.style.opacity = "0";
    localStorage.removeItem("nh-bitti");
    bitisBaslat();
    return;
  }
  const max = acikBolum();
  if (bolum > max) {
    bolum = max;
    history.replaceState(null, "", "?b=" + bolum);
  }
  kaydet();
  try {
    await yukleBolum(bolum);
  } catch (e) {
    kutu.classList.add("acik");
    metinEl.textContent = "Bölüm paketi yüklenemedi. Sayfayı yenile.";
    return;
  }
  bolumHazirlik();
  slotCiz();
  const p = $("#perde");
  if (p) p.style.opacity = "0";
  if (+bolum === 4 && bolumTam()) {
    bitisBaslat();
    return;
  }
  karanlikGiris();
}

addEventListener("click", (e) => {
  if (epilogBekliyor) {
    laraKaydiCal();
    return;
  }
  if (
    e.target.closest(".nokta") ||
    e.target.closest("#sesBtn") ||
    e.target.closest("#isaretBtn") ||
    e.target.closest("#panel") ||
    e.target.closest("#vinyet") ||
    e.target.closest(".sonraki") ||
    e.target.closest("#epilogBaslat") ||
    e.target.closest("#finalLaraBtn")
  ) {
    return;
  }
  ilerle();
});

addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !$("#panel").classList.contains("acik")) ilerle();
});

addEventListener("resize", () => sahneKutuAyar());

addEventListener("mousemove", (e) => {
  document.documentElement.style.setProperty("--fx", e.clientX + "px");
  document.documentElement.style.setProperty("--fy", e.clientY + "px");
  const m = $("#imlec");
  if (m) {
    m.style.left = e.clientX + "px";
    m.style.top = e.clientY + "px";
  }
});

$("#sesBtn").addEventListener("click", (e) => {
  e.stopPropagation();
  if (muzikAcik) sesKapat(true);
  else sesAc(true);
});

$("#isaretBtn").addEventListener("click", (e) => {
  e.stopPropagation();
  $("#panel").classList.add("acik");
  $("#flagIn").focus();
});

$("#kapatPanel").addEventListener("click", () => $("#panel").classList.remove("acik"));
$("#flagForm").addEventListener("submit", (e) => {
  e.preventDefault();
  isaretDene();
});

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", baslat);
} else {
  baslat();
}
