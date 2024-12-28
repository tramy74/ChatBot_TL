from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base  # Import Base from your database file

class Conversation(Base):
    __tablename__ = "conversations"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    messages = relationship("Message", back_populates="conversation")
