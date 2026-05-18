# Phishing Detection System

A machine learning web app that detects phishing URLs using TF-IDF + SVM, served via FastAPI.

## Setup

```bash
pip install -r requirements.txt
```

## Usage

### Step 1: Train the model (run once)
```bash
python train.py
```
This trains multiple models, runs hyperparameter tuning, and saves the best model to `models/`.

### Step 2: Start the web server
```bash
uvicorn app:app --reload
```
Then open http://localhost:8000 and enter any URL to check if it's phishing.

## Bugs Fixed

1. **Regex in `clean_url`**: `r"http\\S+"` had a literal double-backslash, so URLs were never stripped. Fixed to `r"https?\S+"`.
2. **Mixed training + serving**: The original `app.py` ran training on every server start (very slow). Split into `train.py` (one-time training) and `app.py` (serving only).
3. **Missing model check**: Added a clear error if `train.py` hasn't been run yet.
4. **`pickle-mixin` in requirements**: Removed — `pickle` is a Python built-in.
5. **Static files not mounted**: Added `app.mount("/static", ...)` so CSS loads correctly.
6. **Hardcoded column names**: Fixed to use correct `URL` and `label` column names from the dataset.
