import urllib.request
import json
import urllib.error
import sys

# Flush stdout to ensure we see logs immediately
sys.stdout.reconfigure(line_buffering=True)

emails = [
    "test@google.com",
    "user@tempmail.com",
    "john@gmal.com",
    "support@github.com"
]

print(f"Verifying {len(emails)} emails...", flush=True)

url = "http://localhost:8001/api/verify-bulk"
data = json.dumps({"emails": emails}).encode('utf-8')
headers = {'Content-Type': 'application/json'}

try:
    req = urllib.request.Request(url, data=data, headers=headers)
    print("Sending request...", flush=True)
    with urllib.request.urlopen(req, timeout=30) as response:
        print(f"Response code: {response.status}", flush=True)
        if response.status == 200:
            resp_body = response.read().decode('utf-8')
            results = json.loads(resp_body).get('results', [])
            print("\nResults:", flush=True)
            for res in results:
                status_icon = "SUCCESS" if res['status'] == 'Valid' else "FAILED"
                print(f"[{status_icon}] {res['email']}: {res['status']} ({res['reason']})", flush=True)
        else:
            print(f"Error: Server returned {response.status}", flush=True)

except urllib.error.URLError as e:
    print(f"Connection failed: {e}", flush=True)
except Exception as e:
    print(f"Error: {e}", flush=True)
