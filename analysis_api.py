# analysis.py
import json
import re
import argparse
import os
from pathlib import Path
from typing import Dict, Any
from openai import OpenAI

# ========== Basic statistics (local calculation, not using the model) ==========
def basic_volume_stats(text: str) -> Dict[str, int]:
    t = text.strip()

    # Rough sentence segmentation (taking into account both Chinese and English punctuation)
    sentences = re.split(r'[。！？!?\.]+(?:\s+|$)', t)
    sentences = [s for s in sentences if s.strip()]

    words = re.findall(r'\b\w+\b', t)

    # Paragraph statistics: count by non-blank lines
    paragraphs = [p for p in t.splitlines() if p.strip()]

    return {
        "characters_no_space": len(re.sub(r'\s+', '', t)),
        "characters_with_space": len(t),
        "words_en_like": len(words),
        "sentences": len(sentences),
        "paragraphs": len(paragraphs),
    }

# ========== prompt ==========
SYSTEM_PROMPT = """You are a precise rater for written feedback quality.
Output STRICTLY valid JSON with the requested schema.
All scores must be numbers from 0 to 10 (allow decimals).
Be concise but specific.
"""

def build_user_message(text: str) -> str:

    return f"""
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

Scoring guidance (brief):
- count.score: more balanced and well-justified points (pos & neg) → higher; vague or few points → lower.
- volume.score: broader coverage with pertinent, non-redundant detail → higher; superficial or bloated → lower.
- readability.score: clear structure, short-to-moderate sentences, easy to follow → higher.
- sentiment.score: professional, constructive tone → higher; harsh/unclear tone → lower.
- topics.score: covers structure, content, data/criteria, visuals, rubric/alignment etc. → higher.

IMPORTANT: Return ONLY the JSON, no extra text.

Feedback text:
\"\"\"{text}\"\"\"
"""

# ========== Calling OpenAI API ==========
def analyze_with_openai(client: OpenAI, text: str, model: str = "gpt-4o-mini") -> Dict[str, Any]:
    user_msg = build_user_message(text)

    resp = client.chat.completions.create(
        model=model,
        temperature=0.2,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_msg}
        ]
    )

    content = resp.choices[0].message.content

    try:
        return json.loads(content)
    except json.JSONDecodeError:

        m = re.search(r'\{[\s\S]*\}\s*$', content)
        if not m:
            raise ValueError("Model did not return valid JSON:\n" + content)
        return json.loads(m.group(0))

# ========== main ==========
def main():
    parser = argparse.ArgumentParser(description="Analyze feedback TXT and score 5 metrics via OpenAI.")
    parser.add_argument("--api_key", type=str, default=None, help="OpenAI API key (sk-...). If omitted, use env OPENAI_API_KEY.")
    parser.add_argument("--input", type=str, default="comments.txt", help="Path to the feedback .txt file")
    parser.add_argument("--model", type=str, default="gpt-4o-mini", help="OpenAI model name (e.g., gpt-4o, gpt-4o-mini)")
    parser.add_argument("--out", type=str, default="scores.json", help="Output JSON path")
    args = parser.parse_args()

    # Reading text
    path = Path(args.input)
    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")

    text = path.read_text(encoding="utf-8", errors="ignore")

    # Local volume statistics
    volume_stats = basic_volume_stats(text)

    # Client (supports reading from parameters or environment variables)
    api_key = args.api_key or os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("No API key provided. Use --api_key or set env OPENAI_API_KEY.")

    client = OpenAI(api_key=api_key)

    # Model Scoring
    model_scores = analyze_with_openai(client, text, model=args.model)

    result = {
        "file": str(path),
        "volume_stats": volume_stats,
        "scores": model_scores
    }

    # print & save
    pretty = json.dumps(result, ensure_ascii=False, indent=2)
    print(pretty)
    Path(args.out).write_text(pretty, encoding="utf-8")
    print(f"\nSaved to {args.out}")

if __name__ == "__main__":
    main()
