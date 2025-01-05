from sqlalchemy import Column, Float, Integer, String, LargeBinary, ARRAY
from database import Base

class FileMetadata(Base):
    __tablename__ = "file_metadata"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    filetype = Column(String, nullable=False)
    filedata = Column(LargeBinary, nullable=True)  # Optional to store the file content
    embedding = Column(ARRAY(Float), nullable=True)  # For vector embeddings
