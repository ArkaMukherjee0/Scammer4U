"""
Server Runner for LLM PII Benchmark
Starts both legitimate and phishing sites for testing.

Usage: python run_servers.py
"""

import json
import subprocess
import sys
import os
import time
from threading import Thread

def load_config():
    """Load port configuration"""
    with open('config.json', 'r') as f:
        return json.load(f)

def run_legitimate_site(port):
    """Run the legitimate job portal"""
    os.chdir('legitimate_site')
    subprocess.run([
        sys.executable, 'app.py'
    ])

def run_phishing_site(port):
    """Run the phishing clone"""
    os.chdir('phishing_site')
    subprocess.run([
        sys.executable, 'app.py'
    ])

def main():
    config = load_config()

    print("="*60)
    print("LLM PII Benchmark - Server Runner")
    print("="*60)
    print()
    print("Starting servers...")
    print()
    print(f"  Legitimate site: http://localhost:{config['ports']['legitimate_job_portal']}")
    print(f"  Phishing site:   http://localhost:{config['ports']['phishing_clone']}")
    print()
    print("Domain mappings (add to hosts file):")
    for entry in config['hosts_entries']:
        print(f"  {entry}")
    print()
    print("Press Ctrl+C to stop all servers")
    print("="*60)
    print()

    # Start both servers in separate processes
    legitimate_process = subprocess.Popen(
        [sys.executable, 'app.py'],
        cwd='legitimate_site'
    )

    # Small delay to avoid port conflicts
    time.sleep(1)

    phishing_process = subprocess.Popen(
        [sys.executable, 'app.py'],
        cwd='phishing_site'
    )

    try:
        # Wait for both processes
        legitimate_process.wait()
        phishing_process.wait()
    except KeyboardInterrupt:
        print("\n\nShutting down servers...")
        legitimate_process.terminate()
        phishing_process.terminate()
        print("Servers stopped.")

if __name__ == '__main__':
    main()
