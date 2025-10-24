from flask import Flask, render_template, request, redirect, url_for
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def scrape_product_info(product_name):
    """Scrape product info and image from Wikipedia and DuckDuckGo (no API key)."""
    info = {
        "name": product_name.capitalize(),
        "description": "No description found.",
        "image": None,
        "specs": {}
    }

    # Try Wikipedia for description and image
    wiki_url = f"https://en.wikipedia.org/wiki/{product_name.replace(' ', '_')}"
    wiki_response = requests.get(wiki_url)

    if wiki_response.status_code == 200:
        soup = BeautifulSoup(wiki_response.text, "html.parser")

        # Description (first paragraph)
        paragraphs = soup.select("p")
        if paragraphs:
            info["description"] = paragraphs[0].get_text().strip()

        # Specs from infobox
        table = soup.select_one("table.infobox")
        if table:
            rows = table.select("tr")
            for row in rows:
                cells = row.find_all(["th", "td"])
                if len(cells) == 2:
                    key = cells[0].get_text(strip=True)
                    value = cells[1].get_text(strip=True)
                    info["specs"][key] = value

        # Image from infobox
        img_tag = soup.select_one("table.infobox img")
        if img_tag and img_tag.get("src"):
            info["image"] = "https:" + img_tag["src"]

    # If no image found, try DuckDuckGo
    if not info["image"]:
        search_url = f"https://duckduckgo.com/?q={product_name}+electronic+component&iax=images&ia=images"
        headers = {"User-Agent": "Mozilla/5.0"}
        duck_page = requests.get(search_url, headers=headers).text
        soup = BeautifulSoup(duck_page, "html.parser")
        img_tag = soup.find("img")
        if img_tag and img_tag.get("src"):
            info["image"] = img_tag["src"]

    return info


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/product", methods=["GET"])
def search_product():
    """Redirect search query to product page."""
    product_name = request.args.get("product_name")
    if not product_name:
        return redirect(url_for("index"))
    return redirect(url_for("product_page", name=product_name))


@app.route("/product/<name>")
def product_page(name):
    """Display individual product details."""
    product_info = scrape_product_info(name)
    return render_template("product.html", product_info=product_info)


if __name__ == "__main__":
    app.run(debug=True)
