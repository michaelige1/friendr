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
    
    print(f"Original dataset shape: {df.shape}")
    print(f"Original dataset size: {len(df)} rows, {len(df.columns)} columns")
    
    # Convert type column to lowercase for consistency
    df['type'] = df['type'].str.lower()
    
    # Check for duplicates based on name and personality ratings only
    # (excluding physical characteristics like age, weight, breed, size)
    personality_cols = [
        "type",
        "name",
        "dogs",
        "cats", 
        "kids",
        "energy",
        "affection",
        "training",
        "new_people"
    ]
    
    # Find duplicates based on personality profile
    duplicates = df.duplicated(subset=personality_cols, keep=False)
    duplicate_count = duplicates.sum()
    
    print(f"\nDuplicate Analysis (based on name + personality ratings):")
    print(f"Total duplicate rows (including originals): {duplicate_count}")
    
    if duplicate_count > 0:
        print(f"Duplicate personality profiles found:")
        duplicate_rows = df[duplicates]
        print(duplicate_rows[['type', 'name', 'dogs', 'cats', 'kids', 'energy', 'affection', 'training', "new_people"]].to_string(index=False))
        
        # Remove duplicates, keeping first occurrence
        df_cleaned = df.drop_duplicates(subset=personality_cols, keep='first')
        removed_count = len(df) - len(df_cleaned)
        
        print(f"\nCleaning Results:")
        print(f"Removed {removed_count} duplicate personality profiles")
        print(f"Cleaned dataset shape: {df_cleaned.shape}")
        print(f"Cleaned dataset size: {len(df_cleaned)} rows, {len(df_cleaned.columns)} columns")
        
        # Use cleaned dataframe
        df = df_cleaned
    else:
        print("No duplicate personality profiles found in the dataset")

    # Features used for clustering (personality ratings only)
    clustering_features = [
        "dogs",
        "cats",
        "kids",
        "energy",
        "affection",
        "training",
        "new_people"
    ]

    # Split dataset into dogs and cats
    dog_df = df[df["type"] == "dog"]
    cat_df = df[df["type"] == "cat"]
    
    print(f"\nPet Type Distribution:")
    print(f"Found {len(dog_df)} dogs and {len(cat_df)} cats")

    # Check if we have enough data for each type
    if len(dog_df) == 0:
        raise ValueError("No dogs found in the dataset")
    if len(cat_df) == 0:
        raise ValueError("No cats found in the dataset")

    # Scale features separately for each group
    scaler_dog = StandardScaler()
    X_dog = scaler_dog.fit_transform(dog_df[clustering_features])

    scaler_cat = StandardScaler()
    X_cat = scaler_cat.fit_transform(cat_df[clustering_features])

    # Train separate KMeans models
    kmeans_dog = KMeans(n_clusters=3, random_state=42, n_init=10)
    kmeans_dog.fit(X_dog)

    kmeans_cat = KMeans(n_clusters=3, random_state=42, n_init=10)
    kmeans_cat.fit(X_cat)

    # Save both models and their scalers
    joblib.dump((kmeans_dog, scaler_dog), SAVE_DIR / "kmeans_dog.pkl")
    joblib.dump((kmeans_cat, scaler_cat), SAVE_DIR / "kmeans_cat.pkl")

    print("\n✅ Models trained and saved: kmeans_dog.pkl, kmeans_cat.pkl")
    
    return df

if __name__ == "__main__":
    cleaned_df = train_and_save_models()
    
    print(f"\n📊 Final Dataset Report:")
    print(f"Final dataset dimensions: {cleaned_df.shape}")
    print(f"Final dataset size: {len(cleaned_df)} rows, {len(cleaned_df.columns)} columns")
    print(f"Pet type breakdown:")
    print(cleaned_df['type'].value_counts())
