# Customer Insight API (Sentiment Engine)

A small FastAPI-based **Customer Insight API** that helps marketing teams quickly
understand customer feedback using an LLM (Gemini).

Given a batch of raw text reviews, the API returns:

1. **Overall Sentiment** – positive / neutral / negative.
2. **Key Themes** – top topics mentioned across the reviews.
3. **Actionable Feedback** – one sentence on what specifically needs improvement.

---

## Tech Stack

- **Language:** Python 3.x
- **Framework:** FastAPI
- **LLM Provider:** Google Gemini (gemini-1.5-flash)
- **Auth:** API key loaded from environment variables (`.env` file)

---

## Setup Instructions

### 1. Clone the repo

```bash
git clone https://github.com/<your-username>/customer-insight-api.git
cd customer-insight-api
