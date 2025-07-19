# src/botsmith/main.py
import asyncio
from fastapi import FastAPI
from pydantic import BaseModel
from botsmith.coder_agent import SimpleAgent


app = FastAPI(title="BotSmith-local", version="0.1.0")

# One shared agent instance (cheap & simple)
agent = SimpleAgent("demo", "alice")

class ChatRequest(BaseModel):
    prompt: str

@app.post("/chat")
async def chat(req: ChatRequest):
    result = await agent.execute(req.prompt, {})
    return {"agent": result["agent_id"], "reply": result["reply"]}

@app.get("/health")
async def health():
    return {"status": "ok"}