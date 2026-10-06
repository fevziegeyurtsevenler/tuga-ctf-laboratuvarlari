import sqlite3

def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # Kullanıcılar tablosu
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    """)

    # Admin hesabı
    cursor.execute("SELECT * FROM users WHERE username = 'admin'")
    if not cursor.fetchone():
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            ("admin", "S1b3r_K0m1t3_TUG4_0987654321!")
        )
        conn.commit()

    conn.close()

if __name__ == "__main__":
    init_db()