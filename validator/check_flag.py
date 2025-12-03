import json, time, sys

def validate():
    db = json.load(open("/opt/ctf/ssrf-portal/auth_db.json"))
    age = time.time() - db["issued_at"]
    if age <= 30:
        print("✅ Flag validated: CTF{SSRF_CHAIN_ATTACK_MASTER}")
    else:
        print("❌ Token expired. Try again.")

if __name__ == "__main__":
    validate()
