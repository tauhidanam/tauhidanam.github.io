import random
import json

categories = ["Sensors", "Motors", "3D Printer Parts", "Microcontrollers", "Displays", "Power Supply", "Modules"]

products = []
for i in range(1, 101):  # 100 products
    category = random.choice(categories)
    name = f"{category} Model {1000 + i}"
    price = round(random.uniform(70, 3500), 2)
    stock = random.randint(5, 150)
    rating = round(random.uniform(3.5, 5.0), 1)
    model = f"M-{i:04d}"
    specs = {
        "Voltage": f"{random.randint(3, 24)}V",
        "Current": f"{round(random.uniform(0.1, 2.0), 2)}A",
        "Accuracy": f"{random.randint(1, 5)}%",
        "Temperature Range": f"{random.randint(-20, 0)}°C to {random.randint(50, 125)}°C"
    }

    product = {
        "id": i,
        "name": name,
        "price": price,
        "model": model,
        "stock": stock,
        "rating": rating,
        "category": category,
        "image": f"/static/images/product_{i}.jpg",
        "description": f"{name} is a reliable and efficient component suitable for various electronic applications.",
        "specs": specs
    }
    products.append(product)

with open("products.json", "w") as f:
    json.dump(products, f, indent=4)

print("✅ Generated 100 products and saved to products.json")
