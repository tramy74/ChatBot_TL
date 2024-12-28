import os
from dotenv import load_dotenv
import numpy as np
from backend.app.utils import db
import llamindex
import openai
import psycopg2
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.database import Embedding, SessionLocal
from main import SessionLocal

load_dotenv()  # Load environment variables from .env

# Access API key and database URL
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")

def store_embedding(text, embedding):
    # Store text and embedding in the PostgreSQL database
    embedding_entry = Embedding(text=text, embedding=embedding)
    db.add(embedding_entry)
    db.commit()

def get_relevant_embeddings(query_embedding, threshold=0.75):
    # Fetch embeddings from the database and compute similarity
    embeddings = db.query(Embedding).all()
    relevant_embeddings = []
    for embedding in embeddings:
        similarity = compute_similarity(query_embedding, embedding.embedding)
        if similarity >= threshold:
            relevant_embeddings.append((embedding.text, similarity))
    return relevant_embeddings

def compute_similarity(vector1, vector2):
    # Compute cosine similarity or another metric for retrieval
    return np.dot(vector1, vector2) / (np.linalg.norm(vector1) * np.linalg.norm(vector2))

def embed_text(text):
    # Use OpenAI or another embedding model
    response = openai.Embedding.create(input=text, model="text-embedding-ada-002")
    return response["data"][0]["embedding"]

def retrieve_and_answer(query):
    query_embedding = embed_text(query)
    relevant_texts = get_relevant_embeddings(query_embedding)
    combined_text = " ".join([text for text, _ in relevant_texts])

    # Generate answer using RAG and OpenAI
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"Based on the following text, answer the question: {query} \n\n Context: {combined_text}",
        max_tokens=100
    )
    return response["choices"][0]["text"].strip()