import openai
import os
from app.database import SessionLocal
from models.file_embedding import FileEmbedding

openai.api_key = os.getenv("OPENAI_API_KEY")

def read_file_content(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()

def get_text_embedding(text):
    response = openai.Embedding.create(input=text, model="text-embedding-ada-002")
    return response['data'][0]['embedding']

def save_embedding_to_db(filename, embedding):
    db = SessionLocal()
    try:
        file_embedding = FileEmbedding(filename=filename, embedding=embedding)
        db.add(file_embedding)
        db.commit()
    except Exception as e:
        db.rollback()
        print("Error saving to database:", e)
    finally:
        db.close()

def process_and_store_file(file_path):
    content = read_file_content(file_path)
    embedding = get_text_embedding(content)
    save_embedding_to_db(filename=os.path.basename(file_path), embedding=embedding)
