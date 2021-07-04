from dungen.dungen import generate, HTMLRenderer
from flask import Flask, send_file
from pathlib import Path

app = Flask(__name__)


@app.route('/')
def index():
    dungeon = generate()
    return HTMLRenderer(dungeon).render()


@app.route('/duck')
def kanji():
    image = Path('./static/kanji.png')
    return send_file(image, mimetype='image/png')


if __name__ == '__main__':
    app.run(debug=True)