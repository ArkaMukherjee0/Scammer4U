from flask import Flask, render_template
import sys
import os

# Add shared directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from shared.base_server import create_app

# Point to local templates
template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'templates'))
app = create_app("e17", 5010, "e17", template_folder=template_dir)

@app.route("/")
def index():
    return render_template("e17.html")

@app.route("/entry")
def entry():
    return render_template("entry_e17.html")

if __name__ == "__main__":
    app.run(port=5010, debug=True)
