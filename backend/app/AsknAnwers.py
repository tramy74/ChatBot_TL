import os
import openai
import psycopg2
from dotenv import load_dotenv
from llama_index.core import Document, VectorStoreIndex

# Load environment variables
load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
openai.api_key = OPENAI_API_KEY

# Connect to PostgreSQL
def connect_to_db():
    conn = psycopg2.connect(DATABASE_URL)
    return conn

def embed_and_store_document(content):
    # Embed document content using LlamaIndex or OpenAI's API
    embedding = openai.Embedding.create(input=content, model="text-embedding-ada-002")["data"][0]["embedding"]
    conn = connect_to_db()
    cursor = conn.cursor()

    # Store embedding and content
    cursor.execute("""
        INSERT INTO document_embeddings (content, embedding) VALUES (%s, %s);
    """, (content, embedding))
    conn.commit()
    cursor.close()
    conn.close()

def handle_user_question(question):
    # Embed the question
    question_embedding = openai.Embedding.create(input=question, model="text-embedding-ada-002")["data"][0]["embedding"]

    conn = connect_to_db()
    cursor = conn.cursor()

    # Search for similar documents
    cursor.execute("""
        SELECT content FROM document_embeddings 
        ORDER BY embedding <-> %s 
        LIMIT 1;
    """, (question_embedding,))
    result = cursor.fetchone()

    # Generate a response
    if result:
        response = result[0]
    else:
        response = "No data available."

    # Log question and response
    cursor.execute("""
        INSERT INTO user_interactions (question, answer) VALUES (%s, %s);
    """, (question, response))
    conn.commit()
    cursor.close()
    conn.close()

    return response
