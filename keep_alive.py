from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "QR Vault bot is alive!"