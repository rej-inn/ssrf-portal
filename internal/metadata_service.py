from flask import Flask, jsonify
import uuid, secrets

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
    app.run(host="127.0.0.1", port=5001)
