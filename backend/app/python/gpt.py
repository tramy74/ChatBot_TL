# gpt.py
import openai
from fastapi import HTTPException
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Function to generate response using GPT-4o model
def generate_gpt4o_response(prompt: str, max_tokens: int, temperature: float):
    try:
        # Generate a response from the GPT-4o model
        response = openai.ChatCompletion.create(
            model="gpt-4o",  # Specify the model you're using
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens,
            temperature=temperature  # Adjust as needed
        )
        return response.choices[0].message['content']
    except openai.error.OpenAIError as e:
        print(f"OpenAI API error: {e}")  # Log the OpenAI-specific error
        raise HTTPException(status_code=500, detail="Failed to generate response due to OpenAI API error")
    except Exception as e:
        print(f"Error generating response: {e}")  # Log the error
        raise HTTPException(status_code=500, detail="Failed to generate response")

# Function to generate embeddings for a prompt
def generate_embedding(prompt: str, model="text-embedding-ada-002"):
    try:
        # Generate embeddings for the input prompt
        response = openai.Embedding.create(
            input=prompt,
            model=model
        )
        return response['data'][0]['embedding']  # Extract the embedding vector
    except openai.error.OpenAIError as e:
        print(f"OpenAI API error: {e}")  # Log the OpenAI-specific error
        raise HTTPException(status_code=500, detail="Failed to generate embedding due to OpenAI API error")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
