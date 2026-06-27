from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
import agent

app = FastAPI()

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        # Convert Pydantic models to dicts for the agent
        messages_dicts = [{"role": msg.role, "content": msg.content} for msg in request.messages]
        response = agent.process_conversation(messages_dicts)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

# Minor optimization: 6348
# Minor optimization: 7287
# Minor optimization: 9652
# Minor optimization: 5321
# Minor optimization: 8477
# Minor optimization: 1124
# Minor optimization: 2498