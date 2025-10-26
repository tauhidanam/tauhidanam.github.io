from flask import Flask, render_template, request, redirect, url_for, jsonify
import json

app = Flask(__name__)

# Load product data
with open("products.json", "r") as f:
    products = json.load(f)

@app.route("/")
def home():
    q = request.args.get("q", "").lower()
    cat = request.args.get("category", "")
    filtered = []
    for p in products:
        if (not q or q in p["name"].lower()) and (not cat or cat == p["category"]):
            filtered.append(p)
    categories = sorted(list(set(p["category"] for p in products)))
    return render_template("index.html", products=filtered, categories=categories, q=q, cat=cat)

@app.route("/product/<int:pid>")
def product(pid):
    p = next((x for x in products if x["id"] == pid), None)
    if not p:
        return "Product not found", 404
    return render_template("product.html", p=p)

@app.route("/api/products")
def api_products():
    return jsonify(products)

if __name__ == "__main__":
    app.run(debug=True)
