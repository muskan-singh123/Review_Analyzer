from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .schemas import ReviewsRequest, InsightResponse
from .llm_client import analyze_reviews

app = FastAPI(
    title="Customer Insight API",
    description="Sentiment Engine for Marketing Teams: analyze batches of customer reviews.",
    version="1.0.0",
)

# Mount static files
#app.mount("/static", StaticFiles(directory="static"), name="static")

# Load templates
templates = Jinja2Templates(directory="templates")


# 👉 Render index.html
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# CORS (optional)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post(
    "/analyze",
    response_model=InsightResponse,
    tags=["analysis"],
)
def analyze_endpoint(payload: ReviewsRequest):
    try:
        return analyze_reviews(payload)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

