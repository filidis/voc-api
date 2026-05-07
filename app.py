from flask import Flask, jsonify
import json
import os

app = Flask(__name__)

CACHE_FILE = "voc_cache.json"


@app.route("/")
def home():
    return jsonify({"status": "ok"})


@app.route("/voc")
def voc():

    if not os.path.exists(CACHE_FILE):
        return jsonify({
            "error": "cache not generated yet"
        })

    with open(CACHE_FILE, "r") as f:
        data = json.load(f)

    return jsonify(data)
