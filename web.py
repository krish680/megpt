<<<<<<< HEAD
from flask import Flask, render_template, abort
from database import get_page

app = Flask(__name__)


@app.route("/")
def home():
    return """
    <h1>QR Vault v2</h1>
    <p>The server is running successfully.</p>
    """


@app.route("/page/<page_id>")
def page(page_id):
    try:
        data = get_page(page_id)

        if not data:
            abort(404)

        return render_template(
            "page.html",
            receiver=data["receiver"],
            sender=data["sender"],
            title=data["title"],
            message=data["message"],
            image_url=data["image"],
            music_url=data.get("music")
        )

    except Exception as e:
        print(e)
=======
from flask import Flask, render_template, abort
from database import get_page

app = Flask(__name__)


@app.route("/")
def home():
    return """
    <h1>QR Vault v2</h1>
    <p>The server is running successfully.</p>
    """


@app.route("/page/<page_id>")
def page(page_id):
    try:
        data = get_page(page_id)

        if not data:
            abort(404)

        return render_template(
            "page.html",
            receiver=data["receiver"],
            sender=data["sender"],
            title=data["title"],
            message=data["message"],
            image_url=data["image"],
            music_url=data.get("music")
        )

    except Exception as e:
        print(e)
>>>>>>> e25fd19efe1b9ce37d47aa9f9c0c7ef17e8eb413
        abort(500)