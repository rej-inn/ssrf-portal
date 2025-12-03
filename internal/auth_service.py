#!/usr/bin/env python3
import os
import time
import json
import hmac
import hashlib
import sys
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Config
DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'auth_db.json')
TOKEN_EXPIRY = 120  # seconds
META_URL = os.environ.get("META_URL", "http://127.0.0.1:5001/instance-info")

def fetch_metadata_with_retry(timeout=15, interval=0.5):
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            r = requests.get(META_URL, timeout=2)
            r.raise_for_status()
            return r.json()
        except Exception:
            time.sleep(interval)
    print(f"[auth_service] ERROR: metadata not reachable at {META_URL} after {timeout}s", file=sys.stderr)
    return None

meta = fetch_metadata_with_retry()
if meta is None:
    # fallback to safe defaults for development so service can start
    INSTANCE_ID = os.environ.get("INSTANCE_ID", "dev-instance")
    SECRET_PART = os.environ.get("SECRET_PART", "deadbeef")
    print("[auth_service] Warning: using fallback INSTANCE_ID/SECRET_PART")
else:
    INSTANCE_ID = meta.get("instance-id")
    SECRET_PART = meta.get("secret-part")

def compute_hmac():
    return hmac.new(SECRET_PART.encode(), INSTANCE_ID.encode(), digestmod=hashlib.sha256).hexdigest()

@app.route("/get-token", methods=["GET", "POST"])
def get_token():
    """
    Accept token & hmac via:
      - POST: headers Authorization: Bearer <token>, X-Internal-HMAC
      - GET: query params token=<token>&hmac=<hmac>
    """
    token = None
    hmac_header = None

    # Check headers first (POST)
    auth_header = request.headers.get("Authorization", "")
    if auth_header.startswith("Bearer "):
        token = auth_header.split(" ", 1)[1].strip()
        hmac_header = request.headers.get("X-Internal-HMAC", "")

    # Fallback to GET params
    if not token:
        token = request.args.get("token")
        hmac_header = request.args.get("hmac")

    if not token or not hmac_header:
        return jsonify({"error": "Missing token or hmac"}), 403

    expected = compute_hmac()
    if hmac_header != expected:
        return jsonify({"error": "Invalid HMAC"}), 403

    issued_at = int(time.time())
    data = {"token": token, "issued_at": issued_at}
    # write DB atomically
    tmp = DB_PATH + ".tmp"
    with open(tmp, "w") as f:
        json.dump(data, f)
    os.replace(tmp, DB_PATH)
    return jsonify({"status": "Token accepted", "issued_at": issued_at})

@app.route("/admin")
def admin():
    if not os.path.exists(DB_PATH):
        return jsonify({"error": "No token found"}), 403

    try:
        data = json.load(open(DB_PATH))
    except Exception:
        return jsonify({"error": "Invalid auth DB"}), 500

    if time.time() - data.get("issued_at", 0) > TOKEN_EXPIRY:
        return jsonify({"error": "Token expired"}), 403

    # Return flag (in real CTF keep flag in validator; simple here)
    return jsonify({"flag": "CTF{ssrf_chain_hmac_master}"})

if __name__ == "__main__":
    # Use 127.0.0.1 binding so only local SSRF can reach it
    app.run(host="127.0.0.1", port=5002)
PY
