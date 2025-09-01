# 📘 Feedback Analysis Project

This project provides a tool to analyze feedback text and quantify it into structured metrics. It supports two modes of operation:

1. **API-based (OpenAI models, cloud)**
2. **Local inference (Ollama models, offline)**

---

## 🚀 Features

- Input: Feedback text from a `.txt` file.  
- Output: Structured **JSON** with scores and explanations for each metric.  
- Metrics:  
  - **Count**: Number and balance of positive/negative points  
  - **Volume**: Informativeness and coverage  
  - **Readability**: Language, sentence length, clarity  
  - **Sentiment**: Polarity and tone  
  - **Topics**: Coverage of main topics  
  - **Overall**: Final evaluation and score  

---

## 🔧 Requirements

- **Python** ≥ 3.9  
- **Dependencies**:
  ```bash
  pip install requests openai argparse
  ```

---

## 🌐 Version 1: API (OpenAI)

### Setup
Set your API key as an environment variable:
```bash
export OPENAI_API_KEY=sk-xxxxxxxx
```

### Run
```bash
python analysis_api.py --input comments.txt --out scores.json --model gpt-4o-mini
```

**Arguments:**
- `--input`: Path to input `.txt` file  
- `--model`: OpenAI model name (e.g., `gpt-4o-mini`, `gpt-4o`)  
- `--out`: Path to save JSON output  

---

## 💻 Version 2: Local (Ollama)

### 1. Install Ollama
On macOS/Linux:
```bash
brew install ollama
```
On Windows: see [Ollama docs](https://ollama.com)

### 2. Pull a model
Recommended small models:
```bash
ollama pull qwen2.5:3b
# or
ollama pull llama3.2:3b
```

### 3. Test the model
```bash
ollama run qwen2.5:3b "Give me a one-sentence pep talk."
```

### 4. Run analysis
```bash
python analysis_locally.py --input comments.txt --out scores.json --model qwen2.5:3b
```

**Arguments:**
- `--input`: Path to input `.txt` file  
- `--model`: Ollama model name  
- `--out`: Path to save JSON output (default: `result.json`)  

---

## 📂 Example Output

```json
{
  "count": {
    "positive_points": 5,
    "negative_points": 8,
    "score": 7
  },
  "volume": {
    "informativeness_comment": "The feedback is informative and detailed.",
    "score": 9
  },
  "readability": {
    "language": "English",
    "avg_sentence_length_comment": "Sentences are moderately long.",
    "clarity_comment": "Generally clear but sometimes verbose.",
    "score": 6
  },
  "sentiment": {
    "polarity": "mixed",
    "tone_comment": "Constructive but occasionally critical.",
    "score": 7
  },
  "topics": {
    "top_topics": ["Design", "Testing", "Requirements"],
    "coverage_comment": "Covers key aspects of the project.",
    "score": 8
  },
  "overall": {
    "rationale": "Helpful feedback, but readability could improve.",
    "score": 7
  }
}
```

---

## 📌 Notes

- **API version**: Data is sent to OpenAI servers → not suitable for sensitive data.  
- **Local version (Ollama)**: All inference is done locally, no data leaves your machine → suitable for private scenarios.  
- Results may vary slightly across runs due to model randomness; use low temperature (0.1–0.2) for stable outputs.  

---

✨ With this setup, you can flexibly switch between **cloud inference** (better accuracy, less setup) and **local inference** (privacy-first, fully offline).

## 📊 Appendix：Scoring Rubric

The analysis produces scores **from 0 to 10** for each metric. The following rubric provides guidance on interpretation:

| **Metric**     | **0–3 (Low)** | **4–6 (Medium)** | **7–8 (Good)** | **9–10 (Excellent)** |
|----------------|---------------|------------------|----------------|-----------------------|
| **Count**      | Very few points, unbalanced, vague | Some points identified, but unbalanced or incomplete | Balanced number of positive/negative points, moderately clear | Comprehensive, balanced, and well-justified |
| **Volume**     | Very little information, superficial | Moderate detail, some gaps | Covers most aspects with relevant detail | Highly informative, concise, and comprehensive |
| **Readability**| Hard to follow, confusing, unclear language | Some clarity but frequent long/complex sentences | Generally clear, average sentence length manageable | Very clear, concise, easy to read |
| **Sentiment**  | Negative/harsh tone, unconstructive | Neutral or inconsistent tone | Constructive with minor issues | Professional, positive, supportive, and constructive |
| **Topics**     | Very narrow, missing most key topics | Covers some relevant topics, but incomplete | Covers major relevant topics with reasonable breadth | Broad and thorough coverage of all key topics |
| **Overall**    | Not useful, hard to act upon | Partially useful, requires effort to extract insights | Useful with clear and actionable insights | Very useful, actionable, and well-structured |