from flask import Flask, jsonify
import uuid, secrets
import os

app = Flask(__name__)

INSTANCE_ID = str(uuid.uuid4())
SECRET_PART = secrets.token_hex(16)

@app.route("/instance-info")
def instance_info():
    return jsonify({
        "instance-id": INSTANCE_ID,
        "secret-part": SECRET_PART
    })

if __name__ == "__main__":
    # Render provides the PORT env variable
    port = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=port)

