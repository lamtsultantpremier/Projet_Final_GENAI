from fastapi import APIRouter , Depends
from src.schemas import CreateMessage , LLMMessage
from sqlalchemy.orm import Session
from src.database.database import get_db
from services import message_services , session_services


router = APIRouter()

@router.post("")
def create_message(create_message : CreateMessage , db : Session = Depends(get_db)):

    current_message = message_services.create_message(create_message , db)

    current_message_session = session_services.get_session_by_id(current_message.session_id , db)

    message_history = [LLMMessage.model_validate(message) for message in current_message_session.messages]

    payload = {"input" : current_message.content , "history" : message_history}
    
    
    return payload