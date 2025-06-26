from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key = os.getenv("OPENAI_API")
)

response = client.responses.create(
            model="gpt-4o-mini",
            input=[{
                "role": "user",
                "content": "what can you do?"
            }],
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

print(response.output_text)