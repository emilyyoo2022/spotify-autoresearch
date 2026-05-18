"""
Week 6 validation: remove index column from feature set and re-run best RF pipeline.
Diagnostic only — does not modify model.py or run.py.
Reproduces exact train/val split from run.py (random_state=42).
"""

import numpy as np
import pandas as pd
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data/spotify.csv")
TARGET = "popularity"

# ── Reproduce exact split from run.py ────────────────────────────────────────
df = pd.read_csv(DATA_PATH)
numeric_df = df.select_dtypes(include=["number"]).copy().dropna()

X_full = numeric_df.drop(columns=[TARGET])
y = numeric_df[TARGET]

X_temp, X_test, y_temp, y_test = train_test_split(X_full, y, test_size=0.2, random_state=42)
X_train_full, X_val_full, y_train, y_val = train_test_split(X_temp, y_temp, test_size=0.25, random_state=42)

# ── Drop index column ─────────────────────────────────────────────────────────
DROP_COL = "index"
X_train = X_train_full.drop(columns=[DROP_COL])
X_val   = X_val_full.drop(columns=[DROP_COL])

print(f"Features with index:    {list(X_train_full.columns)}")
print(f"Features without index: {list(X_train.columns)}")

# ── Build identical pipeline (same transforms, same RF) ──────────────────────
def _engineer_features(X):
    X = pd.DataFrame(X).copy()
    X['log_duration_ms'] = np.log1p(X['duration_ms'])
    X['log_instrumentalness'] = np.log1p(X['instrumentalness'])
    return X

model = Pipeline([
    ('features', FunctionTransformer(_engineer_features, validate=False)),
    ('model', RandomForestRegressor(n_estimators=200, random_state=42, n_jobs=-1))
])

import time
t0 = time.time()
model.fit(X_train, y_train)
preds = model.predict(X_val)
runtime = time.time() - t0

# ── Overall metrics ───────────────────────────────────────────────────────────
rmse_new = np.sqrt(mean_squared_error(y_val, preds))
from sklearn.metrics import r2_score
r2_new = r2_score(y_val, preds)

RMSE_PREV = 15.0196
R2_PREV   = 0.5484

print(f"\n=== OVERALL METRICS ===")
print(f"Previous (with index):    RMSE={RMSE_PREV:.4f}  R2={R2_PREV:.4f}")
print(f"New (without index):      RMSE={rmse_new:.4f}  R2={r2_new:.4f}")
print(f"Delta RMSE:               {rmse_new - RMSE_PREV:+.4f}")
print(f"Runtime: {runtime:.1f}s")

# ── Bucket analysis ───────────────────────────────────────────────────────────
def assign_bucket(pop):
    if pop <= 33:
        return "low (0-33)"
    elif pop <= 66:
        return "medium (34-66)"
    else:
        return "high (67-100)"

results = pd.DataFrame({
    "true_popularity":      y_val.values,
    "predicted_popularity": preds,
    "error":                preds - y_val.values,
    "abs_error":            np.abs(preds - y_val.values),
    "sq_error":             (preds - y_val.values) ** 2,
})
results["bucket"] = results["true_popularity"].apply(assign_bucket)

bucket_order = ["low (0-33)", "medium (34-66)", "high (67-100)"]

# Previous bucket numbers for comparison
prev = {
    "low (0-33)":      {"rmse": 14.1632, "mae": 9.4752,  "mean_error":  8.9966},
    "medium (34-66)":  {"rmse": 11.5339, "mae": 8.3574,  "mean_error": -6.8423},
    "high (67-100)":   {"rmse": 31.7197, "mae": 27.8561, "mean_error": -27.8474},
}

print(f"\n=== BUCKET METRICS ===")
print(f"{'Bucket':<20} {'N':>6}  {'RMSE (new)':>10}  {'RMSE (prev)':>11}  {'ΔRMSE':>7}  {'MAE (new)':>9}  {'Bias (new)':>10}")
print("-" * 90)

new_rows = []
for bucket in bucket_order:
    sub = results[results["bucket"] == bucket]
    n        = len(sub)
    rmse     = np.sqrt(sub["sq_error"].mean())
    mae      = sub["abs_error"].mean()
    mean_err = sub["error"].mean()
    std_err  = sub["error"].std()
    p25      = sub["error"].quantile(0.25)
    p75      = sub["error"].quantile(0.75)

    delta = rmse - prev[bucket]["rmse"]
    print(f"{bucket:<20} {n:>6}  {rmse:>10.4f}  {prev[bucket]['rmse']:>11.4f}  {delta:>+7.4f}  {mae:>9.4f}  {mean_err:>+10.4f}")

    new_rows.append({
        "bucket": bucket, "n_tracks": n,
        "rmse": round(rmse, 4), "mae": round(mae, 4),
        "mean_error": round(mean_err, 4), "std_error": round(std_err, 4),
        "error_p25": round(p25, 4), "error_p75": round(p75, 4),
    })

# ── Feature importances (no-index model) ─────────────────────────────────────
rf = model.named_steps['model']
X_t = model.named_steps['features'].transform(X_train)
feat_names = list(X_t.columns)
imp_df = pd.DataFrame({"feature": feat_names, "importance": rf.feature_importances_})
imp_df = imp_df.sort_values("importance", ascending=False).reset_index(drop=True)

print(f"\n=== FEATURE IMPORTANCES (no index) ===")
print(imp_df.to_string(index=False))

# ── Save outputs ──────────────────────────────────────────────────────────────
out_dir = os.path.dirname(os.path.abspath(__file__))

new_bucket_df = pd.DataFrame(new_rows)
new_bucket_df.to_csv(os.path.join(out_dir, "popularity_bucket_analysis_no_index.csv"), index=False)
print("\nSaved: popularity_bucket_analysis_no_index.csv")

# Summary dict for memo writing
print("\n=== SUMMARY FOR MEMO ===")
print(f"overall_rmse_prev={RMSE_PREV}, overall_rmse_new={rmse_new:.4f}, delta={rmse_new-RMSE_PREV:+.4f}")
for row in new_rows:
    print(row)
print(imp_df.to_string(index=False))
