from sqlalchemy import Column, Integer, String, Text
from database import Base, engine

class ChatHistory(Base):
    __tablename__ = "chat_history"
    id = Column(Integer, primary_key=True, index=True)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)

Base.metadata.create_all(bind=engine)