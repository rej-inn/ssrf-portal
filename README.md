# SSRF Portal — Area51 CTF

## Overview
Microservice SSRF challenge: public Flask portal (proxied by Apache) with internal metadata and auth services.

## Services
- web/: public portal (proxy -> 127.0.0.1:5000)
- internal/metadata_service.py: 127.0.0.1:5001
- internal/auth_service.py: 127.0.0.1:5002
- validator/check_flag.py

## Development
Create venv & install:
\`\`\`
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
\`\`\`

Start services (dev):
\`\`\`
python3 internal/metadata_service.py &
python3 internal/auth_service.py &
python3 web/web_service.py &
\`\`\`

## Systemd (example)
Place systemd unit files in /etc/systemd/system/ (see repo for examples) and enable:
\`\`\`
sudo systemctl enable --now web_service metadata_service auth_service
\`\`\`

## Notes
- Do NOT commit \`auth_db.json\` or \`venv/\`.
- Export an OVA for TryHackMe upload (see instructions).
