import requests
from bs4 import BeautifulSoup
import json
import random

# Path to your products JSON
PRODUCTS_FILE = "data/products.json"

# Example products to fetch
product_keywords = [
    "5V relay module",
    "220 ohm resistor",
    "6V DC motor",
    "Arduino sensor",
    "capacitor 100uF",
    "LED 5mm",
    "servo motor",
    "transistor NPN",
    "microcontroller ESP32"
]

def scrape_product_info(keyword):
    """Scrape product description and image from Wikipedia (fallback to DuckDuckGo image search)"""
    info = {
        "name": keyword.title(),
        "description": "No description available",
        "image": None,
        "price": round(random.uniform(0.5, 15.0), 2)  # Random price for demo
    }

    # Wikipedia search
    wiki_url = f"https://en.wikipedia.org/wiki/{keyword.replace(' ', '_')}"
    r = requests.get(wiki_url)
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, "html.parser")
        p = soup.find("p")
        if p:
            info["description"] = p.get_text(strip=True)
        img_tag = soup.select_one("table.infobox img")
        if img_tag and img_tag.get("src"):
            info["image"] = "https:" + img_tag["src"]

    # If no image, use DuckDuckGo
    if not info["image"]:
        search_url = f"https://duckduckgo.com/?q={keyword}+electronic+component&iax=images&ia=images"
        headers = {"User-Agent": "Mozilla/5.0"}
        page = requests.get(search_url, headers=headers).text
        soup = BeautifulSoup(page, "html.parser")
        img_tag = soup.find("img")
        if img_tag and img_tag.get("src"):
            info["image"] = img_tag["src"]

    return info

def load_existing_products():
    try:
        with open(PRODUCTS_FILE, "r") as f:
            return json.load(f)
    except:
        return []

def save_products(products):
    with open(PRODUCTS_FILE, "w") as f:
        json.dump(products, f, indent=2)

def main():
    products = load_existing_products()
    next_id = max([p["id"] for p in products], default=0) + 1

    for keyword in product_keywords:
        print(f"Adding product: {keyword}")
        info = scrape_product_info(keyword)
        info["id"] = next_id
        next_id += 1
        products.append(info)

    save_products(products)
    print(f"✅ Added {len(product_keywords)} products successfully!")

if __name__ == "__main__":
    main()
