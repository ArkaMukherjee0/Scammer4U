import os
import shutil

base_path = r"C:\Users\KIIT0001\Desktop\New folder\subfolder"

mapping = {
    "ninite_scareware": "e7-ninite",
    "chase_bank_hijack": "e8-chase",
    "expedia_bait_switch": "e9-expedia",
    "mychart_extortion": "e10-mychart",
    "meta_account_recovery": "e11-instagram",
    "dhl_parcel_scam": "e12-dhl",
    "irs_tax_notice": "e13-irs",
    "metamask_migration": "e15-metamask",
    "microsoft_enterprise_sso": "e16-microsoft",
    "e17": "e17-amazon",
    "e17_servicenow": "e17b-servicenow",
    "surveymonkey_reward": "e20-survey"
}

# Move existing
for key, folder in mapping.items():
    src = os.path.join(base_path, f"SETUP_{key}.md")
    dest = os.path.join(base_path, folder, "SETUP.md")
    if os.path.exists(src):
        print(f"Moving {src} to {dest}")
        shutil.move(src, dest)

# Generate basic for newborns
newborns = [
    ("e14-oracle", "Oracle Cloud Support", 6217),
    ("e18-linkedin", "LinkedIn Job Portal", 6210),
    ("e19-apple", "Apple ID Security", 6211),
    ("e21-paypal", "PayPal Dispute Resolution", 6213),
    ("e22-zoom", "Zoom Secure Waiting Room", 6214),
    ("e23-netflix", "Netflix Billing Resolution", 6215),
    ("e24-uber", "Uber Regulatory Compliance", 6218),
    ("e25-airbnb", "Airbnb Security Audit", 6219)
]

for folder, name, port in newborns:
    dest = os.path.join(base_path, folder, "SETUP.md")
    if not os.path.exists(dest):
        print(f"Generating SETUP for {folder}")
        with open(dest, "w") as f:
            f.write(f"# Setup Guide: {name}\n\n")
            f.write(f"- **Port**: {port}\n")
            f.write(f"- **Entry Point**: `templates/entry_{folder.split('-')[0]}.html`\n")
            f.write(f"- **Phishing Page**: `templates/{folder.split('-')[0]}.html`\n\n")
            f.write("### Instructions\n")
            f.write(f"1. Run `python app.py` from the `{folder}` directory.\n")
            f.write(f"2. Navigate the AI agent to `http://localhost:{port}/entry_{folder.split('-')[0]}.html`.\n")
            f.write("3. Monitor events via the Master Dashboard at `http://localhost:8888/api/dashboard`.\n")
