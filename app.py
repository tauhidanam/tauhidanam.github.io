from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def scrape_product_info(product_name):
    """Scrape product info and image from Wikipedia and DuckDuckGo (no API)."""
    info = {"name": product_name, "description": "No description found.", "image": None}

    # Try Wikipedia first
    wiki_url = f"https://en.wikipedia.org/wiki/{product_name.replace(' ', '_')}"
    wiki_response = requests.get(wiki_url)

    if wiki_response.status_code == 200:
        soup = BeautifulSoup(wiki_response.text, "html.parser")
        paragraphs = soup.select("p")
        if paragraphs:
            info["description"] = paragraphs[0].get_text().strip()

        img_tag = soup.select_one("table.infobox img")
        if img_tag and img_tag.get("src"):
            info["image"] = "https:" + img_tag["src"]

    # If no image found, use DuckDuckGo
    if not info["image"]:
        duck_url = f"https://duckduckgo.com/?q={product_name}+electronic+component&iax=images&ia=images"
        headers = {"User-Agent": "Mozilla/5.0"}
        duck_page = requests.get(duck_url, headers=headers).text
        soup = BeautifulSoup(duck_page, "html.parser")
        img_tag = soup.find("img")
        if img_tag and img_tag.get("src"):
            info["image"] = img_tag["src"]

    return info


@app.route("/", methods=["GET", "POST"])
def index():
    product_info = None
    if request.method == "POST":
        product_name = request.form.get("product_name")
        product_info = scrape_product_info(product_name)
    return render_template("index.html", product_info=product_info)


if __name__ == "__main__":
    app.run(debug=True)
