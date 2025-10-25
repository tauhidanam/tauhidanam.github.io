from flask import Flask, render_template, request, jsonify
import json, os

app = Flask(__name__)

# Load product data
with open("products.json") as f:
    products = json.load(f)

@app.route("/")
def index():
    category = request.args.get("category")
    search = request.args.get("search", "").lower()

    filtered = [
        p for p in products
        if (not category or p["category"] == category)
        and (not search or search in p["name"].lower())
    ]
    return render_template("index.html", products=filtered, categories=sorted(set(p["category"] for p in products)))

@app.route("/api/products")
def api_products():
    return jsonify(products)

@app.route("/health")
def health():
    return "OK", 200  # Render health check endpoint

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
