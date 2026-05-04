# Failure Analysis Memo — Week 4 Controlled Experiments

**Date:** 2026-05-04
**Experiment axis:** n_estimators in RandomForestRegressor (50, 100, 200, 300)
**Controlled variables:** dataset, numeric features only, random_state=42, train/val/test split, RMSE metric

---

## Results Summary

| n_estimators | Val RMSE | Val R2 | Runtime (s) |
|-------------|----------|--------|-------------|
| 50          | 15.1752  | 0.5390 | 9.67        |
| 100         | 15.0714  | 0.5453 | 19.56       |
| 200         | 15.0254  | 0.5480 | 39.76       |
| 300         | 14.9942  | 0.5499 | 58.46       |

---

## Dominant Failure Mode: Signal Failure (Feature Ceiling)

The dominant failure mode in this experiment is **signal failure** — specifically, a feature ceiling imposed by the numeric-only feature set.

Increasing n_estimators from 50 to 300 reduced RMSE by only **0.181 units** (1.2% relative improvement), while runtime increased **6×** (9.67s → 58.46s). The marginal gain per additional 100 trees shrank monotonically:

- 50 → 100: −0.1038 RMSE, +9.89s
- 100 → 200: −0.0460 RMSE, +20.20s
- 200 → 300: −0.0312 RMSE, +18.70s

This is a classic diminishing-returns curve. The model is not broken — all runs were stable, no leakage occurred, and the agent respected all constraints — but more trees cannot recover signal that the features do not contain.

A Random Forest with n_estimators=300 still explains only ~55% of variance in validation (R2=0.5499). That leaves ~45% unexplained, which is unlikely to be recovered by further tuning of n_estimators.

---

## Why This Failure Mode Dominates

Spotify popularity is partly determined by factors not present in the numeric audio features (e.g., artist fame, playlist placement, release timing, genre trends). Numeric features like danceability, energy, and tempo have limited predictive power for popularity in isolation. The model has likely extracted most of the available signal from these features already — even at n_estimators=50.

---

## Next Steps

1. **Add non-numeric features.** Artist, genre, and track name encodings (e.g., target encoding or embeddings) would likely unlock more signal than any further hyperparameter tuning.
2. **Try a different model family.** HistGradientBoostingRegressor or XGBoost may extract more signal from the same numeric features due to sequential residual fitting.
3. **Feature engineering.** Interaction terms, log-transformations of skewed features (e.g., duration_ms), or binned tempo/loudness may help.
4. **Accept n_estimators=100 or 200 as the operating point.** The RMSE gap between 100 and 300 trees is only 0.077 units, but the runtime difference is 3×. Unless RMSE is the hard constraint, n_estimators=100 offers the best efficiency trade-off.

---

## Conclusion

The experiment ran cleanly with no code, leakage, or agent failures. The limiting factor is feature quality, not model capacity. Continued tuning of n_estimators beyond 100–200 trees is not recommended given the cost/benefit ratio observed.
