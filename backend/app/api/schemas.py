from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class DocumentUpload(BaseModel):
    title: str
    author: str
    doc_type: str
    summary: Optional[str] = None
    content_url: str

class UserCreate(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    user_id: int
    username: str

class DocumentListResponse(BaseModel):
    documents: List[dict]

class ConversationCreate(BaseModel):
    title: str

class ConversationResponse(BaseModel):
    conversation_id: int
    title: str
    created_at: datetime

class MessageCreate(BaseModel):
    text: str
    is_user: bool

class MessageResponse(BaseModel):
    message_id: int
    conversation_id: int
    text: str
    is_user: bool
    timestamp: datetime

