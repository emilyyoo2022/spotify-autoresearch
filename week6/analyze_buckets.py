"""
Week 6 popularity bucket analysis.
Reproduces the exact train/val split from run.py and analyzes prediction error
across low-, medium-, and high-popularity tracks.
"""

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from model import build_model

# ── Reproduce exact split from run.py ───────────────────────────────────────
DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data/spotify.csv")
TARGET = "popularity"

df = pd.read_csv(DATA_PATH)
numeric_df = df.select_dtypes(include=["number"]).copy().dropna()

X = numeric_df.drop(columns=[TARGET])
y = numeric_df[TARGET]

X_temp, X_test, y_temp, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
X_train, X_val, y_train, y_val = train_test_split(X_temp, y_temp, test_size=0.25, random_state=42)

# ── Fit best model ───────────────────────────────────────────────────────────
model = build_model()
model.fit(X_train, y_train)
preds = model.predict(X_val)

# ── Bucket assignment ────────────────────────────────────────────────────────
# Buckets based on true popularity (0–100 scale, split at 33 and 66)
def assign_bucket(pop):
    if pop <= 33:
        return "low (0-33)"
    elif pop <= 66:
        return "medium (34-66)"
    else:
        return "high (67-100)"

results = pd.DataFrame({
    "true_popularity": y_val.values,
    "predicted_popularity": preds,
    "error": preds - y_val.values,
    "abs_error": np.abs(preds - y_val.values),
    "sq_error": (preds - y_val.values) ** 2,
})
results["bucket"] = results["true_popularity"].apply(assign_bucket)

# ── Per-bucket metrics ───────────────────────────────────────────────────────
bucket_order = ["low (0-33)", "medium (34-66)", "high (67-100)"]

rows = []
for bucket in bucket_order:
    sub = results[results["bucket"] == bucket]
    n = len(sub)
    rmse = np.sqrt(sub["sq_error"].mean())
    mae = sub["abs_error"].mean()
    mean_err = sub["error"].mean()
    std_err = sub["error"].std()
    p25 = sub["error"].quantile(0.25)
    p75 = sub["error"].quantile(0.75)
    rows.append({
        "bucket": bucket,
        "n_tracks": n,
        "rmse": round(rmse, 4),
        "mae": round(mae, 4),
        "mean_error": round(mean_err, 4),
        "std_error": round(std_err, 4),
        "error_p25": round(p25, 4),
        "error_p75": round(p75, 4),
    })

bucket_df = pd.DataFrame(rows)
print(bucket_df.to_string(index=False))

out_dir = os.path.dirname(os.path.abspath(__file__))
bucket_df.to_csv(os.path.join(out_dir, "popularity_bucket_analysis.csv"), index=False)
print("\nSaved: popularity_bucket_analysis.csv")

# ── Plot ─────────────────────────────────────────────────────────────────────
fig, axes = plt.subplots(1, 3, figsize=(15, 5))
fig.suptitle("Prediction Error by Popularity Bucket\n(RandomForest, n_estimators=200, numeric features + log transforms)",
             fontsize=11, y=1.01)

# Panel 1: RMSE and MAE bar chart
ax1 = axes[0]
x = np.arange(len(bucket_order))
width = 0.35
rmse_vals = bucket_df["rmse"].values
mae_vals = bucket_df["mae"].values
bars1 = ax1.bar(x - width/2, rmse_vals, width, label="RMSE", color="#2196F3", alpha=0.85)
bars2 = ax1.bar(x + width/2, mae_vals, width, label="MAE", color="#FF9800", alpha=0.85)
ax1.set_xticks(x)
ax1.set_xticklabels(["Low\n(0–33)", "Medium\n(34–66)", "High\n(67–100)"], fontsize=9)
ax1.set_ylabel("Error (popularity units)")
ax1.set_title("RMSE and MAE by Bucket")
ax1.legend()
ax1.set_ylim(0, max(rmse_vals.max(), mae_vals.max()) * 1.25)
for bar in bars1:
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.2,
             f"{bar.get_height():.2f}", ha='center', va='bottom', fontsize=8)
for bar in bars2:
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.2,
             f"{bar.get_height():.2f}", ha='center', va='bottom', fontsize=8)

# Panel 2: Error distribution violin plot
ax2 = axes[1]
violin_data = [results[results["bucket"] == b]["error"].values for b in bucket_order]
parts = ax2.violinplot(violin_data, positions=[1, 2, 3], showmedians=True, showextrema=True)
colors = ["#66BB6A", "#42A5F5", "#EF5350"]
for i, pc in enumerate(parts['bodies']):
    pc.set_facecolor(colors[i])
    pc.set_alpha(0.7)
ax2.axhline(0, color='black', linewidth=0.8, linestyle='--', alpha=0.5)
ax2.set_xticks([1, 2, 3])
ax2.set_xticklabels(["Low\n(0–33)", "Medium\n(34–66)", "High\n(67–100)"], fontsize=9)
ax2.set_ylabel("Prediction Error (pred − true)")
ax2.set_title("Error Distribution by Bucket")

# Panel 3: Track count
ax3 = axes[2]
counts = bucket_df["n_tracks"].values
bar_colors = ["#66BB6A", "#42A5F5", "#EF5350"]
bars3 = ax3.bar(["Low\n(0–33)", "Medium\n(34–66)", "High\n(67–100)"], counts,
                color=bar_colors, alpha=0.85)
ax3.set_ylabel("Number of tracks (validation set)")
ax3.set_title("Track Count by Bucket")
for bar, count in zip(bars3, counts):
    ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 20,
             str(count), ha='center', va='bottom', fontsize=9)

plt.tight_layout()
fig.savefig(os.path.join(out_dir, "error_by_bucket_plot.png"), dpi=150, bbox_inches='tight')
print("Saved: error_by_bucket_plot.png")

# Print summary for use in memos
print("\n── Summary for memos ──")
for _, row in bucket_df.iterrows():
    print(f"{row['bucket']}: n={row['n_tracks']}, RMSE={row['rmse']}, MAE={row['mae']}, mean_err={row['mean_error']}")
