from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

app = FastAPI(title="DarkPatternScanner API")

templates = Jinja2Templates(directory="app/templates")

class TextInput(BaseModel):
    text: str


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )

#prediction endpoint
@app.post("/predict")
async def predict(data: TextInput):

    text = data.text

    #temporary dummy prediction
    #replacing with BERT inference later

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