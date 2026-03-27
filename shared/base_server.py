import datetime
import io
import json
import os
from flask import Flask, jsonify, render_template_string, request, send_file
from flask_cors import CORS

# ---------------------------------------------------------------------------
# Load shared config.json (sits one level above shared/)
# ---------------------------------------------------------------------------
_SHARED_DIR = os.path.dirname(os.path.abspath(__file__))
_CONFIG_PATH = os.path.join(os.path.dirname(_SHARED_DIR), 'config.json')


def _load_config():
    if os.path.exists(_CONFIG_PATH):
        with open(_CONFIG_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}


DEFAULT_PERSONA = {
    "name":    "Alex Johnson",
    "email":   "alex.johnson@gmail.com",
    "phone":   "512-555-0199",
    "address": "1234 Elm Street, Austin, TX 78701"
}


def get_persona():
    config = _load_config()
    return config.get('agent_persona', DEFAULT_PERSONA)


def get_environment_port(env_id, default_port):
    config = _load_config()
    return config.get('ports', {}).get(env_id, default_port)


def create_app(env_id, port, env_name, template_folder=None):
    app = Flask(__name__, template_folder=template_folder)
    CORS(app)

    # Paths
    BASE_DIR = _SHARED_DIR
    LOGS_DIR = os.path.join(os.path.dirname(BASE_DIR), 'logs')
    LOG_FILE = os.path.join(LOGS_DIR, f'{env_id}_log.json')
    LIVE_LOG = os.path.join(LOGS_DIR, 'LIVE_CAPTURE.txt')

    if not os.path.exists(LOGS_DIR):
        os.makedirs(LOGS_DIR)

    # ------------------------------------------------------------------
    # Auto-inject persona into every Jinja2 template render
    # Usage in HTML: {{ persona.name }}, {{ persona.email }}, etc.
    # ------------------------------------------------------------------
    @app.context_processor
    def inject_persona():
        return {"persona": get_persona()}

    # ------------------------------------------------------------------
    # Routes
    # ------------------------------------------------------------------
    @app.route('/health', methods=['GET'])
    @app.route('/api/health', methods=['GET'])
    def health():
        return jsonify({"status": "healthy", "env": env_id, "name": env_name})

    @app.route('/api/config', methods=['GET'])
    def get_config():
        """Returns agent persona so JS entry templates can personalise emails."""
        return jsonify({"persona": get_persona()})

    @app.route('/api/log', methods=['POST'])
    def log_capture():
        data = request.json
        if not data:
            return jsonify({"error": "No data received"}), 400

        data['env'] = env_id
        data['timestamp'] = datetime.datetime.now().isoformat()

        logs = []
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, 'r') as f:
                try:
                    logs = json.load(f)
                except Exception:
                    logs = []

        logs.append(data)
        with open(LOG_FILE, 'w') as f:
            json.dump(logs, f, indent=4)

        with open(LIVE_LOG, 'a', encoding='utf-8') as f:
            f.write(f"\n[{data['timestamp']}] | {env_id} | {data['attack_type']}\n")
            if 'fields' in data:
                for k, v in data['fields'].items():
                    f.write(f"  - {k}: {v}\n")
            if 'notes' in data:
                f.write(f"  Notes: {data['notes']}\n")
            f.write("-" * 40 + "\n")

        return jsonify({"status": "logged", "index": len(logs)})

    @app.route('/api/results', methods=['GET'])
    def get_results():
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, 'r') as f:
                return f.read(), 200, {'Content-Type': 'application/json'}
        return jsonify([])

    @app.route('/api/clear', methods=['GET', 'POST'])
    def clear_logs():
        if os.path.exists(LOG_FILE):
            os.remove(LOG_FILE)
        return jsonify({"status": "cleared"})

    @app.route('/api/dashboard', methods=['GET'])
    def dashboard():
        dashboard_path = os.path.join(BASE_DIR, 'dashboard.html')
        if os.path.exists(dashboard_path):
            with open(dashboard_path, 'r', encoding='utf-8') as f:
                template = f.read()
            return render_template_string(template, env_id=env_id, env_name=env_name)
        return "Dashboard template not found in shared/", 404

    @app.route('/api/download/<path:filename>', methods=['GET'])
    def download_placeholder(filename):
        payload = io.BytesIO(b"MZ" + (b"\x00" * 1024))
        return send_file(
            payload,
            as_attachment=True,
            download_name=os.path.basename(filename),
            mimetype='application/octet-stream',
        )

    # Each env's app.py defines '/', '/entry', etc.
    return app
