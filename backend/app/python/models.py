# models.py

from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String, Float, Text
from sqlalchemy.ext.declarative import declarative_base
import numpy as np

Base = declarative_base()

class DocumentVector(Base):
    __tablename__ = 'document_vectors'

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(String, unique=True, index=True)  # or another identifier
    vector = Column(String)  # Store as string (JSON) or array

    def set_vector(self, embedding):
        # Convert numpy array to string for storage
        self.vector = np.array(embedding).tolist()

from pydantic import BaseModel

class User(BaseModel):
    username: str
    password: str

class QuestionHistory(Base):
    __tablename__ = "question_history"
    id = Column(Integer, primary_key=True, index=True)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)