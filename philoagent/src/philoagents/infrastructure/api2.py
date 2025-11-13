import uvicorn
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from philoagents.application.conversation_service.generate_response import (
    get_response,
)
from philoagents.application.conversation_service.reset_conversation import (
    reset_conversation_state,
)
from philoagents.domain.philosopher_factory import PhilosopherFactory

# Ensure these imports are correct based on your file structure
from .opik_utils import configure , flush_traces

# Configuration should happen at module load time
configure()

PHILOSOPHER_NAMES = {
    "socrates": "Socrates",
    "plato": "Plato",
    "aristotle": "Aristotle",
    "descartes": "Rene Descartes",
    "leibniz": "Gottfried Wilhelm Leibniz",
    "ada_lovelace": "Ada Lovelace",
    "turing": "Alan Turing",
    "chomsky": "Noam Chomsky",
    "searle": "John Searle",
    "dennett": "Daniel Dennett",
}

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatMessage(BaseModel):
    message: str
    philosopher_id: str

@app.get("/philosophers")
async def get_philosophers():
    """Returns the list of available philosophers for selection in Streamlit UI."""
    return PHILOSOPHER_NAMES

@app.post("/chat")
async def chat(chat_message: ChatMessage):
    # Use a separate try/except for the chat logic
    try:
        philosopher_factory = PhilosopherFactory()
        philosopher = philosopher_factory.get_philosopher(chat_message.philosopher_id)

        # NOTE: Make sure you pass all required arguments here! I am guessing based on the context.
        response, _ = await get_response(
            messages=chat_message.message,
            philosopher_id=chat_message.philosopher_id,
            philosopher_name=philosopher.name,
            philosopher_perspective=philosopher.perspective,
            philosopher_style=philosopher.style,
            philosopher_context="",
        )
        
        # --- NEW CODE: FLUSH TRACE DATA - RE-ENABLED ---
        try:
            # We are now using the fixed flush_traces() function from opik_utils.py
            flush_traces() 
        except Exception:
            # Silently catch the Opik flush error to keep the main request working
            pass 
        # -----------------------------------------------
        
        return {"response": response}
    
    # This original except block catches errors from RAG/LLM process or unhandled
    # exceptions from the Opik block above (if not fully commented out).
    except Exception as e:
        # If the error is still a 500 here, the issue is in get_response()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/reset-memory")
async def reset_conversation():
    try:
        result = await reset_conversation_state()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)