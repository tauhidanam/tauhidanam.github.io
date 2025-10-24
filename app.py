import json
import os
from flask import Flask, render_template, request, redirect, url_for, session
import stripe
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
app.secret_key = "your_secret_key_here"

# Stripe setup (replace with your test key from https://dashboard.stripe.com/test/apikeys)
stripe.api_key = "sk_test_..."

# Load products
def load_products():
    with open("data/products.json") as f:
        return json.load(f)

@app.route('/')
def home():
    products = load_products()
    return render_template('index.html', products=products)

@app.route('/product/<int:pid>')
def product(pid):
    products = load_products()
    product = next((p for p in products if p["id"] == pid), None)
    return render_template('product.html', product=product)

@app.route('/add_to_cart/<int:pid>')
def add_to_cart(pid):
    products = load_products()
    product = next((p for p in products if p["id"] == pid), None)
    if not product:
        return "Product not found"

    cart = session.get("cart", [])
    cart.append(product)
    session["cart"] = cart
    return redirect(url_for("cart"))

@app.route('/cart')
def cart():
    cart = session.get("cart", [])
    total = sum(item["price"] for item in cart)
    return render_template("cart.html", cart=cart, total=total)

@app.route('/checkout', methods=["POST"])
def checkout():
    cart = session.get("cart", [])
    total = int(sum(item["price"] for item in cart) * 100)

    session["cart"] = []

    checkout_session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[
            {
                "price_data": {
                    "currency": "usd",
                    "product_data": {
                        "name": "Robohta Order"
                    },
                    "unit_amount": total,
                },
                "quantity": 1,
            },
        ],
        mode="payment",
        success_url=request.host_url + "success",
        cancel_url=request.host_url + "cart",
    )
    return redirect(checkout_session.url, code=303)

@app.route('/success')
def success():
    return "<h1>✅ Payment Successful! Thank you for shopping with Robohta Electronics.</h1>"

if __name__ == "__main__":
    app.run(debug=True)
