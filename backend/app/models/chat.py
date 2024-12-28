from sqlalchemy import Column, Integer, String, Text
from database import Base, engine

def create_chat_session_table(session_id):
    class ChatSession(Base):
        __tablename__ = f"chat_session_{session_id}"
        id = Column(Integer, primary_key=True, index=True)
        question = Column(Text, nullable=False)
        answer = Column(Text, nullable=False)
    return ChatSession

Base.metadata.create_all(bind=engine)