import json, random

categories = {
    "Sensors": [
        "NTC 100K Thermistor", "HC-SR04 Ultrasonic Sensor", "DHT11 Temperature Sensor", "PIR Motion Sensor", "IR Obstacle Sensor"
    ],
    "Motors": [
        "12V DC Gear Motor", "NEMA17 Stepper Motor", "Mini Servo SG90", "BLDC 2205 Motor", "28BYJ-48 Stepper Motor"
    ],
    "Microcontrollers": [
        "Arduino Uno R3", "ESP32 DevKit", "Raspberry Pi Pico", "NodeMCU ESP8266", "Arduino Nano"
    ],
    "Power": [
        "5V Relay Module", "LM2596 Buck Converter", "7805 Voltage Regulator", "12V Power Supply Adapter", "Lithium Battery Charger TP4056"
    ],
    "Passive Components": [
        "10K Resistor Pack", "100uF Capacitor", "1N4007 Diode", "10K Potentiometer", "220uH Inductor"
    ]
}

product_list = []
id_counter = 1

for category, items in categories.items():
    for _ in range(20):  # 20 per category = 100 total
        base_name = random.choice(items)
        model = f"{random.randint(1000,9999)}"
        price = round(random.uniform(0.5, 25.0), 2)
        stock = random.randint(5, 200)
        rating = random.randint(3, 5)
        reviews = random.randint(10, 500)
        image = f"https://robohta.me/static/images/{base_name.replace(' ', '_')}.jpg"

        specs = [
            f"Model: {model}",
            f"Category: {category}",
            f"Rated Voltage: {random.choice(['5V','12V','24V','3.3V'])}",
            f"Operating Temp: -20°C to {random.randint(60,120)}°C",
            f"Dimensions: {random.randint(5,40)}x{random.randint(5,40)} mm"
        ]

        details = [
            f"Ideal for hobbyists, robotics, and DIY projects.",
            f"Compatible with Arduino and Raspberry Pi.",
            f"High-quality build with long lifespan."
        ]

        product_list.append({
            "id": id_counter,
            "name": base_name,
            "model": model,
            "price": price,
            "category": category,
            "description": f"{base_name} is a high-quality component suitable for {category.lower()} applications.",
            "specs": specs,
            "details": details,
            "stock": stock,
            "image": image,
            "rating": rating,
            "reviews": reviews
        })
        id_counter += 1

with open("products.json", "w") as f:
    json.dump(product_list, f, indent=2)

print("✅ 100 products generated and saved to products.json")
