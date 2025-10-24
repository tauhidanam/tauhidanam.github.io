from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# Product details (placeholder)
@app.route('/product/<name>')
def product(name):
    # Dummy example (replace later with real API or manual data)
    specs = {
        "relay": {
            "name": "5V Relay Module",
            "description": "Single channel relay module for Arduino, rated 10A/250V.",
            "price": "$2.50",
            "image": "https://upload.wikimedia.org/wikipedia/commons/4/4b/5V_Relay_Module.jpg"
        },
        "resistor": {
            "name": "220 Ohm Resistor",
            "description": "Standard ¼ watt resistor, color code: red-red-brown.",
            "price": "$0.05",
            "image": "https://upload.wikimedia.org/wikipedia/commons/8/89/Resistor.jpg"
        },
        "motor": {
            "name": "DC Motor 6V",
            "description": "Small brushed DC motor ideal for DIY electronics.",
            "price": "$3.00",
            "image": "https://upload.wikimedia.org/wikipedia/commons/6/6b/DC_motor.jpg"
        }
    }

    product = specs.get(name.lower(), None)
    if not product:
        return f"Product '{name}' not found.", 404

    return render_template('product.html', product=product)


if __name__ == "__main__":
    app.run(debug=True)
