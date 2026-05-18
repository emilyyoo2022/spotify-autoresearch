# Week 6 Scope Lock Memo — Popularity Bucket Analysis

**Date:** 2026-05-18
**Model:** RandomForestRegressor (n_estimators=200, random_state=42) + log1p(duration_ms) + log1p(instrumentalness)
**Overall validation RMSE:** 15.0196
**Analysis:** Error breakdown across low-, medium-, and high-popularity tracks (validation set, n=22,800)

---

## Bucket Definitions

| Bucket | Range | N (validation) |
|--------|-------|----------------|
| Low | popularity 0–33 | 11,127 |
| Medium | popularity 34–66 | 10,117 |
| High | popularity 67–100 | 1,556 |

Thresholds are fixed at 33 and 66 on the 0–100 popularity scale. High-popularity tracks are a small minority of the dataset.

---

## Results: Error by Bucket

| Bucket | RMSE | MAE | Mean Error (bias) | Std Error |
|--------|------|-----|-------------------|-----------|
| Low (0–33) | 14.16 | 9.48 | +8.99 | 10.94 |
| Medium (34–66) | **11.53** | **8.36** | −6.84 | 9.29 |
| High (67–100) | **31.72** | **27.86** | −27.85 | 15.19 |

---

## Where the Model Performs Best

**Medium-popularity tracks (34–66)** are the easiest to predict. RMSE is 11.53, MAE is 8.36, and error variance is the lowest of any bucket. The model is systematically biased toward this range — predictions regress toward the mean of the training distribution, which is centered in this band. Medium tracks benefit from the largest cluster of training examples and do not rely on features the model cannot see.

---

## Where the Model Performs Worst

**High-popularity tracks (67–100)** are the most difficult. RMSE is 31.72 — more than double the medium-bucket RMSE — and MAE is 27.86. The mean prediction error is −27.85, meaning the model chronically and severely underpredicts high-popularity tracks. This is not random noise: it is systematic bias.

Low-popularity tracks are intermediate. RMSE is 14.16 and the model overpredicts by +8.99 on average. This is the mirror image of the high-popularity failure: the model pulls both extremes toward the mean.

---

## Interpretation: Regression to the Mean

The pattern across all three buckets is a textbook **regression to the mean** driven by missing signal:

- **Low-popularity tracks:** The model doesn't see enough signal to confidently predict near-zero popularity. It hedges by predicting higher than the true value.
- **High-popularity tracks:** The model doesn't see enough signal to confidently predict very high popularity. It hedges by predicting lower than the true value.
- **Medium tracks:** These cluster near the conditional mean of the training distribution. The model's natural pull toward the center happens to be accurate here.

The severity at the high end is compounded by class imbalance: high-popularity tracks make up only 6.8% of the validation set (1,556 of 22,800). The model has fewer examples of extreme popularity to learn from.

---

## What This Implies About the Feature Signal Ceiling

The bucket analysis makes the feature ceiling concrete:

1. **Numeric audio features cannot distinguish very popular from moderately popular tracks.** A song with high danceability, energy, and low speechiness could be a blockbuster or a mid-tier track — the audio features alone cannot tell. What separates them is artist fame, playlist placement, and release timing: none of which appear in the feature set.

2. **The ceiling is not uniform.** There is more recoverable signal at the low end (bad-sounding, obscure, or clearly niche tracks) than at the high end (where every popular track sounds different and success is determined by cultural factors).

3. **Adding more trees or better preprocessing cannot fix this.** Week 4 showed diminishing returns from n_estimators. Week 5 showed that feature engineering moved RMSE by 0.006. The bucket analysis explains why: the remaining error is not reducible by any transformation of the existing columns.

---

## Conclusion for Final Story

The model is accurate in the range where the available features carry signal, and systematically wrong in the range where the determining factors are unobserved. This is not a modeling failure — it is a data ceiling. The finding is interpretable, defensible, and complete.
