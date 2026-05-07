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
        return jsonify({"error": "cache not found"}), 404

    with open(CACHE_FILE, "r") as f:
        return jsonify(json.load(f))
