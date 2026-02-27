import json
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3.1:8b"

def generate_stream(prompt: str):
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": True,
        "options": {
            "temperature": 0.4,
            "top_p": 0.9,
            "num_ctx": 2048
        }
    }
    r = requests.post(OLLAMA_URL, json=payload, stream=True, timeout=60)
    r.raise_for_status()
    for line in r.iter_lines():
        if line:
            data = json.loads(line)
            yield data.get("response", "")
