import psycopg2
from llama_index.core import VectorStoreIndex
from app.utils.db_utils import connect_to_db

# Function to save vectors to the database
def save_vector_to_db(document_id, document_title, document_content, embedding_vector):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO document_vectors (document_id, document_title, document_content, embedding)
        VALUES (%s, %s, %s, %s)
    """, (document_id, document_title, document_content, embedding_vector))
    conn.commit()
    cursor.close()
    conn.close()

# Process document, generate embedding, and save to database
def process_and_save_document(document_text, document_title):
    # Assuming you have a method in LlamaIndex to generate an embedding
    index = VectorStoreIndex.from_documents([document_text])
    embedding = index.get_embedding()  # Replace with actual method to get embedding from LlamaIndex
    
    # Save to database
    save_vector_to_db(None, document_title, document_text, embedding)
