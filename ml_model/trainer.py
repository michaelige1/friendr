# ml_model/trainer.py
import pandas as pd
import joblib
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from pathlib import Path

DATA_PATH = Path("data/pet_data.csv")
SAVE_DIR = Path("saved_models")
SAVE_DIR.mkdir(exist_ok=True)

def train_and_save_models():
    # Load dataset
    df = pd.read_csv(DATA_PATH)

    # Features used for clustering
    feature_cols = [
        "dogs",
        "cats",
        "kids",
        "energy",
        "affection",
        "training"
    ]

    # Split dataset into dogs and cats
    dog_df = df[df["type"] == "dog"]
    cat_df = df[df["type"] == "cat"]

    # Scale features separately for each group
    scaler_dog = StandardScaler()
    X_dog = scaler_dog.fit_transform(dog_df[feature_cols])

    scaler_cat = StandardScaler()
    X_cat = scaler_cat.fit_transform(cat_df[feature_cols])

    # Train separate KMeans models
    kmeans_dog = KMeans(n_clusters=3, random_state=42)
    kmeans_dog.fit(X_dog)

    kmeans_cat = KMeans(n_clusters=3, random_state=42)
    kmeans_cat.fit(X_cat)

    # Save both models and their scalers
    joblib.dump((kmeans_dog, scaler_dog), SAVE_DIR / "kmeans_dog.pkl")
    joblib.dump((kmeans_cat, scaler_cat), SAVE_DIR / "kmeans_cat.pkl")

    print("✅ Models trained and saved: kmeans_dog.pkl, kmeans_cat.pkl")

if __name__ == "__main__":
    train_and_save_models()
