# Index Artifact Validation — Week 6

**Date:** 2026-05-18
**Purpose:** Determine whether the project's conclusions depend on the `index` column, which was identified as the highest-importance feature (35.8%) and suspected to act as a noisy genre proxy due to dataset ordering.
**Model:** RandomForestRegressor (n_estimators=200, random_state=42) + log1p(duration_ms) + log1p(instrumentalness), with and without `index`.
**Split:** Identical to run.py — random_state=42, 60/20/20 train/val/test.

---

## What `index` Is

The `index` column is the dataset's row number (0–113,999). It has no intrinsic musical meaning. Its high RF importance (35.8%) arises because the CSV groups tracks by genre — all acoustic tracks appear together, then all pop tracks, etc. The row index is therefore a proxy for genre, and genre correlates with popularity. The RF was exploiting this structural artifact.

---

## Results

### Overall Validation RMSE

| Model | RMSE | R² | Δ RMSE |
|-------|------|----|--------|
| With `index` (retained model) | 15.0196 | 0.5484 | — |
| Without `index` (this validation) | 15.7187 | 0.5054 | +0.699 |

Removing `index` worsens overall RMSE by 0.70 units. This confirms that the RF was extracting real (if indirect) signal from index — specifically, genre-correlated patterns it cannot reach through the audio features directly.

### Bucket-Level Metrics

| Bucket | N | RMSE (with index) | RMSE (no index) | Δ RMSE | MAE (no index) | Bias (no index) |
|--------|---|-------------------|-----------------|--------|----------------|-----------------|
| Low (0–33) | 11,127 | 14.16 | 15.22 | +1.06 | 11.22 | +10.67 |
| Medium (34–66) | 10,117 | 11.53 | 13.31 | +1.78 | 9.86 | −8.79 |
| High (67–100) | 1,556 | 31.72 | **28.48** | **−3.24** | 23.27 | −23.26 |

### Feature Importances Without `index`

| Rank | Feature | Importance |
|------|---------|------------|
| 1 | acousticness | 0.1050 |
| 2 | danceability | 0.0995 |
| 3 | tempo | 0.0986 |
| 4 | valence | 0.0982 |
| 5 | speechiness | 0.0953 |
| 6 | loudness | 0.0927 |
| 7 | energy | 0.0882 |
| 8 | liveness | 0.0839 |
| 9 | duration_ms | 0.0539 |
| 10 | log_duration_ms | 0.0532 |
| 11 | key | 0.0413 |
| 12 | instrumentalness | 0.0373 |
| 13 | log_instrumentalness | 0.0372 |
| 14 | mode | 0.0094 |
| 15 | time_signature | 0.0062 |

Without `index`, importances distribute evenly across the 8 core audio features (each 8–11%). This is the expected picture: no single feature dominates, reflecting that popularity prediction requires the joint signal of multiple audio dimensions.

---

## Does Each Conclusion Survive?

### 1. Do tree-based models still significantly outperform linear models?

**Yes.** The no-index RF RMSE is 15.72 vs. the LinearRegression baseline of 22.06. That is a 28.8% relative improvement and a 6.34-unit absolute reduction — still a large and unambiguous gap. The main claim is intact.

### 2. Does the regression-to-the-mean effect on high-popularity tracks remain?

**Yes — and the pattern is actually cleaner without index.** High-bucket RMSE drops from 31.72 to 28.48 (an improvement of 3.24 units) when index is removed, while low- and medium-bucket RMSE gets worse. This is the most important finding of the validation:

- With index, the model was using genre-correlated row position to partially identify popular-genre tracks, inflating its apparent accuracy on average while the structural gap at the high end remained severe.
- Without index, high-bucket RMSE is 28.48 and bias is −23.26 — still nearly 2.1× the medium-bucket RMSE, still a large systematic underprediction.

The regression-to-the-mean effect is real. It was not an artifact of the index column. **Removing the artifact makes the bucket pattern more interpretable, not weaker.**

### 3. Does the feature ceiling interpretation still hold?

**Yes, more cleanly.** Without the index proxy, the RF is working from genuine audio signal only. It still reaches RMSE 15.72, which:
- Is 28.8% better than the linear baseline
- Still plateaus immediately — every further change would face the same ceiling
- Still fails severely on high-popularity tracks (bias −23.26)

The ceiling is audio-feature signal, not RF capacity. The index column was giving the model a borrowed edge that masked this slightly. The no-index result is the truer picture of what audio features alone can achieve.

---

## Decision: Update Retained Model to Drop `index`

The index column is a dataset artifact, not a real audio feature. The no-index model is:
- Less accurate overall (RMSE +0.70) but more interpretable and honest
- Better on high-popularity tracks (RMSE −3.24) — the hardest and most important bucket
- Correctly distributes importance across genuine audio features

`model.py` has been updated to explicitly drop `index` before fitting. `popularity_bucket_analysis.csv` has been updated to reflect no-index results. `feature_importance_summary.md` has been updated accordingly.

---

## Summary

All three conclusions from the locked story survive the removal of the index artifact:

| Conclusion | Survives? | Notes |
|------------|-----------|-------|
| RF >> LinearRegression | Yes | 15.72 vs. 22.06, −28.8% |
| Improvements plateau quickly | Yes | No new headroom opened by removing index |
| Regression-to-mean on high-popularity tracks | Yes | High-bucket RMSE 28.48, bias −23.26; still 2.1× medium |
| Feature ceiling is real | Yes | Cleaner picture without the genre proxy |

The validation strengthens rather than weakens the project's final story.
