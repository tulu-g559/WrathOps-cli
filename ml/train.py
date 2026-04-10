import json
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report


# 📂 Load dataset
with open("ml/secrets_dataset.json", "r") as f:
    data = json.load(f)

X = [x[0] for x in data]   # text
y = [x[1] for x in data]   # label


# ✂️ Train-test split (important for evaluation)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)


# 🔤 Vectorization (character-level works best for secrets)
vectorizer = TfidfVectorizer(
    analyzer="char",
    ngram_range=(3, 5),
    min_df=2,          # ignore rare noise
    max_features=5000  # control size
)

X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)


# 🤖 Model
model = LogisticRegression(
    max_iter=1000,
    class_weight="balanced"   # important if dataset is skewed
)

model.fit(X_train_vec, y_train)


# 📊 Evaluation
y_pred = model.predict(X_test_vec)

print("\n📊 Model Evaluation:\n")
print(classification_report(y_test, y_pred))


# 💾 Save model
with open("model.pkl", "wb") as f:
    pickle.dump(model, f)

with open("vectorizer.pkl", "wb") as f:
    pickle.dump(vectorizer, f)

print("\n✅ Model and vectorizer saved!")


# 🧪 Quick test function
def predict_secret(text):
    vec = vectorizer.transform([text])
    pred = model.predict(vec)[0]
    prob = max(model.predict_proba(vec)[0])
    return pred, prob


# 🔍 Test samples
samples = [
    "sk-abc123xyz4567890abcdef",
    "hello_world_variable",
    "AKIAIOSFODNN7EXAMPLE"
]

print("\n🔎 Sample Predictions:\n")
for s in samples:
    label, confidence = predict_secret(s)
    print(f"{s[:30]}... → {label} ({confidence:.2f})")