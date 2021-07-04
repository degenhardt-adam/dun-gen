from dungen.dungen import generate, HTMLRenderer
from flask import Flask, render_template, send_file
from pathlib import Path

app = Flask(__name__)


@app.route('/')
def index():
    dungeon = generate()
    dungeon_render = HTMLRenderer(dungeon).render()
    return render_template('main.html', dungeon_render=dungeon_render)


@app.route('/duck')
def kanji():
    image = Path('./static/kanji.png')
    return send_file(image, mimetype='image/png')


if __name__ == '__main__':
    app.run(debug=True)