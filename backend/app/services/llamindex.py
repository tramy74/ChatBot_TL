import os
import psycopg2
from llama_index.core import VectorStoreIndex
from llama_index.core.node_parser import SimpleFileNodeParser
from llama_index.readers.file import FlatReader
from pathlib import Path
from llama_index.embeddings.openai import OpenAIEmbedding
from app.database import get_db  # Ensure this is defined to get a DB connection
from datetime import datetime
from psycopg2.extras import execute_values

# Function to connect to PostgreSQL
def connect_db():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )

# Function to save vectors into PostgreSQL
def save_embedding(content, content_type, vector, db_connection):
    with db_connection.cursor() as cursor:
        insert_query = """
        INSERT INTO embeddings (content_type, content, vector, created_at)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(insert_query, (content_type, content, vector, datetime.now()))
    db_connection.commit()

# Function to retrieve the closest vector
def retrieve_closest_embedding(query_vector, db_connection):
    with db_connection.cursor() as cursor:
        cursor.execute("""
        SELECT content, vector, 
               1 - (vector <-> %s) AS similarity -- Using PostgreSQL distance operator
        FROM embeddings
        ORDER BY similarity DESC
        LIMIT 1
        """, (query_vector,))
        result = cursor.fetchone()
    return result

# Main process for handling documents and questions
def process_content(content, content_type, embedder):
    vector = embedder.embed(content)
    
    # Save the embedding in the database
    db_connection = connect_db()
    save_embedding(content, content_type, vector, db_connection)
    db_connection.close()
    return vector

# Using LlamaIndex with embedded vectors
def answer_question(question, index):
    query_vector = process_content(question, "question", OpenAIEmbedding())

    # Retrieve the closest document from the database
    db_connection = connect_db()
    closest_doc = retrieve_closest_embedding(query_vector, db_connection)
    db_connection.close()
    
    if closest_doc:
        # Use retrieved content to generate answer
        response = index.query(question, retriever=closest_doc["content"])
        return response
    else:
        return "No relevant document found."

def generate_answer_with_rag(question, context_data):
    """
    This function generates an answer using retrieval-augmented generation (RAG).
    It first retrieves relevant documents from the provided context_data, 
    and then uses an LLM to generate an answer based on these retrieved documents.

    Parameters:
        question (str): The user’s question.
        context_data (list of dict): The context data where each item contains information such as 
                                     'title', 'text', or 'vector' of documents.

    Returns:
        str: Generated answer based on the retrieved documents.
    """

    # Initialize the VectorIndex (embedding store)
    vector_index = VectorStoreIndex(embedding_function=OpenAIEmbedding())

    # Populate the VectorIndex with context data
    for doc in context_data:
        vector_index.add(doc["text"], metadata={"title": doc["title"]})

    # Retrieve the most relevant documents
    retrieved_docs = vector_index.retrieve(question, top_k=5)

    # Combine retrieved documents for context
    context_text = "\n".join([doc["text"] for doc in retrieved_docs])

    # Generate an answer using an LLM
    answer = f"Answering based on retrieved context:\n{context_text}\nQuestion: {question}\nAnswer: The answer based on RAG."

    return answer

# Example usage
if __name__ == "__main__":
    # Load documents and create the index with embeddings
    documents = ["Document 1 content...", "Document 2 content..."]  # Replace with your actual document contents
    embedder = OpenAIEmbedding()
    db_connection = connect_db()

    # Process and store document embeddings
    for doc in documents:
        process_content(doc, "document", embedder)

    db_connection.close()
    
    # Build the index
    index = VectorStoreIndex.from_documents(documents, embedder=embedder)
    
    # Ask a question and retrieve an answer
    question = "What is Document 1 about?"
    answer = answer_question(question, index)
    print("Answer:", answer)
