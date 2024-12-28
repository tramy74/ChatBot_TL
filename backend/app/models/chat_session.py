# models/chat_session.py
from sqlalchemy import Column, Integer, String
from database import Base, engine

class ChatSession(Base):
    __tablename__ = "chat_sessions"
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, unique=True, index=True)
    first_question = Column(String, nullable=True)

Base.metadata.create_all(bind=engine)