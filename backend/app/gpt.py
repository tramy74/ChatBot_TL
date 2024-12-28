import os
from dotenv import load_dotenv
import openai

# Load environment variables from .env file
load_dotenv()

# Access the API key
openai.api_key = os.getenv("OPENAI_API_KEY")

def create_prompt(document_content: str, user_query: str) -> str:
    prompt = (
        f"Context: {document_content}\n"
        f"Question: {user_query}\n"
        "Answer:"
    )
    return prompt

def query_gpt4o(document_content: str, user_query: str, max_tokens: int = 150):
    prompt = create_prompt(document_content, user_query)
    response = openai.Completion.create(
        model="gpt-4o",
        prompt=prompt,
        max_tokens=max_tokens,
        temperature=0.7
    )
    return response.choices[0].text.strip()


