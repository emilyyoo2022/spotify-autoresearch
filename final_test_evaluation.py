"""
Final test-set evaluation — run once only for reporting.

Do NOT modify model.py or run.py.
Do NOT re-tune anything after seeing these results.
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from model import build_model

DATA_PATH = "data/spotify.csv"
TARGET = "popularity"

def main():
    df = pd.read_csv(DATA_PATH)

    numeric_df = df.select_dtypes(include=["number"]).copy()

    if TARGET not in numeric_df.columns:
        raise ValueError(f"Target column '{TARGET}' not found in numeric columns.")

    numeric_df = numeric_df.dropna()

    X = numeric_df.drop(columns=[TARGET])
    y = numeric_df[TARGET]

    # Identical split to run.py: 60% train, 20% val, 20% test, random_state=42
    X_temp, X_test, y_temp, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    X_train, X_val, y_train, y_val = train_test_split(
        X_temp, y_temp, test_size=0.25, random_state=42
    )

    # Train final locked model on training split only
    model = build_model()
    model.fit(X_train, y_train)

    # Validation performance (for comparison)
    val_preds = model.predict(X_val)
    val_rmse = mean_squared_error(y_val, val_preds) ** 0.5

    # One-time evaluation on the held-out test set
    test_preds = model.predict(X_test)
    test_rmse = mean_squared_error(y_test, test_preds) ** 0.5
    test_r2 = r2_score(y_test, test_preds)

    print(f"Validation RMSE:  {val_rmse:.4f}")
    print(f"Final Test RMSE:  {test_rmse:.4f}")
    print(f"Final Test R2:    {test_r2:.4f}")

if __name__ == "__main__":
    main()
