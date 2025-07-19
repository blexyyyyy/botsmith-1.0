from typing import Any, Optional

class MemoryStore:
    def __init__(self) -> None:
        self._store: dict[str, dict[str, Any]] = {}

    def save(self, agent_id: str, key: str, value: Any) -> None:
        self._store.setdefault(agent_id, {})[key] = value

    def load(self, agent_id: str, key: str) -> Optional[Any]:
        return self._store.get(agent_id, {}).get(key)

    def list_keys(self, agent_id: str) -> list[str]:
        return list(self._store.get(agent_id, {}).keys())