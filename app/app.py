from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

app = FastAPI(title="DarkPatternScanner API")

templates = Jinja2Templates(directory="app/templates")


# -----------------------------
# Request Schema
# -----------------------------
class TextInput(BaseModel):
    text: str


# -----------------------------
# Home Page
# -----------------------------
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )


# -----------------------------
# Prediction Endpoint
# -----------------------------
@app.post("/predict")
async def predict(data: TextInput):

    text = data.text

    # --------------------------------------------------
    # Temporary dummy prediction
    # Replace with BERT inference later
    # --------------------------------------------------
    prediction = "unknown"
    confidence = 0.0

    if "only" in text.lower():
        prediction = "scarcity"
        confidence = 0.91

    return {
        "text": text,
        "label": prediction,
        "confidence": confidence
    }