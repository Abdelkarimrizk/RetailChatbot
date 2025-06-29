from flask import Blueprint, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv
import os
from agent.tools.image_search import image_search
from agent.tools.recommend import recommend
from io import BytesIO
from PIL import Image
import base64

load_dotenv()

general_bp = Blueprint("chat", __name__)

client = OpenAI(
    api_key = os.getenv("OPENAI_API")
)

# Checks if the user is asking for a recommendation, returns a bool value
def is_recommendation(message):
    keywords = ["recommend", "recommendation", "suggest", "suggestion", "do you have", "do you sell", "looking for", "looking to buy"]
    if any(keyword in message.lower() for keyword in keywords):
        return True
    
    response = client.responses.create(
        model = "gpt-4.1-nano",
        input = [
            {"role": "user", 
             "content": (
                 "Message: \n"
                 f"{message} \n\n"
                 "Answer with only 'yes' or 'no'."
                )
             }
        ],
        instructions=("You are a binary classifier that ONLY answers with 'yes' or 'no'. \n"
                     "Your task it to determine if the user is asking for a product recommendation. \n"
                     "Do not explain. Do not include any other text. \n"
                     "If the user input includes the sentence 'do you have', answer with 'yes' \n"
                     "If it seems like the user is asking for a recommendation, answer with 'yes' \n"
                     "If the input contains 'recommend' or 'recommendation', answer with 'yes' \n"
                     "If the input contains 'suggest' or 'suggestion', answer with 'yes' \n"
                     ),
        temperature=0
    )

    result = response.output_text.strip().lower()
    print(result)
    return result == "yes"

# decodes the base64 image from frontend 
def decode_image(base64_str):
    if base64_str.startswith("data:image"):
        base64_str = base64_str.split(",")[1]
    image_data = base64.b64decode(base64_str)
    return Image.open(BytesIO(image_data)).convert("RGB")

@general_bp.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    message = data.get("message", "")
    image = data.get("image")
    history = data.get("history", [])

    if not message and not image:
        return jsonify({"error": "No message or image provided"}), 400
    
    # if there is an image or a recommendation request, it will be added to tool_output 
    tool_output = ""

    # adds the user message to history
    if message and not image:
        history.append({"role": "user", "content": message})

        # adds the recommendation to tool_output
        if is_recommendation(message):
            products = recommend(message)
            tool_output += ("The user is requesting a product recommendation. \n")
            if not products:
                tool_output += ("No products can be recommended. \n")
            else:
                tool_output += ("Here are some products that can be recommended: \n"
                                "\n".join(f"- title={product['title']}, price={product['price']}, description={product['description']}" for product in products) + "\n\n")
    
    # adds the image based product search output to tool_output
    else:
        if message: 
            history.append({"role": "user", "content": message})

        pil_image = decode_image(image)
        products = image_search(pil_image)
        tool_output += ("The user has uploaded an image. \n")
        if not products:
            tool_output += ("No products similar to the image were found. \n")
        else:
            tool_output += ("Here are some products that match the image: \n"
                            "\n".join(f"- title={product['title']}, price={product['price']}, description={product['description']}" for product in products) + "\n\n")
    
    # adds the tool output to history, given that it exists
    if tool_output:
        history.append({"role": "assistant", "content": tool_output})
        print(f"Tool output added to history: {tool_output}")

    try:
        response = client.responses.create(
            model="gpt-4o-mini",
            input=history,
            instructions=(
                "You are a helpful assistant for an online store named FakeStore, Your name is Iris. \n"
                "You can ONLY: \n"
                " - Answer general questions about the store and its products. \n"
                " - Recommend products to the user based on their text input. \n"
                " - Find similar products based on user-uploaded images. \n"
                " You cannot help the user with purchasing products, you can only do what is stated above. \n"
                "When tool outputs (like product matches and recommendations) are provided in earlier assistant messages, "
                "you must use them as context for your response, do not repeat them word for word. \n"
                "Consider all messages when responding. \n"
                "If the user has uploaded an image, recommend all products that match the image. \n"
                "If you do not know the answer to a question, respond honestly and suggest that the user contact the store for support \n"
                "Do not make up any information, if you cannot find the product in the earlier messages, the product does not exist. \n"
                "If no products can be recommended, tell the user that there are no products like that. \n"
                "Always respond in a friendly and professional manner \n"
                "Always keep your answers as short as possible. \n"
                "Use bullet point lists when describing multiple features or steps, each bullet point must begin with -. each sentence must end with a full stop.\n"
                "The store sells all types of products, from clothing to electronics \n"
                "The website URL is https://fakestoreapi.com/ \n"
                "If the user asks a question that is not related to the store, its products, or your role, respond with 'I'm sorry, I don't know how to help with that.' \n"
            )
        )
        reply = response.output_text
        print(f"Assistant reply: {reply}")
        history.append({"role": "assistant", "content": reply})
        return jsonify({"reply": reply, "history": history})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
