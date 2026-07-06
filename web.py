from flask import Flask, render_template, abort
from database import get_page

app = Flask(__name__)


@app.route("/")
def home():
    return """
    <h1>QR Vault v2 🚀</h1>
    <p>Server is running successfully.</p>
    <p>Open a memory page using <code>/page/&lt;id&gt;</code></p>
    """


@app.route("/page/<page_id>")
def page(page_id):
    try:
        data = get_page(page_id)

        if not data:
            abort(404)

        receiver = data.get("receiver")
        sender = data.get("sender")
        title = data.get("title")
        message = data.get("message")
        image_url = data.get("image")
        music_url = data.get("music")
        theme = data.get("theme")
        qr_url = data.get("qr")

        return render_template(
            "page.html",
            receiver=receiver,
            sender=sender,
            title=title,
            message=message,
            image_url=image_url,
            music_url=music_url,
            theme=theme,
            qr_url=qr_url,
        )

    except Exception as e:
        print("PAGE ERROR:", repr(e))
        abort(500)


if __name__ == "__main__":
    app.run(debug=True)