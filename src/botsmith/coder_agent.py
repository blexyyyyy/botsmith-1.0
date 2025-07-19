# src/botsmith/coder_agents.py
from typing import Dict, Any, List
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_ext.models.ollama import OllamaChatCompletionClient
from botsmith.memory import MemoryStore

class SimpleAgent:
    """
    Single-agent wrapper for REST endpoint.
    """
    def __init__(
        self,
        agent_id: str,
        name: str,
        system_message: str = "You are a helpful assistant.",
    ):
        self.agent_id = agent_id
        self.name = name
        self.memory = MemoryStore()
        self.assistant = AssistantAgent(
            name=name,
            model_client=OllamaChatCompletionClient(
                model="llama3:latest",
                base_url="http://localhost:11434",
                timeout=60,
                temperature=0.0,
            ),
            system_message=system_message,
        )

    async def execute(self, task: str, context: Dict[str, Any]) -> Dict[str, Any]:
        self.memory.save(self.agent_id, "last_task", task)
        messages = [TextMessage(content=task, source="user")]
        reply = await self.assistant.on_messages(messages, cancellation_token=None)
        reply_text = reply.chat_message.content
        self.memory.save(self.agent_id, "last_reply", reply_text)
        return {"agent_id": self.agent_id, "reply": reply_text}

    def get_capabilities(self) -> List[str]:
        return ["chat", "reasoning", "code_generation"]

    def get_performance_metrics(self) -> Dict[str, float]:
        return {"cpu_util": 0.0}


def build_team() -> RoundRobinGroupChat:
    """Builds a two-agent team using the local Ollama model."""
    llm = OllamaChatCompletionClient(
        model="llama3:latest",
        base_url="http://localhost:11434",
        timeout=60,
        temperature=0.0,
    )

    coder = AssistantAgent(
        name="Coder",
        model_client=llm,
        system_message="You are a concise Python developer. Only output code or short comments.",
    )

    reviewer = AssistantAgent(
        name="Reviewer",
        model_client=llm,
        system_message="You are a code reviewer. Give one-sentence feedback and stop.",
    )

    team = RoundRobinGroupChat([coder, reviewer], max_turns=3)
    return team