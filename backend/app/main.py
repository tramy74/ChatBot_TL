# import os
# import openai
# import uuid
# from fastapi import FastAPI, UploadFile, File, Depends
# from app.embeddings.embedding_utils import process_and_store_file
# from sqlalchemy.orm import Session
# from fastapi.middleware.cors import CORSMiddleware
# from database import SessionLocal, engine, init_db
# from models.chat_session import ChatSession
# from models.chat_history import ChatHistory
# from models.file_embedding import FileEmbedding
# from models.chat import create_chat_session_table
# from models.conversation import Conversation
# from models.message import Message
# from pydantic import BaseModel
# from app.api import routes

# app = FastAPI()

# app.include_router(routes.router, prefix="/api")

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:3000"],  # Update this if your frontend is hosted elsewhere
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# UPLOAD_FOLDER = "uploads/"
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# def generate_embedding(file_content):
#     response = openai.Embedding.create(
#         input=file_content.decode("utf-8"),  # assuming text file content
#         model="text-embedding-ada-002"
#     )
#     embedding = response['data'][0]['embedding']
#     return embedding

# @app.on_event("startup")
# async def startup_event():
#     await init_db()

# @app.post("/upload_and_embed")
# async def upload_and_embed(file: UploadFile = File(...), db: Session = Depends(get_db)):
#     # Read file content as binary
#     file_content = await file.read()
#     file_location = os.path.join(UPLOAD_FOLDER, file.filename)
    
#     # Generate embedding for the file content
#     embedding = generate_embedding(file_content)

#     # Save file and embedding data to database
#     file_record = FileEmbedding(
#         filename=file.filename,
#         embedding=embedding,
#         file_data=file_content
#     )
#     db.add(file_record)
#     db.commit()
#     db.refresh(file_record)

#     # Optionally save the file to disk (if desired)
#     with open(file_location, "wb") as f:
#         f.write(file_content)

#     return {"info": f"File '{file.filename}' uploaded and embedded"}
# @app.post("/chat")
# async def chat(question: str, db: Session = Depends(get_db)):
#     # Generate response using OpenAI API
#     response = openai.Completion.create(
#         model="text-davinci-003",
#         prompt=question,
#         max_tokens=150
#     )
#     answer = response.choices[0].text.strip()

#     # Save question and answer to the database
#     chat_history = ChatHistory(question=question, answer=answer)
#     db.add(chat_history)
#     db.commit()

#     return {"question": question, "answer": answer}

# @app.post("/new_chat")
# async def new_chat(db: Session = Depends(get_db)):
#     session_id = str(uuid.uuid4())
#     new_session = ChatSession(session_id=session_id)
#     db.add(new_session)
#     db.commit()
#     db.refresh(new_session)
#     return {"session_id": session_id}


# @app.post("/chat/{session_id}")
# async def chat(session_id: str, question: str, db: Session = Depends(get_db)):
#     # Generate response
#     response = openai.Completion.create(
#         model="text-davinci-003",
#         prompt=question,
#         max_tokens=150
#     )
#     answer = response.choices[0].text.strip()

#     # Save question-answer in dynamic session table
#     ChatSessionTable = create_chat_session_table(session_id)
#     chat_entry = ChatSessionTable(question=question, answer=answer)
#     db.add(chat_entry)
#     db.commit()

#     # Update first question if not already set
#     session_record = db.query(ChatSession).filter(ChatSession.session_id == session_id).first()
#     if session_record and not session_record.first_question:
#         session_record.first_question = question
#         db.commit()

#     return {"question": question, "answer": answer}

# @app.get("/sessions")
# async def get_sessions(db: Session = Depends(get_db)):
#     sessions = db.query(ChatSession).all()
#     return [{"session_id": session.session_id, "first_question": session.first_question} for session in sessions]

# @app.post("/chat")
# async def chat(conversation_id: int = None, question: str = None, db: Session = Depends(get_db)):
#     # Generate response from OpenAI
#     response = openai.Completion.create(model="text-davinci-003", prompt=question, max_tokens=150)
#     answer = response.choices[0].text.strip() if response.choices else "Không tìm thấy dữ liệu."

#     if not answer:
#         answer = "Không tìm thấy dữ liệu."

#     if conversation_id:
#         # Add message to existing conversation
#         conversation = db.query(Conversation).get(conversation_id)
#     else:
#         # Create new conversation with the first question as the title
#         conversation = Conversation(title=question)
#         db.add(conversation)
#         db.commit()
#         db.refresh(conversation)

#     # Save the message
#     message = Message(conversation_id=conversation.id, question=question, answer=answer)
#     db.add(message)
#     db.commit()

#     return {"conversation_id": conversation.id, "question": question, "answer": answer}

# @app.get("/conversations")
# async def get_conversations(db: Session = Depends(get_db)):
#     conversations = db.query(Conversation).all()
#     return [{"id": conv.id, "title": conv.title} for conv in conversations]

# @app.get("/conversation/{conversation_id}")
# async def get_conversation(conversation_id: int, db: Session = Depends(get_db)):
#     messages = db.query(Message).filter(Message.conversation_id == conversation_id).all()
#     return [{"question": msg.question, "answer": msg.answer} for msg in messages]

# class Question(BaseModel):
#     question: str

# @app.post("/chat")
# async def chat(question: Question):
#     # Generate a response based on the question
#     answer = handle_user_question(question.question)
#     return {"answer": answer}

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
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

@app.post("/query")
async def get_answer(query: Query):
    response = query_engine.query(query.question)

    # Capture and process the response stream
    answer_stream = StringIO()
    with contextlib.redirect_stdout(answer_stream):
        response.print_response_stream()
    answer = answer_stream.getvalue().strip()

    # Handle empty or invalid responses
    if not answer or "external source" in answer.lower():
        answer = "Không có dữ liệu."

    return {"answer": answer}

