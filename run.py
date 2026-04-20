import time
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from model import build_model

DATA_PATH = "data/spotify.csv"
TARGET = "popularity"

def main():
    start = time.time()

    df = pd.read_csv(DATA_PATH)

    # keep only numeric columns for a simple Week 2 baseline
    numeric_df = df.select_dtypes(include=["number"]).copy()

    if TARGET not in numeric_df.columns:
        raise ValueError(f"Target column '{TARGET}' not found in numeric columns. Columns are: {list(numeric_df.columns)}")

    numeric_df = numeric_df.dropna()

    X = numeric_df.drop(columns=[TARGET])
    y = numeric_df[TARGET]

    # First split off final test set (locked away)
    X_temp, X_test, y_temp, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Then split remaining into train/validation
    X_train, X_val, y_train, y_val = train_test_split(
        X_temp, y_temp, test_size=0.25, random_state=42
    )
    # This gives 60% train, 20% val, 20% test

    model = build_model()
    model.fit(X_train, y_train)
    preds = model.predict(X_val)

    rmse = mean_squared_error(y_val, preds) ** 0.5
    r2 = r2_score(y_val, preds)

    runtime = time.time() - start

    print(f"Rows: {len(df)}")
    print(f"Train size: {len(X_train)}")
    print(f"Validation size: {len(X_val)}")
    print(f"Locked test size: {len(X_test)}")
    print(f"Validation RMSE: {rmse:.4f}")
    print(f"Validation R2: {r2:.4f}")
    print(f"Runtime (seconds): {runtime:.2f}")

if __name__ == "__main__":
    main()