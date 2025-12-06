import os
import json
from typing import Any, Dict

from dotenv import load_dotenv

import google.generativeai as genai
#genai.configure(api_key=GEMINI_API_KEY)

from .schemas import ReviewsRequest, InsightResponse

# Load environment variables from .env
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY is not set. "
        "Create a .env file and set GEMINI_API_KEY=your_key_here"
    )

genai.configure(api_key=GEMINI_API_KEY)

# You can change the model if needed
GEMINI_MODEL_NAME = "gemini-1.5-flash"

SYSTEM_INSTRUCTIONS = """
You are a Customer Insight Engine for a marketing analytics team.

You will receive a batch of raw customer reviews about a product.

You MUST return a STRICT JSON object ONLY, with EXACTLY these keys:
- "overall_sentiment": one of "positive", "neutral", or "negative".
- "sentiment_scores": an object with keys "positive", "neutral", "negative" and float values between 0 and 1 that sum approximately to 1.
- "key_themes": an array of at most 3 short topic phrases (e.g., "UI speed", "customer support", "pricing").
- "actionable_feedback": a single sentence describing what specifically needs improvement.

Rules:
- Do NOT include any additional keys.
- Do NOT include explanations or markdown.
- Output MUST be pure JSON (no backticks, no comments).
"""


def _build_prompt(req: ReviewsRequest) -> str:
    joined_reviews = "\n".join(f"- {review}" for review in req.reviews)
    prompt = f"""
{SYSTEM_INSTRUCTIONS}

Customer reviews:
{joined_reviews}
"""
    return prompt.strip()


def _extract_json(text: str) -> Dict[str, Any]:
    """
    Tries to parse JSON from the model output.
    If there is extra text, extracts the first {...} block.
    """
    text = text.strip()

    # If it's already pure JSON, this will just work
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # Fallback: extract substring between first { and last }
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        json_str = text[start : end + 1]
        return json.loads(json_str)

    raise ValueError(f"Could not parse JSON from model output: {text}")


def analyze_reviews(req: ReviewsRequest) -> InsightResponse:
    prompt = _build_prompt(req)

    model = genai.GenerativeModel(GEMINI_MODEL_NAME)
    response = model.generate_content(prompt)

    # Gemini returns a rich object; we just want the text
    text = response.text or ""

    data = _extract_json(text)

    # Pydantic will validate and coerce this into our response schema
    return InsightResponse(**data)
