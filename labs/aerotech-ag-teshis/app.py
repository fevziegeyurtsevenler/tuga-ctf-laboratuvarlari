import subprocess
from flask import Flask, request, make_response, render_template_string

app = Flask(__name__)

FLAG1 = "TUGA{c00k1e_m4n1pul4s1y0nu_v3_y3tk1_yuk53ltm3}"

PAGE_TEMPLATE = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AeroTech Savunma // Ağ Teşhis ve Operasyon Portalı</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        @keyframes pulse-slow {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.35; }
        }
        .pulse-light { animation: pulse-slow 1.8s ease-in-out infinite; }
        .grid-pattern {
            background-size: 24px 24px;
            background-image: linear-gradient(to right, rgba(255, 255, 255, 0.03) 1px, transparent 1px),
                              linear-gradient(to bottom, rgba(255, 255, 255, 0.03) 1px, transparent 1px);
        }
    </style>
</head>
<body class="bg-slate-950 text-slate-100 font-sans min-h-screen flex flex-col justify-between grid-pattern">

    <!-- Üst Kontrol Çubuğu -->
    <header class="border-b border-slate-800/80 bg-slate-900/80 backdrop-blur-md px-6 py-4 flex items-center justify-between sticky top-0 z-50">
        <div class="flex items-center space-x-3">
            <div class="w-10 h-10 rounded-xl bg-gradient-to-tr from-cyan-600 to-blue-500 flex items-center justify-center text-white font-bold shadow-lg shadow-cyan-500/20">
                <i class="fa-solid fa-satellite-dish text-lg"></i>
            </div>
            <div>
                <div class="flex items-center space-x-2">
                    <h1 class="text-sm font-bold tracking-wider uppercase text-slate-100">AEROTECH DEFENSE SYSTEMS</h1>
                    <span class="text-[10px] font-mono bg-cyan-950 text-cyan-400 border border-cyan-800/60 px-1.5 py-0.5 rounded">NET-SEC v2.6</span>
                </div>
                <p class="text-xs text-slate-400">Merkezi Altyapı & Ağ Teşhis Konsolu</p>
            </div>
        </div>

        <div class="flex items-center space-x-4">
            <div class="hidden sm:flex items-center space-x-2 text-xs font-mono text-slate-400">
                <span class="w-2 h-2 rounded-full bg-emerald-400 pulse-light"></span>
                <span>GATEWAY: 10.14.0.1</span>
            </div>
            <div class="flex items-center space-x-2 text-xs bg-slate-900 px-3 py-1.5 rounded-lg border border-slate-700">
                <span class="w-2 h-2 rounded-full {{ 'bg-emerald-500 shadow-sm shadow-emerald-400' if is_admin else 'bg-rose-500 shadow-sm shadow-rose-400' }}"></span>
                <span class="text-slate-400 font-mono">ROL:</span>
                <span class="font-bold font-mono {{ 'text-emerald-400' if is_admin else 'text-rose-400' }} uppercase">{{ current_role }}</span>
            </div>
        </div>
    </header>

    <!-- Ana Çalışma Alanı -->
    <main class="flex-1 max-w-5xl w-full mx-auto p-6 space-y-6">

        <!-- Durum ve Metrik Kartları -->
        <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div class="bg-slate-900/60 border border-slate-800 p-4 rounded-xl shadow-sm">
                <p class="text-xs text-slate-400 font-mono">DÜĞÜM DURUMU</p>
                <div class="flex items-center justify-between mt-2">
                    <span class="text-sm font-semibold text-slate-200">Çevrimiçi / Hazır</span>
                    <i class="fa-solid fa-server text-cyan-400 text-sm"></i>
                </div>
            </div>
            <div class="bg-slate-900/60 border border-slate-800 p-4 rounded-xl shadow-sm">
                <p class="text-xs text-slate-400 font-mono">PROTOKOL KATMANI</p>
                <div class="flex items-center justify-between mt-2">
                    <span class="text-sm font-semibold text-slate-200">ICMP Echo v4</span>
                    <i class="fa-solid fa-network-wired text-indigo-400 text-sm"></i>
                </div>
            </div>
            <div class="bg-slate-900/60 border border-slate-800 p-4 rounded-xl shadow-sm">
                <p class="text-xs text-slate-400 font-mono">GECİKME ORTALAMASI</p>
                <div class="flex items-center justify-between mt-2">
                    <span class="text-sm font-semibold text-slate-200">0.42 ms</span>
                    <i class="fa-solid fa-bolt text-amber-400 text-sm"></i>
                </div>
            </div>
            <div class="bg-slate-900/60 border border-slate-800 p-4 rounded-xl shadow-sm">
                <p class="text-xs text-slate-400 font-mono">ERİŞİM SEVİYESİ</p>
                <div class="flex items-center justify-between mt-2">
                    <span class="text-sm font-semibold font-mono {{ 'text-emerald-400' if is_admin else 'text-rose-400' }}">
                        {{ 'ROOT_ADMIN' if is_admin else 'GUEST_RESTRICTED' }}
                    </span>
                    <i class="fa-solid {{ 'fa-unlock text-emerald-400' if is_admin else 'fa-lock text-rose-400' }} text-sm"></i>
                </div>
            </div>
        </div>

        {% if not is_admin %}
        <!-- Yetkisiz Ziyaretçi Paneli -->
        <div class="bg-slate-900/80 border border-rose-900/40 rounded-2xl p-8 text-center space-y-4 shadow-2xl relative overflow-hidden">
            <div class="absolute -top-10 -right-10 w-40 h-40 bg-rose-500/10 rounded-full blur-3xl pointer-events-none"></div>
            
            <div class="w-16 h-16 bg-rose-950/60 border border-rose-800/80 text-rose-400 rounded-2xl flex items-center justify-center mx-auto text-2xl shadow-xl shadow-rose-950/40">
                <i class="fa-solid fa-shield-halved"></i>
            </div>
            
            <div class="space-y-1">
                <h2 class="text-base font-bold text-slate-100 tracking-wide">YETKİSİZ ERİŞİM TESPİT EDİLDİ</h2>
                <p class="text-xs text-slate-400 max-w-md mx-auto leading-relaxed">
                    Ağ kontrol modülü yalnızca onaylanmış operasyonel roller için aktiftir. Oturum kimliğiniz sistem tarafından doğrulanmadı.
                </p>
            </div>

            <div class="inline-flex items-center space-x-2 bg-slate-950 border border-slate-800 rounded-lg px-4 py-2 text-xs text-slate-400 font-mono">
                <span class="text-slate-500">Mevcut Çerez:</span>
                <code class="text-rose-400 font-semibold">role={{ current_role }}</code>
            </div>
        </div>

        {% else %}
        <!-- Yetkili Yönetici Paneli -->
        <div class="space-y-6">

            <!-- FLAG 1 Paneli -->
            <div class="bg-emerald-950/30 border border-emerald-800/60 rounded-xl p-5 flex flex-col sm:flex-row sm:items-center justify-between gap-4 shadow-lg shadow-emerald-950/20">
                <div class="flex items-center space-x-3">
                    <div class="w-10 h-10 bg-emerald-900/40 text-emerald-400 rounded-lg border border-emerald-700/60 flex items-center justify-center flex-shrink-0">
                        <i class="fa-solid fa-flag-checkered text-base"></i>
                    </div>
                    <div>
                        <p class="text-[11px] font-mono uppercase tracking-wider text-emerald-300">Aşama 1 Başarılı // Yetki Belirteci Yakalandı</p>
                        <p class="font-mono text-sm font-bold text-emerald-200 select-all mt-0.5">{{ flag1 }}</p>
                    </div>
                </div>
                <span class="text-[11px] font-mono bg-emerald-900/50 text-emerald-300 border border-emerald-700/80 px-2.5 py-1 rounded w-fit">PRIVILEGE_ELEVATED</span>
            </div>

            <!-- Ping Test Konsolu -->
            <div class="bg-slate-900/90 border border-slate-800 rounded-xl p-6 shadow-xl space-y-4">
                <div class="flex items-center justify-between border-b border-slate-800 pb-3">
                    <div>
                        <h2 class="text-xs font-bold text-slate-200 uppercase tracking-wider">Ağ Teşhis Alt Sistemi (ICMP Diagnostics)</h2>
                        <p class="text-xs text-slate-400 mt-0.5">Sistem komut satırı üzerinden soket düzeyinde ping paketi iletir.</p>
                    </div>
                    <span class="text-[10px] font-mono bg-slate-800 text-slate-300 px-2 py-0.5 rounded">SUBNET: 127.0.0.0/8</span>
                </div>

                <form method="POST" class="flex flex-col sm:flex-row gap-3">
                    <div class="relative flex-1">
                        <i class="fa-solid fa-terminal absolute left-4 top-3.5 text-slate-500 text-xs"></i>
                        <input type="text" name="ip" value="{{ ip_input }}" placeholder="Hedef IP veya Hostname (Örn: 127.0.0.1)" required autocomplete="off"
                               class="w-full bg-slate-950 border border-slate-800 focus:border-cyan-500 focus:ring-1 focus:ring-cyan-500 rounded-lg pl-10 pr-4 py-2.5 text-xs text-cyan-300 font-mono outline-none transition">
                    </div>
                    <button type="submit" 
                            class="bg-gradient-to-r from-cyan-600 to-blue-600 hover:from-cyan-500 hover:to-blue-500 text-white text-xs font-semibold px-6 py-2.5 rounded-lg flex items-center justify-center space-x-2 transition shadow-md shadow-cyan-600/20">
                        <i class="fa-solid fa-bolt text-xs"></i>
                        <span>Teşhisi Başlat</span>
                    </button>
                </form>
            </div>

            <!-- Terminal Çıktısı Penceresi -->
            {% if output %}
            <div class="bg-slate-950 border border-slate-800 rounded-xl overflow-hidden shadow-2xl">
                <div class="bg-slate-900/90 px-4 py-2 border-b border-slate-800 flex items-center justify-between">
                    <div class="flex items-center space-x-2">
                        <div class="w-2.5 h-2.5 rounded-full bg-rose-500"></div>
                        <div class="w-2.5 h-2.5 rounded-full bg-amber-500"></div>
                        <div class="w-2.5 h-2.5 rounded-full bg-emerald-500"></div>
                        <span class="text-[11px] font-mono text-slate-400 ml-2">sys-diag@aerotech-gateway:~$</span>
                    </div>
                    <span class="text-[10px] font-mono text-slate-500">PROCESS_COMPLETED</span>
                </div>
                <pre class="p-5 font-mono text-xs text-emerald-400 whitespace-pre-wrap overflow-x-auto leading-relaxed">{{ output }}</pre>
            </div>
            {% endif %}

        </div>
        {% endif %}

    </main>

    <!-- Alt Bilgi -->
    <footer class="border-t border-slate-900 bg-slate-950/80 px-6 py-4 text-center text-xs text-slate-500 font-mono">
        AEROTECH DEFENSE INFRASTRUCTURE // SİBER GÜVENLİK KOMİTESİ LAB ÇALIŞMASI &copy; 2026
    </footer>

</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    user_role = request.cookies.get('role')
    
    if not user_role:
        resp = make_response(render_template_string(PAGE_TEMPLATE, is_admin=False, current_role='guest'))
        resp.set_cookie('role', 'guest')
        return resp

    is_admin = (user_role == 'admin')
    output = ""
    ip_input = ""

    if is_admin and request.method == 'POST':
        ip_input = request.form.get('ip', '')
        if ip_input:
            try:
                cmd = f"ping -c 1 {ip_input}"
                output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, timeout=5).decode('utf-8')
            except subprocess.CalledProcessError as e:
                output = e.output.decode('utf-8')
            except Exception as e:
                output = str(e)

    resp = make_response(render_template_string(
        PAGE_TEMPLATE,
        is_admin=is_admin,
        current_role=user_role,
        flag1=FLAG1 if is_admin else "",
        output=output,
        ip_input=ip_input
    ))
    return resp

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
