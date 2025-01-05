from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from dotenv import load_dotenv
from llama_index.llms.openai import OpenAI
from llama_index.core import Settings
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from io import StringIO
import contextlib
import os

load_dotenv()

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load documents and set up the query engine
documents = SimpleDirectoryReader("D:\\DaiHoc\\ForthYear\\chatbot\\backend\\app\\data").load_data()
llm = OpenAI(temperature=0, model="gpt-4o")
Settings.llm = llm
Settings.chunk_size =512

index = VectorStoreIndex.from_documents(documents)
query_engine = index.as_query_engine(similarity_top_k=3, streaming=True)


class Query(BaseModel):
    question: str

# @app.post("/query")
# async def get_answer(query: Query, ):
#     response = query_engine.query(query.question)

#     # Capture and process the response stream
#     answer_stream = StringIO()
#     with contextlib.redirect_stdout(answer_stream):
#         response.print_response_stream()
#     answer = answer_stream.getvalue().strip()

#     # Handle empty or invalid responses
#     if not answer or "external source" in answer.lower():
#         answer = "Không có dữ liệu."

#     return {"answer": answer}

@app.post("/query")
async def get_answer(question: str = Form(...), file: UploadFile = None):
    file_info = None
    if file:
        file_content = await file.read()
        file_info = {
            "filename": file.filename,
            "size": len(file_content),
            "type": file.content_type.split("/")[-1],  # Lấy loại file (PDF, PNG, ...)
        }

    response = query_engine.query(question)
    answer_stream = StringIO()
    with contextlib.redirect_stdout(answer_stream):
        response.print_response_stream()
    answer = answer_stream.getvalue().strip()

    if not answer or "external source" in answer.lower():
        answer = "Không có dữ liệu."

    return {"question": question, "answer": answer, "file": file_info}
