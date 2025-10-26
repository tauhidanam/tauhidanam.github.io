import json, random

categories = [
    "Resistors", "Capacitors", "Transistors", "Motors", "Sensors",
    "Arduino", "Raspberry Pi", "Power Supply", "Tools", "LEDs"
]

products = []
for i in range(1, 101):
    category = random.choice(categories)
    price = random.randint(20, 1500)
    stock = random.randint(5, 50)
    product = {
        "id": i,
        "name": f"{category[:-1]} Model {1000+i}",
        "category": category,
        "price": price,
        "stock": stock,
        "image": f"https://source.unsplash.com/400x400/?{category},electronics",
        "description": f"High quality {category.lower()} for electronics projects. Ideal for students and hobbyists.",
    }
    products.append(product)

with open("products.json", "w") as f:
    json.dump(products, f, indent=2)

print("✅ 100 products generated successfully!")
