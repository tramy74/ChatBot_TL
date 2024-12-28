import os
import logging
import sys
from dotenv import load_dotenv  # Import the library to load .env
from llama_index.llms.openai import OpenAI
from llama_index.core import VectorStoreIndex, Settings, Document
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Load environment variables
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Set up logging
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

# Initialize FastAPI
app = FastAPI()

# Database connection setup
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

# OpenAI setup for LlamaIndex
llm = OpenAI(temperature=0, model="gpt-4o", api_key=OPENAI_API_KEY)
Settings.llm = llm
Settings.chunk_size = 512

# Load documents from the database or file directory
def load_documents():
    # Example function to retrieve documents from PostgreSQL
    with SessionLocal() as session:
        # Replace 'your_table' with the name of your table storing text data
        result = session.execute("SELECT content FROM your_table")
        documents = [Document(text=row[0]) for row in result]
    return documents

# Initialize the index
documents = load_documents()
index = VectorStoreIndex.from_documents(documents)

# Define FastAPI request and response models
class QuestionRequest(BaseModel):
    question: str

class AnswerResponse(BaseModel):
    answer: str

# Define the query route
@app.post("/ask", response_model=AnswerResponse)
async def ask_question(request: QuestionRequest):
    question = request.question
    try:
        query_engine = index.as_query_engine(similarity_top_k=3, streaming=True)
        response = query_engine.query(question)
        answer = response.print_response_stream()  # Adjust based on response handling in LlamaIndex
        return AnswerResponse(answer=answer)
    except Exception as e:
        logging.error(f"Error processing question: {e}")
        raise HTTPException(status_code=500, detail="Error processing question")

# llamindex.py

def get_response(question):
    # Here, add logic to handle the question using RAG and LlamaIndex.
    # For example, you might retrieve documents, process embeddings, and generate answers.
    response = "This is a placeholder response."  # Replace with real logic.
    return response
