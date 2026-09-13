import os
import sqlite3
import time
import threading
from collections import defaultdict, deque

from flask import Flask, request, session, redirect, url_for, render_template, g, abort
from werkzeug.security import check_password_hash

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "son-vardiya-dev-secret")
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
)

DB_PATH = os.environ.get("DB_PATH", "/data/lab.db")

# ---- Hafif, bellek-içi rate limiting -------------------------------------
# Amaç: /login ve /archive/<code> üzerinde otomatik, hızlı ardışık denemeleri
# pratik olmaktan çıkarmak. KALICI KİLİT YOKTUR: pencere süresi dolunca
# istekler kendiliğinden serbest kalır; normal bir kullanıcının birkaç
# manuel denemesi asla engellenmez. Tek instance/tek proses için yeterlidir;
# çok-worker'lı bir dağıtımda paylaşılan bir store (ör. Redis) gerekir.
_rate_limit_lock = threading.Lock()
_rate_limit_buckets = defaultdict(deque)


def _client_ip():
    # Lab, reverse proxy arkasında koşmadığı için X-Forwarded-For gibi
    # sahteye açık başlıklara güvenilmez; doğrudan bağlantı IP'si kullanılır.
    return request.remote_addr or "unknown"


def rate_limited(bucket, max_requests, window_seconds):
    """Sliding-window rate limiter. Limit aşılmışsa kalan bekleme saniyesini
    (int) döner; aşılmamışsa None döner ve isteği sayaca ekler."""
    key = (bucket, _client_ip())
    now = time.monotonic()
    with _rate_limit_lock:
        q = _rate_limit_buckets[key]
        while q and now - q[0] > window_seconds:
            q.popleft()
        if len(q) >= max_requests:
            retry_after = max(1, int(window_seconds - (now - q[0])))
            return retry_after
        q.append(now)
        return None


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(exception=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db_if_needed():
    """Lab veritabanını ilk çalıştırmada hazırlar; eksik temel tablo varsa
    eski/stale Docker volume durumunda da şemayı yeniden kurar."""
    conn = sqlite3.connect(DB_PATH)
    required_tables = {
        "users", "employees", "employee_profiles", "documents",
        "announcements", "archive_records", "support_tickets",
    }
    existing_tables = {
        row[0] for row in conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        ).fetchall()
    }
    need_init = not os.path.exists(DB_PATH) or not required_tables.issubset(existing_tables)
    if need_init:
        init_sql_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "init.sql")
        with open(init_sql_path, "r", encoding="utf-8") as f:
            conn.executescript(f.read())
        conn.commit()
    conn.close()


def login_required(view):
    from functools import wraps

    @wraps(view)
    def wrapped(*args, **kwargs):
        if "username" not in session:
            return redirect(url_for("login"))
        return view(*args, **kwargs)

    return wrapped


@app.route("/")
def index():
    if "username" in session:
        return redirect(url_for("portal"))
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        # Login brute-force koruması: aynı IP'den kısa sürede çok fazla
        # POST denemesi 429 ile geçici olarak yavaşlatılır. Kalıcı kilit yok.
        retry_after = rate_limited("login", max_requests=8, window_seconds=60)
        if retry_after is not None:
            error = f"Çok fazla deneme yapıldı. Lütfen {retry_after} saniye sonra tekrar deneyin."
            return render_template("login.html", error=error), 429

        username = request.form.get("username", "")
        password = request.form.get("password", "")

        # Login parametrize sorgu kullanır - bilerek zafiyetsiz bırakıldı.
        # Şifreler veritabanında pbkdf2:sha256 ile hash'lenmiş olarak tutulur
        # (bkz. database/init.sql); düz metin karşılaştırma yapılmaz.
        db = get_db()
        cur = db.execute(
            "SELECT * FROM users WHERE username = ?",
            (username,),
        )
        user = cur.fetchone()

        if user and check_password_hash(user["password_hash"], password):
            session["username"] = user["username"]
            session["display_name"] = user["display_name"]
            return redirect(url_for("portal"))
        error = "Kullanıcı adı veya şifre hatalı."

    return render_template("login.html", error=error)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/portal")
@login_required
def portal():
    db = get_db()
    cur = db.execute(
        "SELECT title, body, posted_by, posted_at FROM announcements ORDER BY posted_at DESC LIMIT 3"
    )
    announcements = cur.fetchall()

    # "Son Erişilen Kaynaklar" artık oturum sahibinin KENDİ dokümanlarından
    # dinamik olarak çekilir (parametrize sorgu). Önceden burada başka bir
    # kullanıcıya (mehmet.kaya) ait doküman ID'leri sabit kodlanmıştı; bu,
    # oyuncu SQLi/4471 ipucunu bulmadan önce IDOR'un varlığını tesadüfen
    # keşfetmesine yol açabiliyordu. Artık her kullanıcı yalnızca kendi
    # dokümanlarını görür, IDOR yalnızca 4471 numarası bilerek denendiğinde
    # ortaya çıkar.
    cur2 = db.execute(
        "SELECT id, title FROM documents WHERE owner_username = ? ORDER BY id DESC LIMIT 3",
        (session["username"],),
    )
    recent_docs = cur2.fetchall()

    # BT destek özet bilgisi: yalnızca sayaç, tek tek talepler burada gösterilmez.
    open_tickets = db.execute(
        "SELECT COUNT(*) AS c FROM support_tickets WHERE status != 'Kapalı'"
    ).fetchone()["c"]

    # Hesap bilgisi özeti için profil bilgisi (varsa)
    profile = db.execute(
        """
        SELECT e.role, ep.department, ep.status
        FROM employee_profiles ep
        JOIN employees e ON e.id = ep.employee_id
        WHERE ep.username = ?
        """,
        (session["username"],),
    ).fetchone()

    return render_template(
        "portal.html",
        display_name=session.get("display_name"),
        announcements=announcements,
        recent_docs=recent_docs,
        open_tickets=open_tickets,
        profile=profile,
    )


@app.route("/system")
@login_required
def system_status():
    """
    Sistem durumu sayfası.

    Tamamen dekoratif/statik bir bilgi paneli - dinamik girdi almaz, herhangi
    bir veritabanı sorgusu çalıştırmaz. Portalın gerçekçi hissini güçlendirmek
    için eklenmiştir.
    """
    return render_template("system.html")


@app.route("/search")
@login_required
def search():
    """
    Personel Ara.

    KASITLI ZAFIYET: 'name' parametresi doğrudan SQL sorgusuna string
    birleştirme (string concatenation) ile ekleniyor. Bu, union-based
    SQL Injection'a izin verir.

    Uygulama normalde sadece id, name, role sütunlarını listeler.
    'note' sütunu arayüzde hiç gösterilmez; yalnızca UNION SELECT ile
    sorguya eklenerek görüntülenebilir.
    """
    name = request.args.get("name", "")
    results = []
    error = None

    if name:
        db = get_db()
        query = (
            "SELECT id, name, role FROM employees "
            "WHERE name LIKE '%" + name + "%'"
        )
        try:
            cur = db.execute(query)
            results = cur.fetchall()
        except sqlite3.Error as e:
            error = str(e)

    return render_template("search.html", results=results, name=name, error=error)


@app.route("/employee/<int:employee_id>")
@login_required
def employee_profile(employee_id):
    """
    Personel profil sayfası (salt okunur, parametrize).

    'note' alanı KESİNLİKLE burada render edilmez - yalnızca /search
    üzerindeki SQL Injection ile ulaşılabilir. Bu endpoint sahiplik/erişim
    açısından herhangi bir zafiyet içermez; herhangi bir çalışanın herkese
    açık kurumsal profil bilgisi görüntülenebilir (gerçek şirket
    dizinlerindeki gibi).
    """
    db = get_db()
    employee = db.execute(
        "SELECT id, name, role FROM employees WHERE id = ?",
        (employee_id,),
    ).fetchone()
    if employee is None:
        abort(404)

    profile = db.execute(
        "SELECT department, internal_ext, email, status FROM employee_profiles WHERE employee_id = ?",
        (employee_id,),
    ).fetchone()

    return render_template("employee_profile.html", employee=employee, profile=profile)


@app.route("/profile")
@login_required
def my_profile():
    """Giriş yapan kullanıcının kendi profili. Salt okunur; başka bir
    kullanıcının bilgisi asla gösterilmez (sorgu her zaman oturumdaki
    username ile parametrize edilir)."""
    db = get_db()
    row = db.execute(
        """
        SELECT e.name, e.role, ep.department, ep.internal_ext, ep.email, ep.status, ep.username
        FROM employee_profiles ep
        JOIN employees e ON e.id = ep.employee_id
        WHERE ep.username = ?
        """,
        (session["username"],),
    ).fetchone()
    return render_template("profile.html", row=row)


@app.route("/announcements")
@login_required
def announcements_list():
    """Tüm duyuruların genişletilmiş listesi. İsteğe bağlı kategori filtresi
    beyaz listeye karşı doğrulanır; serbest metin SQL'e eklenmez."""
    db = get_db()
    categories = [r["category"] for r in db.execute(
        "SELECT DISTINCT category FROM announcements ORDER BY category"
    ).fetchall()]

    selected = request.args.get("category", "")
    if selected and selected in categories:
        rows = db.execute(
            "SELECT title, body, category, posted_by, posted_at FROM announcements "
            "WHERE category = ? ORDER BY posted_at DESC",
            (selected,),
        ).fetchall()
    else:
        selected = ""
        rows = db.execute(
            "SELECT title, body, category, posted_by, posted_at FROM announcements "
            "ORDER BY posted_at DESC"
        ).fetchall()

    return render_template(
        "announcements.html", announcements=rows, categories=categories, selected=selected
    )


@app.route("/support")
@login_required
def support_list():
    """IT Destek bilet listesi. Durum filtresi beyaz listeye karşı
    doğrulanır (Açık / İşlemde / Kapalı)."""
    db = get_db()
    valid_statuses = {"Açık", "İşlemde", "Kapalı"}
    selected = request.args.get("status", "")

    if selected in valid_statuses:
        tickets = db.execute(
            "SELECT ticket_no, requester_name, subject, priority, status, opened_at, updated_at "
            "FROM support_tickets WHERE status = ? ORDER BY opened_at DESC",
            (selected,),
        ).fetchall()
    else:
        selected = ""
        tickets = db.execute(
            "SELECT ticket_no, requester_name, subject, priority, status, opened_at, updated_at "
            "FROM support_tickets ORDER BY opened_at DESC"
        ).fetchall()

    return render_template(
        "support.html", tickets=tickets, selected=selected, valid_statuses=sorted(valid_statuses)
    )


@app.route("/support/<ticket_no>")
@login_required
def support_detail(ticket_no):
    db = get_db()
    ticket = db.execute(
        "SELECT * FROM support_tickets WHERE ticket_no = ?",
        (ticket_no,),
    ).fetchone()
    if ticket is None:
        abort(404)
    return render_template("support_detail.html", ticket=ticket)


@app.route("/documents")
@login_required
def documents():
    """Kullanıcının kendi dokümanlarının listesi (parametrize, zafiyetsiz)."""
    db = get_db()
    docs = db.execute(
        "SELECT id, title, category, status, updated_at FROM documents "
        "WHERE owner_username = ? ORDER BY id DESC",
        (session["username"],),
    ).fetchall()
    return render_template("documents.html", docs=docs)


@app.route("/documents/view")
@login_required
def document_view():
    """
    Doküman görüntüleme.

    KASITLI ZAFIYET (IDOR): Endpoint sadece oturum açık mı diye bakıyor,
    görüntülenen dokümanın gerçekten oturum sahibine ait olup olmadığını
    KONTROL ETMİYOR. Bu yüzden 'id' parametresi değiştirilerek başka
    kullanıcılara (örn. sistem hesabına) ait dokümanlara erişilebilir.
    """
    doc_id = request.args.get("id", type=int)
    if doc_id is None:
        return render_template("document_view.html", doc=None, error="Geçersiz doküman ID.")

    db = get_db()
    cur = db.execute("SELECT * FROM documents WHERE id = ?", (doc_id,))
    doc = cur.fetchone()

    if doc is None:
        return render_template("document_view.html", doc=None, error="Doküman bulunamadı.")

    return render_template("document_view.html", doc=doc, error=None)


@app.route("/archive/<code>")
@login_required
def archive_record(code):
    """
    Ek kayıt görüntüleme (kod ile erişim).

    Bu endpoint navbar'da veya herhangi bir listede yer almaz; yalnızca ilgili
    kodu (örn. bir belge/zarf üzerinde görülen referans numarasını) bilen bir
    kullanıcı tarafından doğrudan URL ile erişilebilir. Erişim kontrolü burada
    da nesne bazlı bir yetkilendirmeye dayanmaz - kod bilindiği an kayıt açılır.

    Archive brute-force koruması: aynı IP'den kısa sürede çok sayıda farklı
    kod denemesi 429 ile geçici olarak yavaşlatılır (kalıcı kilit yok).
    """
    retry_after = rate_limited("archive", max_requests=6, window_seconds=15)
    if retry_after is not None:
        return render_template(
            "archive_record.html",
            record=None,
            error=f"Çok fazla deneme yapıldı. Lütfen {retry_after} saniye sonra tekrar deneyin.",
        ), 429

    db = get_db()
    cur = db.execute("SELECT * FROM archive_records WHERE code = ?", (code,))
    record = cur.fetchone()

    if record is None:
        return render_template("archive_record.html", record=None, error="Kayıt bulunamadı.")

    return render_template("archive_record.html", record=record, error=None)


# Veritabanı, modül her yüklendiğinde (doğrudan `python app.py` ile de,
# ileride bir WSGI sunucusu - gunicorn vb. - ile de) hazır olacak şekilde
# burada başlatılır; sadece __main__ bloğuna bağlı bırakılmaz.
init_db_if_needed()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
