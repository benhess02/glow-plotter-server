import os
from flask import Flask, request
from urllib.parse import urlencode
from dotenv import load_dotenv
import requests

load_dotenv()

RC_AUTH_URL = "https://www.recurse.com/oauth/authorize"
RC_TOKEN_URL = "https://www.recurse.com/oauth/token"
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")

app = Flask(__name__, static_folder="static", static_url_path="")

@app.route("/")
def index_route():
    return app.send_static_file("index.html")

@app.route("/login")
def login():
    return app.redirect(f"{RC_AUTH_URL}?{urlencode({
        "response_type": "code",
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
    })}")

@app.route("/rcredirect")
def rcredirect():
    code = request.args.get("code")
    if code is not None:
        try:
            res = requests.get(RC_TOKEN_URL, params={
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": REDIRECT_URI,
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET
            }).content
            return res.decode()
        except:
            return "Failed to get token"
    return "Invalid redirect"

@app.route("/api")
def hello_world():
    return "<p>Hello, World</p>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)