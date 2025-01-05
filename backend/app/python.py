# Add this to the beginning of your app (e.g., `main.py`)
from sqlalchemy import Engine
from models import ChatHistory, FileMetadata
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
Base.metadata.create_all(bind=Engine)
