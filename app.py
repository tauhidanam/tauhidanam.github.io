from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import json, requests
from config import STORE_ID, STORE_PASS, BASE_URL, CURRENCY

app = Flask(__name__)
app.secret_key = "super_secret_robohta"

# Load product data
with open("products.json") as f:
    products = json.load(f)

@app.route("/")
def index():
    query = request.args.get("q", "").lower()
    category = request.args.get("category", "")
    filtered = [p for p in products if query in p["name"].lower()]
    if category:
        filtered = [p for p in filtered if p["category"] == category]
    categories = sorted(set(p["category"] for p in products))
    return render_template("index.html", products=filtered, categories=categories, query=query, selected_category=category)

@app.route("/product/<int:pid>")
def product_page(pid):
    product = next((p for p in products if p["id"] == pid), None)
    return render_template("product.html", product=product)

@app.route("/cart")
def cart():
    cart_items = session.get("cart", [])
    total = sum(p["price"] for p in cart_items)
    return render_template("cart.html", cart=cart_items, total=total)

@app.route("/add_to_cart/<int:pid>")
def add_to_cart(pid):
    cart = session.get("cart", [])
    product = next((p for p in products if p["id"] == pid), None)
    if product:
        cart.append(product)
        session["cart"] = cart
    return redirect(url_for("cart"))

@app.route("/checkout")
def checkout():
    cart = session.get("cart", [])
    total = sum(p["price"] for p in cart)
    return render_template("checkout.html", total=total)

@app.route("/process_payment", methods=["POST"])
def process_payment():
    total = request.form.get("total")
    post_data = {
        "store_id": STORE_ID,
        "store_passwd": STORE_PASS,
        "total_amount": total,
        "currency": CURRENCY,
        "tran_id": "RHTA12345",
        "success_url": request.url_root + "success",
        "fail_url": request.url_root + "fail",
        "cancel_url": request.url_root + "cancel",
        "cus_name": "Test Buyer",
        "cus_email": "test@robohta.me",
        "cus_add1": "Dhaka",
        "cus_phone": "01700000000",
    }
    response = requests.post(BASE_URL, data=post_data)
    try:
        redirect_url = response.json().get("GatewayPageURL")
        return redirect(redirect_url)
    except:
        return "Payment initiation failed."

@app.route("/success")
def success():
    session["cart"] = []
    return "✅ Payment Successful! Thank you for shopping with RoboHTA Electronics."

@app.route("/fail")
def fail():
    return "❌ Payment Failed."

@app.route("/cancel")
def cancel():
    return "⚠️ Payment Cancelled."

if __name__ == "__main__":
    app.run(debug=True)
