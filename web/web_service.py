from flask import Flask, request
import requests, re, json
import os

app = Flask(__name__)

@app.route("/")
def index():
    return """
    <!doctype html>
    <html lang="en">
    <head>
      <meta charset="utf-8">
      <title>Area51 Systems</title>
      <meta name="viewport" content="width=device-width,initial-scale=1">
      <style>
        :root{
          --bg:#f6f7fb; --card:#ffffff; --muted:#6b7280; --accent:#0ea5a4; --accent-2:#2563eb;
          --glass: rgba(255,255,255,0.6);
          --radius:12px;
          font-family: Inter, ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial;
        }
        html,body{height:100%;margin:0;background:linear-gradient(180deg,var(--bg),#ffffff);color:#0f172a}
        .frame{max-width:1200px;margin:4vh auto;padding:28px;}
        .grid{
          display:grid;grid-template-columns: 260px 1fr;gap:20px;align-items:start;
        }
        .sidebar{
          background:var(--card);border-radius:var(--radius);padding:18px;box-shadow:0 6px 20px rgba(15,23,42,0.06);
        }
        .brand{display:flex;align-items:center;gap:12px;margin-bottom:18px}
        .logo{width:52px;height:52px;border-radius:10px;background:linear-gradient(135deg,var(--accent-2),var(--accent));display:flex;align-items:center;justify-content:center;color:#fff;font-weight:700;font-size:18px}
        .org{font-size:14px;margin:0}
        .org-sub{color:var(--muted);font-size:12px;margin-top:2px}
        .nav{margin-top:14px;border-top:1px solid #eef2f7;padding-top:12px}
        .nav a{display:block;color:#0f172a;text-decoration:none;padding:8px 0;font-size:13px}
        .nav a .note{display:block;color:var(--muted);font-size:12px}
        .side-card{margin-top:14px;padding:12px;background:linear-gradient(180deg,#fff, #fbfcff);border-radius:8px}
        .pill{display:inline-block;padding:6px 10px;border-radius:999px;font-size:12px;background:#eef2ff;color:#1e293b;margin-right:6px}
        .main{display:flex;flex-direction:column;gap:18px}
        .header{display:flex;justify-content:space-between;align-items:center}
        .title{font-size:18px;margin:0}
        .subtitle{color:var(--muted);font-size:13px;margin-top:4px}
        .cards{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-top:6px}
        .card{background:var(--card);padding:14px;border-radius:12px;box-shadow:0 6px 20px rgba(15,23,42,0.04)}
        .card h3{margin:0;font-size:13px}
        .stat{font-size:22px;font-weight:700;margin-top:8px}
        .meta{font-size:12px;color:var(--muted);margin-top:6px}
        .bar{height:10px;background:#eef2f7;border-radius:999px;overflow:hidden;margin-top:10px}
        .bar > i{display:block;height:100%;width:0;background:linear-gradient(90deg,var(--accent-2),var(--accent));border-radius:inherit}
        .panel{background:var(--card);padding:16px;border-radius:12px;box-shadow:0 6px 20px rgba(15,23,42,0.04)}
        .panel h4{margin:0 0 8px 0;font-size:14px}
        .cols{display:grid;grid-template-columns:1fr 360px;gap:14px}
        .logs{background:#0b1220;color:#cbd5e1;padding:12px;border-radius:8px;font-family:ui-monospace, SFMono-Regular, Menlo, Monaco, "Roboto Mono", monospace;font-size:12px;max-height:220px;overflow:auto}
        .muted{color:var(--muted)}
      </style>
    </head>
    <body>
      <h1>Area51 Internal Portal</h1>
      <p>Static UI only. SSRF endpoints below.</p>
    </body>
    </html>
    """

@app.route("/fetch")
def fetch():
    url = request.args.get("url")
    if not url:
        return "Missing URL", 400

    # naive block
    if re.search(r"127\.0\.0\.1|0\.0\.0\.0|169\.254", url):
        return "Access Denied: localhost blocked", 403

    try:
        r = requests.get(url, timeout=3)
        return r.text, r.status_code
    except Exception as e:
        return str(e), 500


@app.route("/fetch_with_headers", methods=["POST"])
def fetch_with_headers():
    url = request.form.get("url")
    headers_json = request.form.get("headers", "{}")

    try:
        headers = json.loads(headers_json)
    except Exception as e:
        return f"Invalid headers JSON: {e}", 400

    try:
        r = requests.get(url, headers=headers, timeout=5)
        return r.text, r.status_code
    except Exception as e:
        return str(e), 500


if __name__ == "__main__":
    # ❤️ Render.com uses PORT env variable
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
