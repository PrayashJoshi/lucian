# routers/chat.py
from fastapi import APIRouter, HTTPException, Body
from ..services.orchestrator import Orchestrator


router = APIRouter()
orchestrator = Orchestrator()

@router.post("/chat")
async def chat_with_lucian(user_message: str = Body(..., embed=True)):
    try:
        response = orchestrator.process_user_message(user_message)
        # Store the response locally
        with open("./chat_responses.txt", "a") as file:
            file.write(f"User message: {user_message}\nResponse: {response}\n\n")
        
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
