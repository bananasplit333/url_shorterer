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
    original_url = request.form['url']
    print(f'url inserted: {original_url}')
    short_code = generate_short_code()

    with db_lock:
        conn = create_connection()
        result = get_url(conn, original_url)
        if result:
            return "URL already exists", 403
        else:
            insert_url(conn, original_url, short_code)

    short_url = 'https://jaehyon.ca/' + short_code
    print("short url inserted")
    return short_url

@app.route('/<short_code>', methods=['GET'])
def redirect_url(short_code):
    with db_lock:
        conn = create_connection()
        result = get_url(conn, short_code)
        if result:
            original_url, click_count = result
            if click_count >= MAX_CLICKS:
                return "URL has expired", 404
            update_click_count(conn, short_code)
            return redirect(original_url)
        else:
            return "URL not found", 404

if __name__ == '__main__':
    conn = create_connection()
    create_table(conn)
    app.run()