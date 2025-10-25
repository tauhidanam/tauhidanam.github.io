from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

# Load products
with open("products.json") as f:
    products = json.load(f)

def search_filter_products(query="", category=""):
    results = []
    for p in products:
        if (query.lower() in p["name"].lower() or query.lower() in p["description"].lower()) and \
           (category == "" or category == p["category"]):
            results.append(p)
    return results

@app.route("/")
def home():
    query = request.args.get("q", "")
    category = request.args.get("category", "")
    filtered = search_filter_products(query, category)
    categories = sorted(list({p["category"] for p in products}))
    return render_template("index.html", products=filtered, query=query, categories=categories, selected=category)

@app.route("/product/<int:pid>")
def product_page(pid):
    product = next((p for p in products if p["id"] == pid), None)
    related = [p for p in products if p["category"] == product["category"] and p["id"] != pid][:4]
    return render_template("product.html", product=product, related_products=related)

if __name__ == "__main__":
    app.run(debug=True)
