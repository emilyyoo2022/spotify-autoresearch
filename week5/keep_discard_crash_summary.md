# Keep / Discard / Crash Summary — Week 5

**Block:** Feature engineering and preprocessing autonomous experiments
**Date:** 2026-05-11
**Experiments run:** 12 (E1–E12)
**Baseline RMSE (Week 5 start):** 15.0254

---

## KEEP (2)

| ID | Change | RMSE | Delta vs prior best |
|----|--------|------|---------------------|
| E1 | Add log1p(duration_ms) | 15.0232 | −0.0022 |
| E7 | Add log1p(instrumentalness) (on E1) | 15.0196 | −0.0036 |

Both kept changes involve log-transforming zero-heavy or right-skewed continuous features. The improvements are small but consistent.

---

## DISCARD (10)

| ID | Change | RMSE | Delta vs prior best | Reason |
|----|--------|------|---------------------|--------|
| E2 | log1p(loudness+60) | 15.0259 | +0.0027 | Loudness not skewed enough to benefit |
| E3 | Drop key/mode/time_signature/index | 15.7345 | +0.7113 | Those features carry real signal |
| E4 | danceability × energy interaction | 15.0361 | +0.0129 | RF finds interactions natively |
| E5 | energy × loudness interaction | 15.0292 | +0.0060 | RF finds interactions natively |
| E6 | tempo × danceability interaction | 15.0424 | +0.0192 | RF finds interactions natively |
| E8 | log_speechiness + log_acousticness added | 15.0261 | +0.0065 | Over-transformation; less skewed features |
| E9 | HistGradientBoostingRegressor tuned | 17.7524 | +2.7328 | Model family underperforms RF here |
| E10 | RF max_features=0.5 | 15.3764 | +0.3568 | Reducing feature diversity hurts |
| E11 | ExtraTreesRegressor | 15.4511 | +0.4315 | Extra randomization hurts here |
| E12 | RF min_samples_leaf=3 | 15.2800 | +0.2604 | Leaf regularization not the bottleneck |

---

## CRASH (0)

No crashes or runtime errors occurred in this block.

---

## Summary

- 2 of 12 experiments improved RMSE (17% keep rate)
- All kept changes were log-transforms of skewed numeric features
- All interaction terms were discarded: RF does not benefit from manually crafted products
- Feature dropping was strongly negative: no "junk" features identified
- Switching model families (HistGBR, ExtraTrees) did not help
- RF hyperparameter variants (max_features, min_samples_leaf) did not help
- Net RMSE improvement this week: 15.0254 → 15.0196 (−0.0058, −0.04% relative)
