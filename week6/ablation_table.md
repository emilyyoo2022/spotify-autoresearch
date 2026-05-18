# Ablation Table — Full Experimental Summary

**Date:** 2026-05-18
**Project:** Spotify Popularity Prediction — AutoResearch Weeks 2–6
**Evaluation metric:** Validation RMSE (lower is better)
**Locked best model:** RF n_estimators=200 + log1p(duration_ms) + log1p(instrumentalness) → RMSE 15.0196

---

## Complete Experimental Direction Summary

| Direction | Experiment(s) | Best / Representative RMSE | Δ vs. Prior Best | Conclusion | Role |
|-----------|---------------|---------------------------|------------------|------------|------|
| **LinearRegression baseline** | Exp 0 | 22.0630 | — (baseline) | Linear model captures almost no variance (R²=0.026); popularity–audio relationship is nonlinear | Frozen baseline |
| **Ridge Regression** | Exp 1 | 22.0630 | 0.000 | Identical to baseline; dataset not overfitting, regularization adds nothing | Dropped |
| **Random Forest (first adoption)** | Exp 2 | 15.0714 | −7.0 (−31.7%) | Largest single improvement in the project; nonlinear tree splits capture structure linear models miss | **Kept** |
| **HistGradientBoosting (default)** | Exp 3 | 18.4472 | +3.4 vs. RF | Slower learner with default params; underperforms RF on this feature set | Dropped |
| **RF n_estimators scaling** | Exp 4, Week 4 matrix | 14.9942 (n=300) | −0.077 vs. n=100 | Diminishing returns: 6× runtime increase for 0.5% RMSE gain; ceiling is feature-driven not capacity-driven | Dropped above n=200 |
| **log1p(duration_ms)** | E1 | 15.0232 | −0.002 | Tiny improvement; right-skewed feature benefits from log compression | **Kept** |
| **log1p(loudness)** | E2 | 15.0259 | +0.003 | No benefit; loudness is bounded and not zero-inflated | Dropped |
| **Feature dropping (key, mode, time_sig, index)** | E3 | 15.7345 | +0.711 | Large degradation; low-intuition features carry real RF signal | Dropped |
| **Interaction terms (danceability×energy, energy×loudness, tempo×danceability)** | E4, E5, E6 | 15.0361 (best) | +0.004 to +0.019 | RF already finds interactions via tree splits; manual products add collinear noise | Dropped |
| **log1p(instrumentalness)** | E7 | 15.0196 | −0.004 | Marginal improvement; instrumentalness is zero-inflated and benefits from log compression | **Kept — final best** |
| **log1p(speechiness, acousticness)** | E8 | 15.0261 | +0.007 | No benefit; these features are not sufficiently zero-inflated | Dropped |
| **HistGradientBoosting (tuned, 500 iter)** | E9 | 17.7524 | +2.733 | Substantially worse; boosting sequential fitting is not well-suited to this feature pattern | Dropped |
| **RF max_features=0.5** | E10 | 15.3764 | +0.357 | Worse; reducing feature fraction per split hurts diversity on this dataset | Dropped |
| **ExtraTreesRegressor** | E11 | 15.4511 | +0.432 | Worse; random split thresholds less effective than RF's best-split search here | Dropped |
| **RF min_samples_leaf=3** | E12 | 15.2800 | +0.260 | Worse; leaf regularization is not the bottleneck | Dropped |
| **Popularity bucket analysis** | Week 6 | RMSE 11.53–31.72 by bucket | N/A (diagnostic) | Model performs best on medium tracks; severely underpredicts high-popularity tracks (bias −27.85); confirms feature ceiling is real and non-uniform | **Final contribution** |

---

## Key Takeaways

**One change drove almost everything:** The switch from LinearRegression to RandomForest (Exp 2) accounts for 7.0 of the 7.04 total RMSE improvement. All subsequent experiments combined moved RMSE by 0.04 units.

**The feature ceiling is real:** Weeks 4 and 5 tested 12+ changes across model complexity, preprocessing, and hyperparameters. Total additional gain: 0.058 RMSE units. This is not a modeling shortfall — the numeric audio features have been mined.

**The ceiling is not uniform:** The bucket analysis shows the feature ceiling bites hardest for high-popularity tracks. Numeric audio features cannot reliably identify breakout hits; the model regresses to the mean and misses by ~28 popularity points on average for tracks above popularity 67.

---

## What Was Never Tried (Out of Scope)

The following were considered and explicitly dropped without testing because they fall outside the program constraints or would not change the core finding:

- Categorical feature encoding (track_genre, explicit, artist) — run.py frozen to numeric columns only
- External data / API integration — dataset frozen
- Neural networks — no theoretical advantage on 13-column tabular regression
- Changing evaluation metric — would invalidate all cross-week comparisons
