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
    next_uri = request.args.get("next_uri")
    return app.redirect(f"{RC_AUTH_URL}?{urlencode({
        "response_type": "code",
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "state": next_uri
    })}")

@app.route("/rcredirect")
def rcredirect():
    code = request.args.get("code")
    next_uri = request.args.get("state")
    if code is not None and next_uri is not None and len(next_uri) > 0:
        try:
            res = requests.post(RC_TOKEN_URL, data={
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": REDIRECT_URI,
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET
            }).json()
            return app.redirect(f"{next_uri}?{urlencode({
                "access_token": res["access_token"],
                "expires_in": res["expires_in"],
            })}")
        except:
            return "Failed to get token"
    return "Invalid redirect"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)