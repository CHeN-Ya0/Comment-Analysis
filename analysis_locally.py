import requests
import json
import argparse
from pathlib import Path

SYSTEM_PROMPT = "You are a precise rater for written feedback quality. Output STRICTLY valid JSON."

def analyze_with_ollama(text: str,
                        model: str = "llama3.2:3b",
                        temperature: float = 0.2,
                        url: str = "http://localhost:11434/api/chat"):
    user_msg = f"""
You will receive a block of feedback text (potentially Chinese and/or English).
Please analyze it and return a JSON object with the following schema:

{{
  "count": {{
    "positive_points": <integer>,
    "negative_points": <integer>,
    "score": <0-10>
  }},
  "volume": {{
    "informativeness_comment": "<one sentence>",
    "score": <0-10>
  }},
  "readability": {{
    "language": "<detected language(s)>",
    "avg_sentence_length_comment": "<short note>",
    "clarity_comment": "<short note>",
    "score": <0-10>
  }},
  "sentiment": {{
    "polarity": "positive|neutral|negative|mixed",
    "tone_comment": "<short note>",
    "score": <0-10>
  }},
  "topics": {{
    "top_topics": ["<topic1>", "<topic2>", "..."],
    "coverage_comment": "<short note>",
    "score": <0-10>
  }},
  "overall": {{
    "rationale": "<one or two sentences why>",
    "score": <0-10>
  }}
}}

IMPORTANT: Return ONLY the JSON, no extra text.

Feedback text:
\"\"\"{text}\"\"\"
"""
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_msg},
        ],
        "stream": False,
        "format": "json",
        "options": {"temperature": temperature}
    }

    resp = requests.post(url, json=payload, timeout=180)
    resp.raise_for_status()

    # Ollama chat API 返回结构：{"message": {"content": "..."}}
    content = resp.json()["message"]["content"]

    # 这里 content 已是纯 JSON 字符串（因为 format="json"）
    data = json.loads(content)
    return data  # 👉 别忘了返回

def main():
    parser = argparse.ArgumentParser(description="Analyze feedback text file with Ollama local model.")
    parser.add_argument("--input", type=str, required=True, help="Path to input txt file")
    parser.add_argument("--model", type=str, default="llama3.2:3b", help="Ollama model name (default: llama3.2:3b)")
    parser.add_argument("--out", type=str, default=None, help="Optional output JSON file")
    args = parser.parse_args()

    path = Path(args.input)
    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")

    text = path.read_text(encoding="utf-8", errors="ignore")

    result = analyze_with_ollama(text, model=args.model)

    pretty = json.dumps(result, indent=2, ensure_ascii=False)
    print(pretty)

    if args.out:
        Path(args.out).write_text(pretty, encoding="utf-8")
        print(f"\nSaved to {args.out}")

if __name__ == "__main__":
    main()
