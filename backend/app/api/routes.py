from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from llamindex import get_relevant_data
from gpt import generate_response  # Assuming gpt.py has response generation

app = FastAPI()

class Query(BaseModel):
    question: str

@app.on_event("startup")
def load_chat_history():
    """Load past chat history from the database into memory on startup."""
    global chat_history
    with get_db() as db:
        history = db.query(QuestionHistory).order_by(QuestionHistory.created_at.asc()).all()
        chat_history = [
            {
                "message_id": item.id,
                "conversation_id": 1,  # Assuming a single conversation for now
                "text": item.question,
                "is_user": True,
                "timestamp": item.created_at,
            } for item in history
        ] + [
            {
                "message_id": item.id + 1000,  # Offset for generated responses
                "conversation_id": 1,
                "text": item.answer,
                "is_user": False,
                "timestamp": item.created_at,
            } for item in history
        ]

@app.get("/history", response_model=List[MessageResponse])
async def get_chat_history():
    """Retrieve the full chat history."""
    return chat_history

@app.post("/ask", response_model=MessageResponse)
async def ask_question(query: MessageCreate, db: Session = Depends(get_db)):
    """Handle user question, generate a response, and save to the database."""
    try:
        question = query.text

        # Use LlamaIndex to fetch relevant data
        relevant_data = get_relevant_data(question)

        # If no relevant data, return a predefined response
        if not relevant_data:
            answer = "No relevant data available for this question."
        else:
            # Generate response using GPT
            answer = generate_response(question, relevant_data)

        # Save the question and answer to the database
        new_entry = QuestionHistory(question=question, answer=answer, created_at=datetime.utcnow())
        db.add(new_entry)
        db.commit()

        # Add the new question and answer to the in-memory history
        new_question = {
            "message_id": new_entry.id,
            "conversation_id": 1,
            "text": question,
            "is_user": True,
            "timestamp": new_entry.created_at,
        }
        new_answer = {
            "message_id": new_entry.id + 1000,  # Offset for answer messages
            "conversation_id": 1,
            "text": answer,
            "is_user": False,
            "timestamp": new_entry.created_at,
        }
        chat_history.extend([new_question, new_answer])

        return new_answer
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))