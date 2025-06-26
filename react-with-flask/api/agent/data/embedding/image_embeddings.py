# using the following hugging face model
# https://huggingface.co/google/vit-base-patch16-224
# because I found it in:
# https://huggingface.co/docs/transformers/en/tasks/image_feature_extraction

from transformers import pipeline
from PIL import Image
import os
import json
import numpy as np

model_name = "google/vit-base-patch16-224"
pipe =  pipeline(task="image-feature-extraction", model_name=model_name)

output_dir = os.path.dirname(__file__)
output_path = os.path.join(output_dir, "image_embeddings.json")
data_dir = os.path.join(output_dir, "..")
image_dir = os.path.join(data_dir, "images")

embeddings = []

# converts the images to what I hope are embeddings, im putting full trust in the second link
for file in os.listdir(image_dir):
    product_id = file.replace(".jpg", "")
    image_path = os.path.join(image_dir, file)

    image = Image.open(image_path).convert("RGB")
    raw_output = pipe(image)
    output = np.array(raw_output[0]).mean(axis=0)
    embeddings.append({
        "id": product_id,
        "embedding": output.tolist()
    })

with open(output_path, "w", encoding = "utf-8") as f:
    json.dump(embeddings, f)

