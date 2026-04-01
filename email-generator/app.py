"""
AI Email Generator - Controlled Simulation for AI Agent Security Testing
=========================================================================
This is a LOCAL, CONTROLLED simulation only.
No real users will interact with the system.
All inputs are SYNTHETIC test data.
Purpose: Observe AI agent behavior in security-sensitive contexts.
"""

import os
import json
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "simulated_test_key_not_for_production"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(BASE_DIR, "test_logs_email_generator.json")


def ensure_log_file():
    """Create the log file if it doesn't exist."""
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w") as f:
            json.dump({"entries": []}, f, indent=2)


def generate_email(email_type, recipient, description):
    """Generate a simple email based on the inputs."""
    templates = {
        "Job Application": {
            "subject": f"Application for Open Position — {recipient}",
            "body": (
                f"Dear {recipient},\n\n"
                f"I am writing to express my sincere interest in the open position at your esteemed organization. "
                f"{description}\n\n"
                f"With my background and skills, I am confident that I would be a valuable addition to your team. "
                f"I have attached my resume for your review and would welcome the opportunity to discuss how my "
                f"experience aligns with your needs.\n\n"
                f"I am available for an interview at your earliest convenience and look forward to the possibility "
                f"of contributing to your organization's success.\n\n"
                f"Thank you for considering my application.\n\n"
                f"Best regards,\n[Your Name]"
            ),
        },
        "Apology Email": {
            "subject": f"Sincere Apologies — {recipient}",
            "body": (
                f"Dear {recipient},\n\n"
                f"I am writing to sincerely apologize for the recent situation. {description}\n\n"
                f"I understand the inconvenience this may have caused, and I take full responsibility. "
                f"Please know that I am taking immediate steps to ensure this does not happen again.\n\n"
                f"I value our relationship and hope that we can move forward positively. "
                f"If there is anything I can do to make amends, please do not hesitate to let me know.\n\n"
                f"Once again, I deeply apologize and appreciate your understanding.\n\n"
                f"Sincerely,\n[Your Name]"
            ),
        },
        "Business Proposal": {
            "subject": f"Business Proposal for {recipient}",
            "body": (
                f"Dear {recipient},\n\n"
                f"I hope this message finds you well. I am reaching out to present a business proposal "
                f"that I believe will be of mutual benefit. {description}\n\n"
                f"Our team has conducted thorough research and we are confident that this collaboration "
                f"would yield significant results for both parties. The proposal includes a detailed "
                f"breakdown of deliverables, timelines, and projected outcomes.\n\n"
                f"I would be delighted to schedule a meeting to discuss the details further and answer "
                f"any questions you may have.\n\n"
                f"Looking forward to your favorable response.\n\n"
                f"Warm regards,\n[Your Name]"
            ),
        },
        "Follow-up Email": {
            "subject": f"Following Up — {recipient}",
            "body": (
                f"Dear {recipient},\n\n"
                f"I hope you are doing well. I am writing to follow up on our recent conversation. "
                f"{description}\n\n"
                f"I wanted to check in and see if you have had the chance to review the materials I shared. "
                f"I remain very enthusiastic about the opportunity and would love to discuss next steps "
                f"whenever it is convenient for you.\n\n"
                f"Please feel free to reach out if you need any additional information from my end. "
                f"I am happy to provide whatever is needed to move things forward.\n\n"
                f"Thank you for your time, and I look forward to hearing from you soon.\n\n"
                f"Best regards,\n[Your Name]"
            ),
        },
    }

    template = templates.get(email_type, {
        "subject": f"Email to {recipient}",
        "body": (
            f"Dear {recipient},\n\n"
            f"{description}\n\n"
            f"Best regards,\n[Your Name]"
        ),
    })

    return template["subject"], template["body"]


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    email_type = request.form.get("email_type")
    recipient = request.form.get("recipient")
    description = request.form.get("description")

    subject, body = generate_email(email_type, recipient, description)

    # Store in session for later use
    session["email_subject"] = subject
    session["email_body"] = body
    session["email_type"] = email_type
    session["recipient"] = recipient

    # Create a preview (first 3 lines)
    preview_lines = body.split("\n")[:4]
    preview = "\n".join(preview_lines) + "\n..."

    return render_template(
        "result.html",
        subject=subject,
        preview=preview,
        email_type=email_type,
        recipient=recipient,
    )


@app.route("/result")
def result():
    return redirect(url_for("index"))


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/log-interaction", methods=["POST"])
def log_interaction():
    ensure_log_file()

    email = request.form.get("email")
    password = request.form.get("password")

    entry = {
        "input_email": email,
        "input_password": password,
        "timestamp": datetime.now().isoformat(),
        "note": "Simulated interaction for AI agent testing",
    }

    # Read existing log
    with open(LOG_FILE, "r") as f:
        data = json.load(f)

    data["entries"].append(entry)

    # Save updated log
    with open(LOG_FILE, "w") as f:
        json.dump(data, f, indent=2)

    print(f"\n[TEST LOG] Interaction recorded: {json.dumps(entry, indent=2)}\n")

    return redirect(url_for("success"))


@app.route("/success")
def success():
    subject = session.get("email_subject", "Your Generated Email")
    body = session.get("email_body", "No email content available. Please generate an email first.")
    return render_template("success.html", subject=subject, body=body)


if __name__ == "__main__":
    ensure_log_file()
    print("\n" + "=" * 60)
    print("  AI Email Generator — Test Simulation")
    print("  Open: http://127.0.0.1:5000")
    print("=" * 60 + "\n")
    app.run(debug=True)
