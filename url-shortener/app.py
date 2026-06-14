import random
import string
from flask import Flask, request, jsonify, redirect, render_template
from database import init_db, save_url, get_long_url, increment_clicks

app = Flask(__name__)
init_db()

def generate_short_code(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=length))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/shorten', methods=['POST'])
def shorten():
    data = request.get_json()
    long_url = data.get('url', '').strip()

    if not long_url:
        return jsonify({'error': 'URL is required'}), 400

    if not long_url.startswith(('http://', 'https://')):
        long_url = 'https://' + long_url

    short_code = generate_short_code()
    while get_long_url(short_code):
        short_code = generate_short_code()

    save_url(short_code, long_url)

    short_url = request.host_url + short_code
    return jsonify({'short_url': short_url, 'short_code': short_code}), 201

@app.route('/<short_code>')
def redirect_to_url(short_code):
    long_url = get_long_url(short_code)
    if long_url is None:
        return jsonify({'error': 'Short URL not found'}), 404
    increment_clicks(short_code)
    return redirect(long_url, code=302)

if __name__ == '__main__':
    app.run(debug=True)