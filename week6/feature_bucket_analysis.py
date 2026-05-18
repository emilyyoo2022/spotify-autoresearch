"""
Week 6 feature bucket error analysis.
Descriptive/interpretive only — no model changes.
Uses current best model (RF n_estimators=200, index dropped, log transforms)
on the locked train/val split to generate predictions, then slices error
by danceability, energy, and tempo buckets.
"""

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
import sys, os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from model import build_model

DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data/spotify.csv")
TARGET = "popularity"
OUT_DIR = os.path.dirname(os.path.abspath(__file__))

# ── Reproduce exact split ─────────────────────────────────────────────────────
df = pd.read_csv(DATA_PATH)
numeric_df = df.select_dtypes(include=["number"]).copy().dropna()

X = numeric_df.drop(columns=[TARGET])
y = numeric_df[TARGET]

X_temp, X_test, y_temp, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
X_train, X_val, y_train, y_val = train_test_split(X_temp, y_temp, test_size=0.25, random_state=42)

# ── Fit and predict ───────────────────────────────────────────────────────────
model = build_model()
model.fit(X_train, y_train)
preds = model.predict(X_val)

results = pd.DataFrame({
    "true_popularity":      y_val.values,
    "predicted_popularity": preds,
    "error":                preds - y_val.values,
    "abs_error":            np.abs(preds - y_val.values),
    "sq_error":             (preds - y_val.values) ** 2,
    "danceability":         X_val["danceability"].values,
    "energy":               X_val["energy"].values,
    "tempo":                X_val["tempo"].values,
})

# ── Bucket definitions ────────────────────────────────────────────────────────
feature_configs = {
    "danceability": {
        "thresholds": (0.4, 0.7),
        "labels": ["low (<0.4)", "medium (0.4–0.7)", "high (>0.7)"],
        "unit": "(0–1 scale)",
    },
    "energy": {
        "thresholds": (0.33, 0.66),
        "labels": ["low (<0.33)", "medium (0.33–0.66)", "high (>0.66)"],
        "unit": "(0–1 scale)",
    },
    "tempo": {
        "thresholds": (90, 140),
        "labels": ["low (<90 BPM)", "medium (90–140 BPM)", "high (>140 BPM)"],
        "unit": "(BPM)",
    },
}

def assign_bucket(val, lo, hi):
    if val <= lo:
        return 0
    elif val <= hi:
        return 1
    else:
        return 2

# ── Compute metrics ───────────────────────────────────────────────────────────
all_rows = []
summary = {}

for feat, cfg in feature_configs.items():
    lo, hi = cfg["thresholds"]
    labels  = cfg["labels"]
    results["bucket_idx"] = results[feat].apply(lambda v: assign_bucket(v, lo, hi))

    feat_rows = []
    for i, label in enumerate(labels):
        sub = results[results["bucket_idx"] == i]
        n        = len(sub)
        rmse     = np.sqrt(sub["sq_error"].mean())
        mae      = sub["abs_error"].mean()
        mean_err = sub["error"].mean()
        std_err  = sub["error"].std()
        feat_rows.append({
            "feature": feat,
            "bucket": label,
            "n_tracks": n,
            "rmse": round(rmse, 4),
            "mae": round(mae, 4),
            "mean_error": round(mean_err, 4),
            "std_error": round(std_err, 4),
        })
        all_rows.append(feat_rows[-1])

    summary[feat] = feat_rows
    print(f"\n=== {feat.upper()} ===")
    for row in feat_rows:
        print(f"  {row['bucket']:<25}  n={row['n_tracks']:>5}  "
              f"RMSE={row['rmse']:.4f}  MAE={row['mae']:.4f}  bias={row['mean_error']:+.4f}")

# ── Save CSV ──────────────────────────────────────────────────────────────────
out_df = pd.DataFrame(all_rows)
out_df.to_csv(os.path.join(OUT_DIR, "feature_bucket_error_summary.csv"), index=False)
print("\nSaved: feature_bucket_error_summary.csv")

# ── Plot ──────────────────────────────────────────────────────────────────────
fig, axes = plt.subplots(2, 3, figsize=(15, 8))
fig.suptitle(
    "Prediction Error by Audio Feature Range\n"
    "RF model (n_estimators=200, index excluded) — validation set",
    fontsize=11, y=1.01
)

palette = {
    "danceability": ["#90CAF9", "#42A5F5", "#1565C0"],
    "energy":       ["#A5D6A7", "#4CAF50", "#1B5E20"],
    "tempo":        ["#FFCC80", "#FFA726", "#E65100"],
}

for col, (feat, cfg) in enumerate(feature_configs.items()):
    rows   = summary[feat]
    labels = [r["bucket"].replace(" ", "\n", 1) for r in rows]
    rmse_v = [r["rmse"]       for r in rows]
    mae_v  = [r["mae"]        for r in rows]
    bias_v = [r["mean_error"] for r in rows]
    colors = palette[feat]

    # Row 0: RMSE and MAE
    ax = axes[0, col]
    x = np.arange(3)
    w = 0.35
    b1 = ax.bar(x - w/2, rmse_v, w, label="RMSE", color=colors[1], alpha=0.85)
    b2 = ax.bar(x + w/2, mae_v,  w, label="MAE",  color=colors[0], alpha=0.85)
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=8)
    ax.set_title(f"{feat.capitalize()} {cfg['unit']}", fontsize=10)
    ax.set_ylabel("Error (popularity units)" if col == 0 else "")
    ax.legend(fontsize=8)
    ax.set_ylim(0, max(rmse_v) * 1.3)
    for b in b1:
        ax.text(b.get_x() + b.get_width()/2, b.get_height() + 0.15,
                f"{b.get_height():.1f}", ha="center", va="bottom", fontsize=7)
    for b in b2:
        ax.text(b.get_x() + b.get_width()/2, b.get_height() + 0.15,
                f"{b.get_height():.1f}", ha="center", va="bottom", fontsize=7)

    # Row 1: Bias (mean error)
    ax2 = axes[1, col]
    bar_colors = [colors[2] if v > 0 else colors[0] for v in bias_v]
    bars = ax2.bar(x, bias_v, color=bar_colors, alpha=0.85)
    ax2.axhline(0, color="black", linewidth=0.8, linestyle="--", alpha=0.6)
    ax2.set_xticks(x)
    ax2.set_xticklabels(labels, fontsize=8)
    ax2.set_ylabel("Mean bias (pred − true)" if col == 0 else "")
    ax2.set_title(f"{feat.capitalize()} — Prediction Bias", fontsize=10)
    lim = max(abs(v) for v in bias_v) * 1.35
    ax2.set_ylim(-lim, lim)
    for b, v in zip(bars, bias_v):
        va = "bottom" if v >= 0 else "top"
        offset = lim * 0.03 if v >= 0 else -lim * 0.03
        ax2.text(b.get_x() + b.get_width()/2, v + offset,
                 f"{v:+.1f}", ha="center", va=va, fontsize=8)

plt.tight_layout()
fig.savefig(os.path.join(OUT_DIR, "feature_bucket_error_plot.png"), dpi=150, bbox_inches="tight")
print("Saved: feature_bucket_error_plot.png")
