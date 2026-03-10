from urllib import request
from datetime import datetime, timezone
import hmac
import hashlib
import json
from dotenv import load_dotenv
import os

load_dotenv()

url = os.getenv("POST_URL"," http://127.0.0.1:5000/echo")

name = "Patrick Lake"
email = "plake.dev@gmail.com"
resume_link = ""
repository_link = "https://github.com/plake492/b12_submission"
action_run_link = ""
now = datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")

signing_secret = os.getenv("SIGNING_SECRET").encode("utf-8")

payload = {
    "name": name,
    "email": email,
    "resume_link": resume_link,
    "repository_link": repository_link,
    "action_run_link": action_run_link,
    "timestamp": now
}

data = json.dumps(payload, separators=(",",":"), sort_keys=True).encode("utf-8")

signature = hmac.new(
    key=signing_secret,
    msg=data,
    digestmod=hashlib.sha256
).hexdigest()

res = request.Request(
    url,
    data=data, 
    headers={'Content-Type': 'application/json'}
)
res.add_header("X-Signature-256", f"sha256={signature}")

with request.urlopen(res) as response:
    result = json.loads(response.read())
    print(json.dumps(result, indent=4))
