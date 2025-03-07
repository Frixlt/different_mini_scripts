from pathlib import Path

from flask import (Flask, Response, redirect, render_template, request,
                   send_file)

app = Flask(__name__)


@app.route("/", methods=["GET"])
def download():
    return send_file(Path(__file__), as_attachment=True)


if __name__ == "__main__":
    # app.debug = True
    # app.config['SECRET_KEY'] = 'secret!'
    app.config["HOST"] = "0.0.0.0"
    app.config["PORT"] = 5000
    # app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
    # app.run(host='0.0.0.0',debug=True)
    app.run()
