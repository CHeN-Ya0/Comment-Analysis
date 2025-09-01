# local_ollama_demo.py
import requests
import json

def ollama_chat(model, messages, stream=False, url="http://localhost:11434/api/chat"):
    payload = {
        "model": model,
        "messages": messages,
        "stream": stream,
        
    }
    r = requests.post(url, json=payload, timeout=120)
    r.raise_for_status()
    data = r.json()
    return data["message"]["content"]

if __name__ == "__main__":
    reply = ollama_chat(
        model="llama3.2:3b",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Give me a 1-sentence pep talk."}
        ]
    )
    print(reply)
