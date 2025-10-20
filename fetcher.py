# fetcher.py
import os, sys, json, time, hashlib, requests
from pathlib import Path
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

BING_API_KEY = os.getenv("BING_API_KEY")
BING_ENDPOINT = os.getenv("BING_ENDPOINT", "https://api.bing.microsoft.com/v7.0/")
HEADERS = {"Ocp-Apim-Subscription-Key": BING_API_KEY}

OUT_DIR = Path("output")
IMAGES_DIR = OUT_DIR / "images"
PRODUCTS_JSON = OUT_DIR / "products.json"
OUT_DIR.mkdir(exist_ok=True)
IMAGES_DIR.mkdir(exist_ok=True)

def bing_search(api, query, count=5):
    url = f"{BING_ENDPOINT}{api}"
    resp = requests.get(url, headers=HEADERS, params={"q": query, "count": count, "mkt": "en-US"}, timeout=15)
    resp.raise_for_status()
    return resp.json()

def download_image(url):
    try:
        r = requests.get(url, stream=True, timeout=15)
        r.raise_for_status()
        parsed = urlparse(url)
        ext = os.path.splitext(parsed.path)[1] or ".jpg"
        fname = hashlib.sha1(url.encode()).hexdigest() + ext
        fpath = IMAGES_DIR / fname
        with open(fpath, "wb") as f:
            for chunk in r.iter_content(8192):
                f.write(chunk)
        return str(fpath)
    except Exception as e:
        print("Image download failed:", e)
        return None

def parse_product_page(url):
    data = {"url": url, "title": "", "description": "", "specs": {}}
    try:
        r = requests.get(url, timeout=15, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(r.text, "html.parser")
        if soup.title:
            data["title"] = soup.title.string.strip()
        desc = soup.find("meta", attrs={"name":"description"})
        if desc and desc.get("content"):
            data["description"] = desc["content"]
        for t in soup.find_all("table"):
            for row in t.find_all("tr"):
                cols = row.find_all(["td","th"])
                if len(cols) >= 2:
                    key = cols[0].get_text(strip=True)
                    val = cols[1].get_text(strip=True)
                    if key and val:
                        data["specs"][key] = val
    except Exception as e:
        print("Parse error:", e)
    return data

def gather_products(query, max_items=5):
    if not BING_API_KEY:
        print("ERROR: Missing BING_API_KEY in .env")
        return []
    print(f"Searching for '{query}'...")
    web = bing_search("search", query, max_items)
    images = bing_search("images/search", query, max_items)
    results = []
    for i, item in enumerate(web.get("webPages", {}).get("value", [])):
        url = item["url"]
        product = parse_product_page(url)
        product["source_name"] = item["name"]
        product["source_url"] = url
        if "value" in images and i < len(images["value"]):
            img_url = images["value"][i]["contentUrl"]
            product["image_path"] = download_image(img_url)
        results.append(product)
        time.sleep(1)
    with open(PRODUCTS_JSON, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"✅ Saved {len(results)} products to {PRODUCTS_JSON}")
    return results

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python fetcher.py \"5v relay\" [count]")
        sys.exit()
    q = sys.argv[1]
    c = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    gather_products(q, c)
