# app.py
from flask import Flask, render_template, send_from_directory, jsonify
import json
from pathlib import Path

app = Flask(__name__, static_folder="output/images")
PRODUCTS_JSON = Path("output/products.json")

@app.route("/")
def home():
    products = []
    if PRODUCTS_JSON.exists():
        with open(PRODUCTS_JSON, encoding="utf-8") as f:
            products = json.load(f)
    for p in products:
        if p.get("image_path"):
            p["image_url"] = "/" + p["image_path"].replace("\\", "/")
        else:
            p["image_url"] = None
    return render_template("index.html", products=products)

@app.route("/output/<path:filename>")
def serve_output(filename):
    return send_from_directory("output", filename)

@app.route("/products.json")
def api():
    if PRODUCTS_JSON.exists():
        with open(PRODUCTS_JSON, encoding="utf-8") as f:
            return jsonify(json.load(f))
    return jsonify([])

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
