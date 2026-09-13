from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from init_db import init_db


app = Flask(__name__)
app.secret_key = "tuga_super_secret_key_change_me"


# Giriş Rotası (SQL Injection Zafiyetli Alan)
@app.route("/", methods=["GET", "POST"])
@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        
        # Zafiyet: Girdi parametrik yerine doğrudan sorguya formatlanıyor
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        
        try:
            cursor.execute(query)
            user = cursor.fetchone()
            if user:
                session["logged_in"] = True
                session["username"] = user[1]
                conn.close()
                return redirect(url_for("dashboard"))
            else:
                error = "Geçersiz kullanıcı adı veya parola."
        except sqlite3.OperationalError:
            error = "Veritabanı sorgu hatası oluştu."
            
        conn.close()
        
    return render_template("login.html", error=error)

# Dahili Panel Rotası
@app.route("/dashboard")
def dashboard():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    return render_template("dashboard.html", username=session.get("username"))

# Çıkış Rotası
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=8080, debug=True)