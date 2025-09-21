from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..database import SessionLocal, ChatSession as DBChatSession, ChatMessage as DBChatMessage, User as DBUser
from ..schemas.chat import ChatSession, ChatSessionCreate, Message, MessageCreate
from .auth import get_current_user # For authentication

router = APIRouter()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/chats", response_model=ChatSession)
def create_chat_session(chat_session: ChatSessionCreate, current_user: DBUser = Depends(get_current_user), db: Session = Depends(get_db)):
    db_chat_session = DBChatSession(title=chat_session.title, owner_id=current_user.id)
    db.add(db_chat_session)
    db.commit()
    db.refresh(db_chat_session)
    return db_chat_session

@router.get("/chats", response_model=List[ChatSession])
def get_user_chat_sessions(current_user: DBUser = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(DBChatSession).filter(DBChatSession.owner_id == current_user.id).all()

@router.get("/chats/{chat_id}", response_model=ChatSession)
def get_chat_session(chat_id: int, current_user: DBUser = Depends(get_current_user), db: Session = Depends(get_db)):
    chat_session = db.query(DBChatSession).filter(DBChatSession.id == chat_id, DBChatSession.owner_id == current_user.id).first()
    if not chat_session:
        raise HTTPException(status_code=404, detail="Chat session not found")
    return chat_session

@router.post("/chats/{chat_id}/messages", response_model=Message)
def create_chat_message(chat_id: int, message: MessageCreate, current_user: DBUser = Depends(get_current_user), db: Session = Depends(get_db)):
    chat_session = db.query(DBChatSession).filter(DBChatSession.id == chat_id, DBChatSession.owner_id == current_user.id).first()
    if not chat_session:
        raise HTTPException(status_code=404, detail="Chat session not found")
    
    db_message = DBChatMessage(session_id=chat_id, sender=message.sender, text=message.text)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message
