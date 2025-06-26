from openai import OpenAI
import os
from dotenv import load_dotenv
import json
import numpy as np

load_dotenv()

client = OpenAI(
    api_key = os.getenv("OPENAI_API")
)

current_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(current_dir, "../data")
products_file = os.path.join(data_dir, "products.json")
embeddings_file = os.path.join(data_dir, "embedding/text_embeddings.json")
products = []
embeddings = []

with open(products_file, "r", encoding = "utf-8") as f:
    products = json.load(f)

with open(embeddings_file, "r", encoding = "utf-8") as f:
    embeddings = json.load(f)

embedding_dict = {}

for item in embeddings:
    embedding_dict[item["id"]] = np.array(item["embedding"])
