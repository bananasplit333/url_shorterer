from flask import Flask, request, redirect
from threading import Lock
from database import create_connection, create_table, insert_url, get_url, update_click_count
from url_shortener import generate_short_code

app = Flask(__name__)
MAX_CLICKS = 3000
db_lock = Lock()

@app.route('/shorten_link', methods=['POST'])
def shorten_url():
    original_url = request.form['url']
    short_code = generate_short_code()
    with db_lock:
        conn = create_connection()
        insert_url(conn, original_url, short_code)
    short_url = request.host_url + short_code
    return short_url

@app.route('/<short_code>')
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