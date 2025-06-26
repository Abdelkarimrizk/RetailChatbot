import os
import requests
import json 

FAKESTORE_URL = "https://fakestoreapi.com/products"

output_dir = os.path.join(os.path.dirname(__file__))
image_dir = os.path.join(output_dir, "images")
products_file = os.path.join(output_dir, "products.json")

response = requests.get(FAKESTORE_URL)
raw_products = response.json()

products = []

for p in raw_products:
    products.append({
        "id": p["id"],
        "title": p["title"],
        "price": p["price"],
        "description": p["description"],
        "image": p["image"]
    })

with open(products_file, "w", encoding = "utf-8") as f:
    json.dump(products, f, indent = 1)

for product in products:
    image_url = product["image"]
    product_id = product["id"]

    image_path = os.path.join(image_dir, f"{product_id}.jpg")
    
    image = requests.get(image_url).content

    with open(image_path, "wb") as f:
        f.write(image)

