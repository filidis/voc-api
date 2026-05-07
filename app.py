from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({"status": "ok", "message": "VOC API running"})

@app.route("/voc")
def voc():
    return jsonify({
        "timezone": "UTC",
        "voc": [
            {
                "inicio": "2026-05-07T10:00:00Z",
                "fim": "2026-05-07T13:00:00Z"
            }
        ]
    })

# IMPORTANTE: Render exige isso
port = int(os.environ.get("PORT", 10000))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=port)
