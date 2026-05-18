import re
import pickle
import os

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

# =========================
# NLP PREPROCESSING
# =========================

def clean_url(text):
    # Remove protocol
    text = re.sub(r"https?://", "", text)
    # Split on non-alphanumeric characters to tokenize the URL parts
    tokens = re.split(r"[^a-zA-Z0-9]", text)
    # Keep tokens that are mostly alphabetic and at least 3 chars
    tokens = [t.lower() for t in tokens if len(t) >= 3 and re.search(r"[a-zA-Z]", t)]
    return " ".join(tokens)

# =========================
# LOAD MODEL
# =========================

MODEL_PATH = "models/model.pkl"
VECTORIZER_PATH = "models/vectorizer.pkl"

if not os.path.exists(MODEL_PATH) or not os.path.exists(VECTORIZER_PATH):
    raise RuntimeError(
        "Model files not found. Please run 'python train.py' first to train and save the model."
    )

model = pickle.load(open(MODEL_PATH, "rb"))
vectorizer = pickle.load(open(VECTORIZER_PATH, "rb"))

# =========================
# FASTAPI APP
# =========================

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

# =========================
# HOME PAGE  & PREDICT
# =========================

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"prediction": ""}
    )

@app.post("/predict", response_class=HTMLResponse)
async def predict(request: Request, url: str = Form(...)):
    cleaned = clean_url(url)
    vector = vectorizer.transform([cleaned])
    prediction = model.predict(vector)

    # Detect if input looks like an email address
    is_email = bool(re.match(r"[^@]+@[^@]+\.[^@]+", url.strip()))
    input_type = "Email" if is_email else "URL"

    if prediction[0] == 0:
        result = f"⚠️ Phishing {input_type} Detected"
    else:
        result = f"✅ Legitimate {input_type}"

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"prediction": result}
    )