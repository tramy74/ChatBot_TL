
from sqlalchemy import Column, Integer, String, Float, LargeBinary
from database import Base, engine

class FileEmbedding(Base):
    __tablename__ = "file_embeddings"
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, unique=True, index=True)
    embedding = Column(Float, nullable=True)  # Array of floats for embeddings, or use JSON if preferred
    file_data = Column(LargeBinary, nullable=False)  # Store file as binary data

Base.metadata.create_all(bind=engine)