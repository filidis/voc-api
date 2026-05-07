from flask import Flask, jsonify
import json
import os
import subprocess

app = Flask(__name__)

CACHE_FILE = "voc_cache.json"


@app.route("/")
def home():
    return jsonify({"status": "ok"})


# -----------------------------
# GERAÇÃO (chamado pelo Sheets)
# -----------------------------
@app.route("/generate-voc")
def generate_voc():

    try:
        subprocess.run(["python", "generate_voc.py"], check=True)

        return jsonify({"status": "generated"})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# -----------------------------
# LEITURA (Sheets usa isso)
# -----------------------------
@app.route("/voc")
def voc():

    if not os.path.exists(CACHE_FILE):
        return jsonify({"error": "cache not found"}), 404

    with open(CACHE_FILE, "r") as f:
        return jsonify(json.load(f))
