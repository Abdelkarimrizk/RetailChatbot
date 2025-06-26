from flask import Blueprint, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv
import os
from agent.tools.image_search import image_search
from agent.tools.recommend import recommend

load_dotenv()

general_bp = Blueprint("chat", __name__)

client = OpenAI(
    api_key = os.getenv("OPENAI_API")
)

# Checks if the user is asking for a recommendation, returns a bool value
def is_recommendation(message):
    response = client.responses.create(
        model = "gpt-4o-mini",
        input = [
            {"role": "user", 
             "content": (
                 "Message: \n"
                 f"{message} \n\n"
                 "Answer with only 'yes' or 'no'."
                )
             }
        ],
        instructions=("You are a binary classifier that ONLY answers with 'yes' or 'no'."
                     "Your task it to determine if the user is asking for a product recommendation."
                     "Do not explain. Do not include any other text."
                     ),
        temperature=0
    )

    result = response.output_text.strip().lower()
    return result == "yes"

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
    if message:
        history.append({"role": "user", "content": message})

        # adds the recommendation to tool_output
        if is_recommendation(message):
            products = recommend(message)
            tool_output += ("The user is requesting a product recommendation. \n")
            if not products:
                tool_output += ("No products can be recommended. \n")
            else:
                tool_output += ("Here are some products that can be recommended: \n"
                                "\n".join(f"- title={product['title']}, price={product['price']}" for product in products) + "\n\n")
    
    # adds the image based product finds to tool_output
    elif image:
        products = image_search(image)
        tool_output += ("The user has uploaded an image. \n")
        if not products:
            tool_output += ("No products similar to the image were found. \n")
        else:
            tool_output += ("Here are some products that match the image: \n"
                            "\n".join(f"- title={product['title']}, price={product['price']}" for product in products) + "\n\n")
    
    # adds the tool output to history, given that it exists
    if tool_output:
        history.append({"role": "assistant", "content": tool_output})

    try:
        response = client.responses.create(
            model="gpt-4o-mini",
            input=history,
            instructions=(
                "You are a helpful assistant for a commerce website for an online store named FakeStore. \n"
                "You can: \n"
                " - Answer general questions about the store and its products. \n"
                " - Recommend products to the user based on their text input. \n"
                " - Find similar products based on user-uploaded images. \n"
                "When tool outputs (like product matches and recommendations) are provided in earlier assistant messages, "
                "you must use them as context for your response, do not repeat them word for word. \n"
                "If you do not know the answer to a question, respond honestly and suggest that the user contact the store for support \n"
                "Always respond in a friendly, professional, and concise manner. \n"
                "The store sells all types of products, from clothing to electronics \n"
                "The website URL is https://fakestoreapi.com/ \n"
                "If the user asks a question that is not related to the store, its products, or your role, respond with 'I'm sorry, I don't know how to help with that.' \n"
            )
        )
        reply = response.output_text
        history.append({"role": "assistant", "content": reply})
        return jsonify({"reply": reply, "history": history})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
