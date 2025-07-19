import httpx

class OllamaLLM:
    def __init__(self, model: str = "llama3:latest", base_url: str = "http://localhost:11434"):
        self.model = model
        self.base_url = base_url.rstrip("/")
        self._endpoint = f"{self.base_url}/api/generate"

    def generate(self, prompt: str, system_prompt: str = "") -> str:
        payload = {"model": self.model, "prompt": prompt, "system": system_prompt, "stream": False}
        r = httpx.post(self._endpoint, json=payload, timeout=60)
        r.raise_for_status()
        return r.json().get("response", "").strip()

    def is_available(self) -> bool:
        try:
            return httpx.get(f"{self.base_url}/api/tags", timeout=2).status_code == 200
        except Exception:
            return False