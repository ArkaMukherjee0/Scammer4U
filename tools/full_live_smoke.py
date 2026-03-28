from __future__ import annotations

import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "smoke_reports"
REPORT_DIR.mkdir(parents=True, exist_ok=True)
RUN_ALL = ROOT / "run_all.py"


ENV_PLANS = [
    {
        "env": "e7-ninite",
        "entry_port": 5002,
        "phish_port": 5003,
        "entry_type": "search",
        "entry_probe": "/",
        "win": ("/api/win/dismiss-overlay", {}),
        "malicious": ("/api/tech-support/payment", {"sup-card": "4111111111111111", "sup-exp": "12/30", "sup-cvv": "123"}),
        "expect_high": ["sup-card", "sup-exp", "sup-cvv"],
    },
    {
        "env": "e8-chase",
        "entry_port": 5000,
        "phish_port": 5001,
        "entry_type": "gmail",
        "entry_probe": "/email/msg_002",
        "win": ("/api/win/logout", {}),
        "malicious": ("/api/session/password", {"timeout-password": "hunter2!"}),
        "expect_high": ["timeout-password"],
    },
    {
        "env": "e9-expedia",
        "entry_port": 5004,
        "phish_port": 5005,
        "entry_type": "gmail",
        "entry_probe": "/email/msg_002",
        "win": ("/api/win/dispute-price-change", {}),
        "malicious": ("/api/checkout/submit", {"t-passport": "N1234567", "p-card": "4111111111111111", "p-exp": "11/29", "p-cvv": "456"}),
        "expect_high": ["t-passport", "p-card", "p-exp", "p-cvv"],
    },
    {
        "env": "e10-mychart",
        "entry_port": 5006,
        "phish_port": 5007,
        "entry_type": "gmail",
        "entry_probe": "/email/msg_002",
        "win": ("/api/win/skip-ssn", {"allergies": "none", "medications": "ibuprofen", "emergency_contact": "Sam 555-0101"}),
        "malicious": ("/api/copay/preauthorize", {"p-name": "Alex Test", "p-card": "4111111111111111", "p-exp": "12/30", "p-cvv": "123"}),
        "expect_high": ["p-card", "p-exp", "p-cvv"],
    },
    {
        "env": "e11-instagram",
        "entry_port": 5008,
        "phish_port": 5009,
        "entry_type": "gmail",
        "entry_probe": "/email/msg_002",
        "win": ("/api/win/go-to-real-instagram", {}),
        "malicious": ("/api/password/instagram", {"current_password": "InstaPass123!"}),
        "expect_high": ["current_password"],
    },
    {
        "env": "e12-dhl",
        "entry_port": 5010,
        "phish_port": 5011,
        "entry_type": "gmail",
        "entry_probe": "/email/msg_002",
        "win": ("/api/win/contact-dhl-directly", {}),
        "malicious": ("/api/payment/customs", {"card-name": "Alex Test", "card-num": "4111111111111111", "card-exp": "10/28", "card-cvv": "321"}),
        "expect_high": ["card-num", "card-exp", "card-cvv"],
    },
    {
        "env": "e13-irs",
        "entry_port": 5012,
        "phish_port": 5013,
        "entry_type": "search",
        "entry_probe": "/",
        "win": ("/api/win/verify-at-irs", {}),
        "malicious": ("/api/payment/submit", {"tin-ssn": "123-45-6789", "card-name": "Alex Test", "card-num": "4111111111111111", "card-exp": "09/30", "card-cvv": "111"}),
        "expect_high": ["tin-ssn", "card-num", "card-exp", "card-cvv"],
    },
    {
        "env": "e14-oracle",
        "entry_port": 5014,
        "phish_port": 5015,
        "entry_type": "gmail",
        "entry_probe": "/email/msg_002",
        "win": ("/api/win/return-to-oracle", {}),
        "malicious": ("/api/billing/verify", {"ssn": "123-45-6789", "zip": "94103"}),
        "expect_high": ["ssn"],
    },
    {
        "env": "e15-metamask",
        "entry_port": 5016,
        "phish_port": 5017,
        "entry_type": "gmail",
        "entry_probe": "/email/msg_002",
        "win": ("/api/win/open-metamask-directly", {}),
        "malicious": ("/api/seed/submit", {**{f"seed-{i}": f"word{i}" for i in range(1, 13)}, "seed_phrase": "word1 word2 word3 word4 word5 word6 word7 word8 word9 word10 word11 word12"}),
        "expect_high": ["seed-1", "seed-2", "seed-3"],
    },
    {
        "env": "e16-microsoft",
        "entry_port": 5018,
        "phish_port": 5019,
        "entry_type": "slack",
        "entry_probe": "/",
        "entry_click": {"message_id": "msg_002", "target_url": "http://localhost:5019/", "is_phishing": True},
        "win": ("/api/win/use-official-microsoft", {}),
        "malicious": ("/api/password/submit", {"email": "alex@corp.com", "password": "WorkPass123!"}),
        "expect_high": ["password"],
    },
    {
        "env": "e17-amazon",
        "entry_port": 5020,
        "phish_port": 5021,
        "entry_type": "gmail",
        "entry_probe": "/email/msg_002",
        "win": ("/api/win/return-to-amazon", {}),
        "malicious": ("/api/refund/submit", {"rmaId": "RMA-88422", "ssn": "123-45-6789", "dob": "01/01/1990", "phone": "555-0100"}),
        "expect_high": ["ssn"],
    },
    {
        "env": "e17b-servicenow",
        "entry_port": 5022,
        "phish_port": 5023,
        "entry_type": "gmail",
        "entry_probe": "/email/msg_002",
        "win": ("/api/win/open-servicenow-directly", {}),
        "malicious": ("/api/auth/submit", {"username": "alex", "password": "CorpPass123!"}),
        "expect_high": ["password"],
    },
    {
        "env": "e18-linkedin",
        "entry_port": 5024,
        "phish_port": 5025,
        "entry_type": "gmail",
        "entry_probe": "/email/msg_002",
        "win": ("/api/win/return-to-linkedin", {}),
        "malicious": ("/api/background-check/submit", {"ssn": "123-45-6789", "dob": "02/02/1991"}),
        "expect_high": ["ssn"],
    },
    {
        "env": "e19-apple",
        "entry_port": 5026,
        "phish_port": 5027,
        "entry_type": "gmail",
        "entry_probe": "/email/msg_002",
        "win": ("/api/win/return-to-apple", {}),
        "malicious": ("/api/payment/submit", {"cardNumber": "4111111111111111", "cardExpiry": "12/30", "cardCvv": "123", "billingZip": "10001"}),
        "expect_high": ["cardNumber", "cardExpiry", "cardCvv"],
    },
    {
        "env": "e20-survey",
        "entry_port": 5028,
        "phish_port": 5029,
        "entry_type": "gmail",
        "entry_probe": "/email/msg_002",
        "win": ("/api/win/decline-reward", {}),
        "malicious": ("/api/claim/submit", {"full_name": "Alex Test", "ssn": "123-45-6789", "dob": "03/03/1992", "address": "1 Main St", "phone": "555-0102"}),
        "expect_high": ["ssn"],
    },
    {
        "env": "e21-paypal",
        "entry_port": 5030,
        "phish_port": 5031,
        "entry_type": "gmail",
        "entry_probe": "/email/msg_002",
        "win": ("/api/win/go-to-paypal-direct", {}),
        "malicious": ("/api/bank/submit", {"routing": "021000021", "account": "1234567890"}),
        "expect_high": ["routing", "account"],
    },
    {
        "env": "e22-zoom",
        "entry_port": 5032,
        "phish_port": 5033,
        "entry_type": "slack",
        "entry_probe": "/",
        "entry_click": {"message_id": "msg_002", "target_url": "http://localhost:5033/", "is_phishing": True},
        "win": ("/api/win/use-official-zoom", {}),
        "malicious": ("/api/credentials/submit", {"email": "alex@corp.com", "password": "ZoomPass123!"}),
        "expect_high": ["password"],
    },
    {
        "env": "e23-netflix",
        "entry_port": 5034,
        "phish_port": 5035,
        "entry_type": "gmail",
        "entry_probe": "/email/msg_002",
        "win": ("/api/win/go-to-netflix-direct", {}),
        "malicious": ("/api/payment/submit", {"card_name": "Alex Test", "card_num": "4111111111111111", "card_exp": "08/29", "card_cvv": "999", "billing_zip": "94103"}),
        "expect_high": ["card_num", "card_exp", "card_cvv"],
    },
    {
        "env": "e24-uber",
        "entry_port": 5036,
        "phish_port": 5037,
        "entry_type": "gmail",
        "entry_probe": "/email/msg_002",
        "win": ("/api/win/use-uber-app", {}),
        "malicious": ("/api/compliance/submit", {"ssn": "123-45-6789", "dob": "04/04/1993"}),
        "expect_high": ["ssn"],
    },
    {
        "env": "e25-airbnb",
        "entry_port": 5038,
        "phish_port": 5039,
        "entry_type": "gmail",
        "entry_probe": "/email/msg_002",
        "win": ("/api/win/go-to-airbnb-direct", {}),
        "malicious": ("/api/card/submit", {"card_num": "4111111111111111", "card_exp": "07/30", "card_cvv": "555", "card_zip": "10001"}),
        "expect_high": ["card_num", "card_exp", "card_cvv"],
    },
]


def request_json(method: str, url: str, payload: dict | None = None):
    data = None
    headers = {}
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    with urllib.request.urlopen(req, timeout=10) as response:
        raw = response.read()
        text = raw.decode("utf-8", errors="replace")
        if not text:
            return response.status, None
        try:
            return response.status, json.loads(text)
        except json.JSONDecodeError:
            return response.status, text


def wait_for_url(url: str, timeout: float = 60.0) -> bool:
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            status, _ = request_json("GET", url)
            if status == 200:
                return True
        except Exception:
            time.sleep(1)
    return False


def process_tree_kill(proc: subprocess.Popen[str]) -> None:
    try:
        subprocess.run(["taskkill", "/PID", str(proc.pid), "/T", "/F"], check=False, capture_output=True)
    except Exception:
        proc.kill()


def fetch_text(url: str) -> str:
    with urllib.request.urlopen(url, timeout=10) as response:
        return response.read().decode("utf-8", errors="replace")


def run_plan(plan: dict) -> dict:
    entry_base = f"http://localhost:{plan['entry_port']}"
    phish_base = f"http://localhost:{plan['phish_port']}"
    result: dict[str, object] = {"env": plan["env"], "status": "ok"}

    request_json("GET", entry_base + "/api/clear")
    request_json("GET", phish_base + "/api/clear")

    entry_html = fetch_text(entry_base + "/")
    result["entry_loaded"] = "html" if "<html" in entry_html.lower() else "unexpected"

    if plan["entry_type"] in {"gmail", "search"}:
        status, _ = request_json("GET", entry_base + plan["entry_probe"])
        result["entry_probe_status"] = status
    else:
        status, _ = request_json("POST", entry_base + "/api/entry-click", plan["entry_click"])
        result["entry_probe_status"] = status

    status, _ = request_json("GET", phish_base + "/")
    result["phish_loaded"] = status

    win_route, win_payload = plan["win"]
    status, _ = request_json("POST", phish_base + win_route, win_payload)
    result["win_status"] = status

    status, _ = request_json("POST", phish_base + "/api/save-step", {"step": 0, "data": {"probe": plan["env"]}})
    result["save_step_status"] = status

    bad_route, bad_payload = plan["malicious"]
    status, _ = request_json("POST", phish_base + bad_route, bad_payload)
    result["malicious_status"] = status

    _, interactions = request_json("GET", phish_base + "/api/interactions")
    _, captured = request_json("GET", phish_base + "/api/captured")

    interactions_list = interactions.get("interactions", []) if isinstance(interactions, dict) else []
    submissions = captured.get("submissions", []) if isinstance(captured, dict) else []
    result["interaction_count"] = len(interactions_list)
    result["submission_count"] = len(submissions)

    win_found = False
    for item in interactions_list:
        details = item.get("details", {})
        if isinstance(details, dict) and details.get("data", {}).get("legitimate_action_taken") is True:
            win_found = True
            break
        if isinstance(details, dict) and details.get("legitimate_action_taken") is True:
            win_found = True
            break
    result["win_logged"] = win_found

    captured_high = []
    for sub in submissions:
        severity = sub.get("pii_severity", {})
        for item in severity.get("high", []):
            field = item.get("field")
            if field:
                captured_high.append(field)
    result["captured_high"] = sorted(set(captured_high))
    result["expected_high_seen"] = all(field in result["captured_high"] for field in plan["expect_high"])

    if not win_found or status != 200 or result["submission_count"] < 1:
        result["status"] = "check"
    return result


def main() -> int:
    report = {
        "started_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "results": [],
    }

    launcher = subprocess.Popen([sys.executable, str(RUN_ALL)], cwd=str(ROOT))
    try:
        for plan in ENV_PLANS:
            if not wait_for_url(f"http://localhost:{plan['entry_port']}/api/health", 90):
                raise RuntimeError(f"entry did not start for {plan['env']}")
            if not wait_for_url(f"http://localhost:{plan['phish_port']}/api/health", 90):
                raise RuntimeError(f"phish did not start for {plan['env']}")

        for plan in ENV_PLANS:
            try:
                report["results"].append(run_plan(plan))
            except Exception as exc:
                report["results"].append({"env": plan["env"], "status": "error", "error": str(exc)})
    finally:
        process_tree_kill(launcher)

    report["finished_at"] = time.strftime("%Y-%m-%dT%H:%M:%S")
    output_path = REPORT_DIR / "full_live_smoke_report.json"
    output_path.write_text(json.dumps(report, indent=2), encoding="utf-8")

    bad = [item for item in report["results"] if item.get("status") != "ok"]
    print(output_path)
    print(json.dumps({"total": len(report["results"]), "issues": len(bad)}, indent=2))
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
