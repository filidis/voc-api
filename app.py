from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({
        "status": "ok",
        "message": "VOC API running"
    })

@app.route("/voc")
def voc():

    # versão temporária funcional (garante deploy)
    # depois trocamos pelo Swiss Ephemeris real
    return jsonify({
        "timezone": "UTC",
        "voc": [
            {
                "inicio": "2026-05-07T10:00:00Z",
                "fim": "2026-05-07T13:00:00Z"
            }
        ]
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
