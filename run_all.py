import os
import subprocess
import sys
import time

base = os.path.dirname(__file__)

environments = [
    ("e7-ninite", "http://localhost:5002", "http://localhost:5003"),
    ("e8-chase", "http://localhost:5000", "http://localhost:5001"),
    ("e9-expedia", "http://localhost:5004", "http://localhost:5005"),
    ("e10-mychart", "http://localhost:5006", "http://localhost:5007"),
    ("e11-instagram", "http://localhost:5008", "http://localhost:5009"),
    ("e12-dhl", "http://localhost:5010", "http://localhost:5011"),
    ("e13-irs", "http://localhost:5012", "http://localhost:5013"),
    ("e14-oracle", "http://localhost:5014", "http://localhost:5015"),
    ("e15-metamask", "http://localhost:5016", "http://localhost:5017"),
    ("e16-microsoft", "http://localhost:5018", "http://localhost:5019"),
    ("e17-amazon", "http://localhost:5020", "http://localhost:5021"),
    ("e17b-servicenow", "http://localhost:5022", "http://localhost:5023"),
    ("e18-linkedin", "http://localhost:5024", "http://localhost:5025"),
    ("e19-apple", "http://localhost:5026", "http://localhost:5027"),
    ("e20-survey", "http://localhost:5028", "http://localhost:5029"),
    ("e21-paypal", "http://localhost:5030", "http://localhost:5031"),
    ("e22-zoom", "http://localhost:5032", "http://localhost:5033"),
    ("e23-netflix", "http://localhost:5034", "http://localhost:5035"),
    ("e24-uber", "http://localhost:5036", "http://localhost:5037"),
    ("e25-airbnb", "http://localhost:5038", "http://localhost:5039"),
]

print("=" * 60)
print("AgentTrap Converted Environments")
print("=" * 60)
for env_name, entry_url, phishing_url in environments:
    print(f"  {env_name} entry:    {entry_url}")
    print(f"  {env_name} phishing: {phishing_url}")
print("=" * 60)
print()

for env_name, _, _ in environments:
    subprocess.Popen([sys.executable, 'run_servers.py'], cwd=os.path.join(base, env_name))
    time.sleep(1)
