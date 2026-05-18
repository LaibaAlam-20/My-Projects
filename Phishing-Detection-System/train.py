import pandas as pd
import numpy as np
import re
import pickle

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, f1_score

# =========================
# LOAD DATASET
# =========================

print("Loading dataset...")
df = pd.read_csv("dataset/PhiUSIIL_Phishing_URL_Dataset.csv")

print(df.head())
print("Columns:", df.columns.tolist())

print("Label distribution:")
print(df["label"].value_counts())
print("Sample phishing URLs:")
print(df[df["label"] == 0]["URL"].head(3).tolist())
print("Sample legitimate URLs:")
print(df[df["label"] == 1]["URL"].head(3).tolist())



# =========================
# FIND URL + LABEL COLUMN
# =========================

# URL column is the second column (index 1), label is the last
url_column = "URL"
label_column = "label"

# =========================
# DATA CLEANING
# =========================

df.drop_duplicates(inplace=True)
df.dropna(subset=[url_column, label_column], inplace=True)
df[url_column] = df[url_column].astype(str)

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

df["cleaned_url"] = df[url_column].apply(clean_url)

# now cleaned_url exists, safe to filter
df = df[df["cleaned_url"].str.strip() != ""]
# =========================
# TF-IDF
# =========================

vectorizer = TfidfVectorizer(max_features=5000)
X = vectorizer.fit_transform(df["cleaned_url"])
y = df[label_column]

# =========================
# TRAIN TEST SPLIT
# =========================

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# =========================
# TRAIN & EVALUATE MODELS
# =========================

models = {
    "Logistic Regression": LogisticRegression(max_iter=1000),
    "Naive Bayes": MultinomialNB(),
    "Random Forest": RandomForestClassifier(n_estimators=100),
    "SVM": LinearSVC(max_iter=2000),
}

best_model = None
best_score = 0
best_model_name = ""

for name, model in models.items():
    print(f"\n========================\n{name}\n========================")
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    f1 = f1_score(y_test, predictions, average="weighted")
    print("Accuracy:", accuracy)
    print("F1 Score:", f1)
    print(classification_report(y_test, predictions))

    if f1 > best_score:
        best_score = f1
        best_model = model
        best_model_name = name

print("\nBEST MODEL:", best_model_name)

# =========================
# HYPERPARAMETER TUNING
# =========================

print("\nRunning Hyperparameter Tuning on SVM...")
params = {"C": [0.1, 1, 10]}
grid = GridSearchCV(LinearSVC(max_iter=2000), params, cv=5, n_jobs=-1)
grid.fit(X_train, y_train)
best_model = grid.best_estimator_
print("Best Parameters:", grid.best_params_)

# =========================
# FINAL EVALUATION
# =========================

final_predictions = best_model.predict(X_test)
final_accuracy = accuracy_score(y_test, final_predictions)
final_f1 = f1_score(y_test, final_predictions, average="weighted")

print("\nFINAL RESULTS")
print("Accuracy:", final_accuracy)
print("F1 Score:", final_f1)
print(confusion_matrix(y_test, final_predictions))

# =========================
# SAVE MODEL
# =========================

import os
os.makedirs("models", exist_ok=True)

pickle.dump(best_model, open("models/model.pkl", "wb"))
pickle.dump(vectorizer, open("models/vectorizer.pkl", "wb"))
print("\nModel and vectorizer saved to models/")
