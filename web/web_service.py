from flask import Flask, request
import requests, re
import json
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

        /* Sidebar */
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

        /* Main content */
        .main{display:flex;flex-direction:column;gap:18px}
        .header{display:flex;justify-content:space-between;align-items:center}
        .title{font-size:18px;margin:0}
        .subtitle{color:var(--muted);font-size:13px;margin-top:4px}

        .cards{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-top:6px}
        .card{background:var(--card);padding:14px;border-radius:12px;box-shadow:0 6px 20px rgba(15,23,42,0.04)}
        .card h3{margin:0;font-size:13px}
        .stat{font-size:22px;font-weight:700;margin-top:8px}
        .meta{font-size:12px;color:var(--muted);margin-top:6px}

        /* progress */
        .bar{height:10px;background:#eef2f7;border-radius:999px;overflow:hidden;margin-top:10px}
        .bar > i{display:block;height:100%;width:0;background:linear-gradient(90deg,var(--accent-2),var(--accent));border-radius:inherit}

        /* Wide panel */
        .panel{background:var(--card);padding:16px;border-radius:12px;box-shadow:0 6px 20px rgba(15,23,42,0.04)}
        .panel h4{margin:0 0 8px 0;font-size:14px}
        .cols{display:grid;grid-template-columns:1fr 360px;gap:14px}

        /* logs */
        .logs{background:#0b1220;color:#cbd5e1;padding:12px;border-radius:8px;font-family:ui-monospace, SFMono-Regular, Menlo, Monaco, "Roboto Mono", monospace;font-size:12px;max-height:220px;overflow:auto}
        .muted{color:var(--muted)}

        /* timeline */
        .timeline{display:flex;flex-direction:column;gap:8px}
        .t-item{display:flex;gap:10px;align-items:flex-start}
        .dot{width:10px;height:10px;border-radius:999px;background:#e6eefb;margin-top:6px;border:3px solid #fff;box-shadow:0 0 0 4px rgba(37,99,235,0.06)}
        .t-body{font-size:13px}
        .chip{display:inline-block;padding:6px 8px;border-radius:8px;background:#f1f5f9;font-size:12px;color:#0b1220;margin-left:8px}

        footer{margin-top:10px;font-size:12px;color:var(--muted)}
        pre.snip{background:#0f172a;color:#dbeafe;padding:12px;border-radius:8px;font-size:12px;overflow:auto}

        @media (max-width:900px){
          .grid{grid-template-columns:1fr; padding:0 12px}
          .cards{grid-template-columns:repeat(2,1fr)}
          .cols{grid-template-columns:1fr}
        }
      </style>
    </head>
    <body>
      <div class="frame">
        <div class="grid" role="main" aria-label="Company portal">
          <aside class="sidebar">
            <div class="brand">
              <div class="logo">A51</div>
              <div>
                <p class="org">Area51 Systems</p>
                <p class="org-sub">Internal Developer Portal</p>
              </div>
            </div>

            <nav class="nav">
              <a>Overview <span class="note">System snapshot & health</span></a>
              <a>Releases <span class="note">Last deployment: 3 days ago</span></a>
              <a>Audit Logs <span class="note">Read-only</span></a>
              <a>Support <span class="note">Contact your rep</span></a>
            </nav>

            <div class="side-card">
              <div style="display:flex;justify-content:space-between;align-items:center">
                <div>
                  <div style="font-size:13px;font-weight:700">Environment</div>
                  <div class="muted" style="font-size:12px">Production / Global</div>
                </div>
                <div style="text-align:right">
                  <div class="pill">v2.4.9</div>
                </div>
              </div>

              <div style="margin-top:12px;font-size:12px;color:var(--muted)">Masked keys</div>
              <div style="margin-top:8px;font-family:ui-monospace,monospace;font-size:12px;color:#0b1220">
                <div>API_KEY: <strong>****-****-a3f9</strong></div>
                <div style="margin-top:6px">ADMIN_TOKEN: <strong>****-****-7b2c</strong></div>
              </div>
            </div>

            <div style="margin-top:12px;font-size:12px;color:var(--muted)">Quick status</div>
            <div style="display:flex;gap:8px;margin-top:8px">
              <div class="pill">DB OK</div>
              <div class="pill">Queue OK</div>
              <div class="pill">Ingress OK</div>
            </div>
          </aside>

          <main class="main">
            <header class="header">
              <div>
                <h1 class="title">Portal Dashboard</h1>
                <div class="subtitle">Operational snapshot • read-only interface</div>
              </div>
              <div class="muted">Last sync: Oct 13, 2025 — 22:18 UTC</div>
            </header>

            <section class="cards">
              <div class="card">
                <h3>Active Services</h3>
                <div class="stat">12</div>
                <div class="meta">Services currently deployed across clusters</div>
              </div>

              <div class="card">
                <h3>Incident Score</h3>
                <div class="stat">1 / 100</div>
                <div class="meta">Low operational risk</div>
                <div class="bar"><i style="width:4%"></i></div>
              </div>

              <div class="card">
                <h3>Storage Usage</h3>
                <div class="stat">412 GB</div>
                <div class="meta">of 2 TB allocated</div>
                <div class="bar"><i style="width:20%"></i></div>
              </div>
            </section>

            <section class="panel cols">
              <div>
                <h4>Recent activity</h4>
                <div class="panel" style="margin-bottom:12px">
                  <div class="timeline">
                    <div class="t-item"><div class="dot"></div><div class="t-body"><strong>2025-10-13 21:30</strong> — Scheduled backup completed <span class="chip">backup</span></div></div>
                    <div class="t-item"><div class="dot"></div><div class="t-body"><strong>2025-10-13 18:02</strong> — Service rollforward to v2.4.9 <span class="chip">deploy</span></div></div>
                    <div class="t-item"><div class="dot"></div><div class="t-body"><strong>2025-10-12 09:12</strong> — Certificate rotation (automated) <span class="chip">security</span></div></div>
                  </div>
                </div>

                <h4>System logs (read-only)</h4>
                <div class="logs">
[2025-10-13 21:30:01] system.backup: snapshot complete (duration=00:07:12)
[2025-10-13 18:02:44] deploy.worker: release v2.4.9 promoted to prod
[2025-10-13 17:59:12] ingress.proxy: rotated cert for *.area51.internal
[2025-10-13 03:10:08] maintenance: db vacuum completed, reclaimed 1.1G
[2025-10-12 11:03:55] scheduler: queue length stable (<= 3)
                </div>
              </div>

              <aside>
                <div class="panel" style="margin-bottom:12px">
                  <h4>Service health</h4>
                  <div style="display:flex;flex-direction:column;gap:10px">
                    <div>
                      <div style="font-size:13px">Auth Service <span class="muted" style="float:right">OK</span></div>
                      <div class="bar"><i style="width:88%"></i></div>
                    </div>
                    <div>
                      <div style="font-size:13px">API Gateway <span class="muted" style="float:right">OK</span></div>
                      <div class="bar"><i style="width:92%"></i></div>
                    </div>
                    <div>
                      <div style="font-size:13px">Internal API <span class="muted" style="float:right">Degraded</span></div>
                      <div class="bar"><i style="width:60%"></i></div>
                    </div>
                  </div>
                </div>

                <div class="panel">
                  <h4>Developer notes</h4>
                  <div class="muted" style="font-size:13px">Minimal info. Contact support for credentials.</div>
                  <pre class="snip"># sample config (redacted)
service:
  name: internal-api
  replicas: 3
  endpoint: https://api.area51.internal/redacted
                  </pre>
                </div>
              </aside>
            </section>

            <section class="panel">
              <h4>Audit snapshot</h4>
              <div style="display:flex;gap:12px;flex-wrap:wrap">
                <div style="min-width:180px" class="card">
                  <div style="font-size:12px;color:var(--muted)">Active sessions</div>
                  <div style="font-weight:700;margin-top:6px">18</div>
                </div>
                <div style="min-width:180px" class="card">
                  <div style="font-size:12px;color:var(--muted)">Open tickets</div>
                  <div style="font-weight:700;margin-top:6px">2</div>
                </div>
                <div style="min-width:180px" class="card">
                  <div style="font-size:12px;color:var(--muted)">Pending PRs</div>
                  <div style="font-weight:700;margin-top:6px">5</div>
                </div>
              </div>
            </section>

            <footer>
              &copy; Area51 Systems — Confidential internal portal. <span class="muted">For authorized personnel only.</span>
            </footer>
          </main>
        </div>
      </div>
    </body>
    </html>
    """

@app.route("/fetch")
def fetch():
    url = request.args.get("url")
    if not url:
        return "Missing URL", 400

    # naive SSRF filter
    if re.search(r"127\\.0\\.0\\.1|0\\.0\\.0\\.0|169\\.254", url):
        return "Access Denied", 403

    try:
        r = requests.get(url, timeout=3)
        return (r.text, r.status_code)
    except Exception as e:
        return str(e), 500

@app.route("/fetch_with_headers", methods=["POST"])
def fetch_with_headers():
    url = request.form.get("url")
    headers_json = request.form.get("headers", "{}")

    try:
        headers = json.loads(headers_json)
    except Exception as e:
        return f"Invalid header JSON: {e}", 400

    try:
        r = requests.get(url, headers=headers, timeout=5)
        return (r.text, r.status_code)
    except Exception as e:
        return str(e), 500

if __name__ == "__main__":
    # For Render: PORT environment variable is required
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
