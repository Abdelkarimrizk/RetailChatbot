from transformers import pipeline
from PIL import Image
import os
import json
import numpy as np

mod = "google/vit-base-patch16-224"
pipe =  pipeline(task="image-feature-extraction", model_name=mod)

current_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(current_dir, "../data")
products_file = os.path.join(data_dir, "products.json")
embeddings_file = os.path.join(data_dir, "embedding/image_embeddings.json")

products = []
embeddings = []

with open(products_file, "r", encoding = "utf-8") as f:
    products = json.load(f)

with open(embeddings_file, "r", encoding = "utf-8") as f:
    embeddings = json.load(f)

embedding_dict = {}

for item in embeddings:
    embedding_dict[item["id"]] = np.array(item["embedding"])

def get_embedding(image):
    outputs = pipe(image)
    pooled = np.array(outputs[0]).mean(axis=0) 
    return pooled

def cosine_similarity(a, b):
    if np.linalg.norm(a) == 0 or np.linalg.norm(b) == 0:
        return 0
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def image_search(image):
    try:
        image_embedding = get_embedding(image)
    except Exception as e:
        print(e)
        return []
    
    recommendations = []
    for product in products:
        product_id = str(product["id"])
        product_embedding = embedding_dict[product_id]

        similarity = cosine_similarity(image_embedding, product_embedding)
        if similarity > 0.4:
            recommendations.append((similarity, product))
        
        recommendations.sort(key = lambda x: x[0], reverse = True)
        
    return [product for _, product in recommendations[:10]]

