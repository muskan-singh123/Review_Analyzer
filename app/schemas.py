from typing import List, Dict, Literal
from pydantic import BaseModel, Field


class ReviewsRequest(BaseModel):
    reviews: List[str] = Field(
        ...,
        min_items=1,
        description="List of raw customer review texts"
    )


class InsightResponse(BaseModel):
    overall_sentiment: Literal["positive", "neutral", "negative"]
    sentiment_scores: Dict[str, float]
    key_themes: List[str]
    actionable_feedback: str
