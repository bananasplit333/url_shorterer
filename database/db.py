import sqlite3

def create_connection():
    conn = sqlite3.connect('urls.db')
    return conn

def create_table(conn):
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS urls
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 original_url TEXT NOT NULL,
                 short_code TEXT NOT NULL,
                 click_count INTEGER DEFAULT 0)''')
    conn.commit()

def insert_url(conn, original_url, short_code):
    c = conn.cursor()
    c.execute("INSERT INTO urls (original_url, short_code) VALUES (?, ?)", (original_url, short_code))
    conn.commit()

def get_url(conn, short_code):
    cur = conn.cursor()
    cur.execute("SELECT original_url, click_count FROM urls WHERE short_code=?", (short_code,))
    result = cur.fetchone()
    conn.close()
    return result

def update_click_count(conn, short_code):
    c = conn.cursor()
    c.execute("UPDATE urls SET click_count = click_count + 1 WHERE short_code = ?", (short_code,))
    conn.commit()