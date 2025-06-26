import os
from dotenv import load_dotenv
from openai import OpenAI
import json

load_dotenv()

client = OpenAI(
    api_key = os.getenv("OPENAI_API")
)

output_dir = os.path.join(os.path.dirname(__file__))
data_dir = os.path.join(output_dir, "..")
products_file = os.path.join(data_dir, "products.json")
output_path = os.path.join(output_dir, "text_embeddings.json")
products = []

with open(products_file, "r", encoding = "utf-8") as f:
    products = json.load(f)

text_embeddings = []

# gets the text embeddings for each product using the title and description, then saves them to a json file
for product in products:
    product_id = str(product["id"])
    product_title = product["title"]
    product_description = product["description"]

    try:
        response = client.embeddings.create(
            model = "text-embedding-3-small",
            input = f"{product_title}, {product_description}"
        )

        text_embeddings.append({
                "id": product_id,
                "title": product_title,
                "embedding": response.data[0].embedding
            })

    except Exception as e:
        print(f"Error embedding product {product_id}: {e}")

with open(output_path, "w", encoding = "utf-8") as f:
    json.dump(text_embeddings, f)