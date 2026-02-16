from flask import Flask, jsonify
import os
import requests

app = Flask(__name__)

RCLONE_RC_URL = os.getenv("RCLONE_RC_URL")
RCLONE_RC_USER = os.getenv("RCLONE_RC_USER")
RCLONE_RC_PASS = os.getenv("RCLONE_RC_PASS")

def rclone_call(endpoint):
    try:
        response = requests.post(
            f"{RCLONE_RC_URL}/{endpoint}",
            auth=(RCLONE_RC_USER, RCLONE_RC_PASS),
            timeout=10
        )
        return response.json()
    except Exception as e:
        return {"error": str(e)}

@app.route("/")
def home():
    return jsonify({"status": "Backend Running"})

@app.route("/api/version")
def version():
    return jsonify(rclone_call("core/version"))

@app.route("/api/stats")
def stats():
    return jsonify(rclone_call("core/stats"))

@app.route("/api/remotes")
def remotes():
    return jsonify(rclone_call("config/listremotes"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
