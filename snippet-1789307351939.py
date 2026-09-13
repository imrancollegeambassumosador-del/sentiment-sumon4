from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from textblob import TextBlob

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    content = await file.read()
    text = content.decode("utf-8", errors="ignore")

    blob = TextBlob(text)
    polarity = blob.sentiment.polarity

    if polarity > 0.1:
        sentiment = "Positive"
    elif polarity < -0.1:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"

    return {
        "filename": file.filename,
        "sentiment": sentiment,
        "score": round(polarity, 3)
    }