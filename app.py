from urllib.parse import urljoin
from flask import Flask, request, redirect 
from flask_cors import CORS
from threading import Lock
from database.db import create_connection, create_table, insert_url, get_url, update_click_count
from utils.url_shortener import generate_short_code

app = Flask(__name__)
CORS(app)
MAX_CLICKS = 3000
db_lock = Lock()

@app.route('/')
def home():
    return

@app.route('/shorten_link', methods=['POST'])
def shorten_url():
    print("POST REQUEST")
    original_url = request.form.get('url')
    if not original_url:
        return "Missing URL parameter", 400
    print(f'url inserted: {original_url}')
    short_code = generate_short_code()
    with db_lock:
        conn = create_connection()
        result = get_url(conn, original_url)
        if result:
            conn.close()
            return "URL already exists", 409
        else:
            insert_url(conn, original_url, short_code)
            conn.close()
    short_url = urljoin(request.host_url, short_code)
    print("short url inserted")
    return short_url


@app.route('/<short_code>', methods=['GET'])
def redirect_url(short_code):
    print('GET REQUEST')
    with db_lock:
        conn = create_connection()
        result = get_url(conn, short_code=short_code)
        if result:
            original_url, click_count = result
            if click_count >= MAX_CLICKS:
                conn.close()
                return "URL has expired", 404
            update_click_count(conn, short_code)
            conn.close()
            return redirect(original_url)
        else:
            conn.close()
            return "URL not found", 404

if __name__ == '__main__':
    conn = create_connection()
    create_table(conn)
    app.run()