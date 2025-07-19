# src/botsmith/workflow.py
import asyncio
from botsmith.coder_agents import build_team   # fixed

async def run_bot_creation(prompt: str) -> str:
    team = build_team()
    result = await team.run(task=prompt)
    return result.messages[-1].content