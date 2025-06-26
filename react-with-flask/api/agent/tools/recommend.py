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

# extracts what the user needs a recommendation for
def extract_recommendation(message):
    try:
        response = client.responses.create(
            model = "gpt-4o-mini",
            input = [{"role": "user", "content": message}],
            instructions= ("You extract the product the user is asking for a recommendation for. \n"
                           "Only reply with a short clear phrase or sentence describing what the user wants \n"
                           "Do not include any other text. Do not include small talk or conversation starters. \n"
                           "Do not explain. Do not give any instructions. \n")
        )
        return response.output_text.strip()
    except Exception as e:
        print(e)
        return None
    
# https://platform.openai.com/docs/guides/embeddings

def get_embedding(text, model="text-embedding-3-small"):
    text = text.replace("\n", " ")
    return client.embeddings.create(input = [text], model=model).data[0].embedding

def cosine_similarity(a, b):
    if np.linalg.norm(a) == 0 or np.linalg.norm(b) == 0:
        return 0
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def recommend(message):
    query = extract_recommendation(message)
    if not query:
        return []
    
    try:
        query_embedding = np.array(get_embedding(query))
    except Exception as e:
        print(e)
        return []
    
    recommendations = []
    for product in products:
        product_id = str(product["id"])
        product_embedding = embedding_dict[product_id]

        similarity = cosine_similarity(query_embedding, product_embedding)
        if similarity > 0.4:
            recommendations.append((similarity, product))
        
        recommendations.sort(key = lambda x: x[0], reverse = True)
        
    return [product for _, product in recommendations[:10]]

